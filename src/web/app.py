from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import requests
import time
from werkzeug.utils import secure_filename
from PIL import Image
import io
import logging
import json
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'dishes'
app.config['HISTORY_FILE'] = 'upload_history.json'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
API_TOKEN = os.getenv("OPENAI_API_KEY")

def load_upload_history():
    """Load upload history from JSON file"""
    try:
        if os.path.exists(app.config['HISTORY_FILE']):
            with open(app.config['HISTORY_FILE'], 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading upload history: {e}")
    return {}

def save_upload_history(history):
    """Save upload history to JSON file"""
    try:
        with open(app.config['HISTORY_FILE'], 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving upload history: {e}")

def get_file_hash(filepath):
    """Generate SHA-256 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error(f"Error generating file hash: {e}")
        return None

def check_previous_upload(file_hash):
    """Check if file has been uploaded before"""
    history = load_upload_history()
    return history.get(file_hash)

def record_upload(file_hash, filename, dishes, generated_images):
    """Record upload in history"""
    history = load_upload_history()
    history[file_hash] = {
        'filename': filename,
        'dishes': dishes,
        'generated_images': generated_images,
        'timestamp': time.time(),
        'upload_count': history.get(file_hash, {}).get('upload_count', 0) + 1
    }
    save_upload_history(history)

def extract_dishes(image_path):
    if not API_TOKEN:
        logger.error("OpenAI API key not set")
        return {"error": "OpenAI API key not set"}
    
    try:
        logger.info(f"Starting dish extraction for {image_path}")
        
        # Encode the image to base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        logger.info("Image encoded successfully")
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "List the food dish names from this menu image. Return only the dish names, one per line, as plain text. Do not use any formatting, code blocks, or markdown. Just list the actual food names."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        logger.info("Making OpenAI API request...")
        
        # Add timeout to prevent hanging
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60  # 60 second timeout
        )
        
        logger.info(f"OpenAI API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            logger.info(f"Received content: {content[:100]}...")
            
            # Parse the response into a list of dishes
            dishes = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Filter out non-dish text and markdown formatting
            filtered_dishes = []
            for dish in dishes:
                # Remove markdown code blocks
                if dish.startswith('```') or dish.endswith('```'):
                    logger.info(f"Skipping markdown code block: {dish}")
                    continue
                
                # Remove common prefixes like "1.", "-", "•", etc.
                dish = dish.lstrip('0123456789.-• ')
                
                # Skip lines that are clearly not dish names
                skip_phrases = [
                    'here are', 'the dishes', 'menu items', 'food items',
                    'sure', 'okay', 'here', 'menu', 'dishes', 'items',
                    'from the menu', 'on the menu', 'available', 'offered',
                    'plaintext', '```', 'code', 'format'
                ]
                
                dish_lower = dish.lower()
                if any(phrase in dish_lower for phrase in skip_phrases):
                    logger.info(f"Skipping non-dish text: {dish}")
                    continue
                
                # Skip very short or very long text (likely not dish names)
                if len(dish) < 3 or len(dish) > 100:
                    logger.info(f"Skipping text due to length: {dish}")
                    continue
                
                # Skip text that looks like explanations or formatting
                if dish.endswith(':') or dish.endswith('.') or ':' in dish:
                    logger.info(f"Skipping text with punctuation: {dish}")
                    continue
                
                # Skip lines that are just formatting characters
                if dish in ['```', '```plaintext', '```text', '```markdown']:
                    logger.info(f"Skipping formatting marker: {dish}")
                    continue
                
                if dish and len(dish) > 2:  # Only keep meaningful dish names
                    filtered_dishes.append(dish)
            
            logger.info(f"Extracted {len(filtered_dishes)} dishes: {filtered_dishes}")
            return {"dishes": filtered_dishes}
        else:
            error_msg = f"OpenAI API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
            
    except requests.exceptions.Timeout:
        error_msg = "OpenAI API request timed out after 60 seconds"
        logger.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Error extracting dishes: {e}"
        logger.error(error_msg)
        return {"error": error_msg}

def generate_image_with_openai(prompt, output_path):
    if not API_TOKEN:
        return False
    
    # Check if image already exists
    if os.path.exists(output_path):
        logger.info(f"Image already exists for: {prompt}")
        return True
    
    try:
        logger.info(f"Generating image for: {prompt}")
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": f"A beautiful, appetizing photo of {prompt}. High quality, professional food photography.",
            "n": 1,
            "size": "1024x1024"
        }
        
        # Add timeout to prevent hanging
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60  # 60 second timeout
        )
        
        logger.info(f"DALL-E API response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                logger.info(f"Image saved to: {output_path}")
                return True
            else:
                logger.error(f"Failed to download image: {img_response.status_code}")
                return False
        else:
            logger.error(f"DALL-E API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout generating image for: {prompt}")
        return False
    except Exception as e:
        logger.error(f"Error generating image for '{prompt}': {e}")
        return False

def sanitize_filename(dish_name):
    """Create a consistent filename from dish name"""
    # Remove special characters and normalize
    sanitized = dish_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    sanitized = sanitized.replace('&', 'and').replace('(', '').replace(')', '')
    sanitized = sanitized.replace('[', '').replace(']', '').replace('{', '').replace('}', '')
    sanitized = sanitized.replace(':', '').replace(';', '').replace(',', '').replace('.', '')
    sanitized = sanitized.replace('!', '').replace('?', '').replace('"', '').replace("'", '')
    sanitized = sanitized.replace('-', '_').replace('+', 'plus')
    
    # Remove multiple underscores
    while '__' in sanitized:
        sanitized = sanitized.replace('__', '_')
    
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    
    # Limit length
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized.lower()

def find_existing_image(dish_name, output_folder):
    """Find existing image with various naming patterns"""
    sanitized_dish = sanitize_filename(dish_name)
    
    # Check for new format first
    new_filename = f"{sanitized_dish}.png"
    new_path = os.path.join(output_folder, new_filename)
    if os.path.exists(new_path):
        logger.info(f"Found existing image with new format: {new_filename}")
        return new_filename, new_path
    
    # Check for old format patterns
    old_patterns = [
        f"{dish_name.replace(' ', '_')}.png",
        f"{dish_name.replace(' ', '_')}_0.png",
        f"{dish_name.replace(' ', '_')}_1.png",
        f"{dish_name.replace(' ', '_')}_2.png",
        f"{dish_name.replace(' ', '_')}_3.png",
        f"{dish_name.replace(' ', '_')}_4.png",
        f"{dish_name.replace(' ', '_')}_5.png",
        f"{dish_name.replace(' ', '_')}_6.png",
        f"{dish_name.replace(' ', '_')}_7.png",
        f"{dish_name.replace(' ', '_')}_8.png",
        f"{dish_name.replace(' ', '_')}_9.png",
    ]
    
    for old_filename in old_patterns:
        old_path = os.path.join(output_folder, old_filename)
        if os.path.exists(old_path):
            logger.info(f"Found existing image with old format: {old_filename}")
            return old_filename, old_path
    
    # Check for any file that contains the dish name (case insensitive)
    existing_files = os.listdir(output_folder)
    dish_lower = dish_name.lower()
    
    for existing_file in existing_files:
        if existing_file.lower().startswith(dish_lower.replace(' ', '_')):
            existing_path = os.path.join(output_folder, existing_file)
            logger.info(f"Found existing image with partial match: {existing_file}")
            return existing_file, existing_path
    
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Upload request received")
    
    if 'file' not in request.files:
        logger.error("No file in request")
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        logger.error("No filename")
        return jsonify({'error': 'No file selected'})
    
    if file:
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"File saved to: {filepath}")
            
            # Generate file hash and check for previous upload
            file_hash = get_file_hash(filepath)
            if file_hash:
                previous_upload = check_previous_upload(file_hash)
                if previous_upload:
                    logger.info(f"File previously uploaded {previous_upload['upload_count']} times, returning cached results")
                    
                    # Return cached results
                    return jsonify({
                        'dishes': previous_upload['dishes'],
                        'generated_images': previous_upload['generated_images'],
                        'total_generated': len(previous_upload['generated_images']),
                        'skipped_images': [],  # No new images generated
                        'total_skipped': 0,
                        'original_image': {
                            'filename': filename,
                            'path': f'/upload/{filename}'
                        },
                        'cached': True,
                        'upload_count': previous_upload['upload_count']
                    })
            
            # Extract dishes from the uploaded image
            logger.info("Starting dish extraction...")
            result = extract_dishes(filepath)
            
            if 'error' in result:
                logger.error(f"Dish extraction failed: {result['error']}")
                return jsonify(result)
            
            dishes = result['dishes']
            
            if not dishes:
                logger.warning("No dishes found")
                return jsonify({'error': 'No dishes found in the menu image'})
            
            logger.info(f"Found {len(dishes)} dishes, checking existing images...")
            
            # List existing files for debugging
            existing_files = os.listdir(app.config['OUTPUT_FOLDER'])
            logger.info(f"Existing files in dishes folder: {existing_files}")
            
            # Generate images for each dish (skip if already exists)
            generated_images = []
            skipped_images = []
            
            for i, dish in enumerate(dishes):
                logger.info(f"Processing dish {i+1}/{len(dishes)}: {dish}")
                
                # Try to find existing image with various naming patterns
                existing_filename, existing_path = find_existing_image(dish, app.config['OUTPUT_FOLDER'])
                
                if existing_filename and existing_path:
                    logger.info(f"Image already exists for: {dish} at {existing_path}")
                    skipped_images.append({
                        'dish': dish,
                        'filename': existing_filename,
                        'path': f'/image/{existing_filename}',
                        'status': 'existing'
                    })
                    generated_images.append({
                        'dish': dish,
                        'filename': existing_filename,
                        'path': f'/image/{existing_filename}'
                    })
                else:
                    logger.info(f"Generating new image for: {dish}")
                    # Create consistent filename for new images
                    sanitized_dish = sanitize_filename(dish)
                    filename = f"{sanitized_dish}.png"
                    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                    
                    success = generate_image_with_openai(dish, output_path)
                    if success:
                        generated_images.append({
                            'dish': dish,
                            'filename': filename,
                            'path': f'/image/{filename}'
                        })
                        logger.info(f"Successfully generated image for: {dish}")
                    else:
                        logger.error(f"Failed to generate image for: {dish}")
                
                time.sleep(2)  # Rate limiting
            
            logger.info(f"Completed processing. Generated {len(generated_images)} images, skipped {len(skipped_images)} existing images")
            
            # Record this upload in history
            if file_hash:
                record_upload(file_hash, filename, dishes, generated_images)
            
            return jsonify({
                'dishes': dishes,
                'generated_images': generated_images,
                'total_generated': len(generated_images),
                'skipped_images': skipped_images,
                'total_skipped': len(skipped_images),
                'original_image': {
                    'filename': filename,
                    'path': f'/upload/{filename}'
                },
                'cached': False
            })
            
        except Exception as e:
            logger.error(f"Error in upload_file: {e}")
            return jsonify({'error': f'Server error: {str(e)}'})

@app.route('/image/<filename>')
def serve_image(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

@app.route('/upload/<filename>')
def serve_upload(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051) 