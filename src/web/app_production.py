from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import requests
import time
from werkzeug.utils import secure_filename
import logging
import json
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Use environment variables for configuration
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['OUTPUT_FOLDER'] = os.environ.get('OUTPUT_FOLDER', 'dishes')
app.config['HISTORY_FILE'] = os.environ.get('HISTORY_FILE', 'upload_history.json')

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
API_TOKEN = os.environ.get("OPENAI_API_KEY")

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
                            "text": "You are a menu analysis expert. Look at this menu image and extract all the food items/dishes listed. Return ONLY a JSON array of dish names, nothing else. For example: [\"Beef Taco\", \"Chicken Fajitas\", \"Carne Asada\"]"
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
        
        logger.info("Sending request to OpenAI...")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            logger.info(f"OpenAI response: {content}")
            
            # Try to parse JSON response
            try:
                dishes = json.loads(content)
                if isinstance(dishes, list):
                    logger.info(f"Successfully extracted {len(dishes)} dishes")
                    return {"dishes": dishes}
                else:
                    logger.error("Response is not a list")
                    return {"error": "Invalid response format"}
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON: {content}")
                return {"error": "Failed to parse response"}
        else:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return {"error": f"OpenAI API error: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"Error in extract_dishes: {e}")
        return {"error": f"Error extracting dishes: {str(e)}"}

def generate_image_with_openai(prompt, output_path):
    if not API_TOKEN:
        logger.error("OpenAI API key not set")
        return False
    
    try:
        logger.info(f"Generating image for: {prompt}")
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "dall-e-3",
            "prompt": f"Professional food photography of {prompt}, high quality, appetizing, well-lit, restaurant quality photo",
            "n": 1,
            "size": "1024x1024"
        }
        
        logger.info("Sending image generation request to OpenAI...")
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            logger.info("Downloading generated image...")
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                logger.info(f"Image saved to: {output_path}")
                return True
            else:
                logger.error(f"Failed to download image: {img_response.status_code}")
                return False
        else:
            logger.error(f"OpenAI image generation error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error in generate_image_with_openai: {e}")
        return False

def sanitize_filename(dish_name):
    """Convert dish name to safe filename"""
    import re
    # Remove special characters and replace spaces with underscores
    safe_name = re.sub(r'[^a-zA-Z0-9\s]', '', dish_name)
    safe_name = re.sub(r'\s+', '_', safe_name.strip())
    return safe_name

def find_existing_image(dish_name, output_folder):
    """Find existing image for a dish with various naming patterns"""
    try:
        # List all files in the output folder
        if not os.path.exists(output_folder):
            return None, None
            
        files = os.listdir(output_folder)
        
        # Create various possible filenames
        sanitized_dish = sanitize_filename(dish_name)
        possible_names = [
            f"{sanitized_dish}.png",
            f"{sanitized_dish}.jpg",
            f"{sanitized_dish}.jpeg",
            f"{dish_name.lower().replace(' ', '_')}.png",
            f"{dish_name.lower().replace(' ', '_')}.jpg",
            f"{dish_name.lower().replace(' ', '_')}.jpeg"
        ]
        
        # Check for exact matches first
        for filename in possible_names:
            if filename in files:
                return filename, os.path.join(output_folder, filename)
        
        # Check for partial matches
        dish_words = dish_name.lower().split()
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename_lower = filename.lower()
                # Check if all words in dish name appear in filename
                if all(word in filename_lower for word in dish_words):
                    return filename, os.path.join(output_folder, filename)
        
        return None, None
        
    except Exception as e:
        logger.error(f"Error finding existing image: {e}")
        return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Upload request received")
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file:
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"File saved to: {filepath}")
            
            # Check if file has been uploaded before
            file_hash = get_file_hash(filepath)
            previous_upload = check_previous_upload(file_hash)
            
            if previous_upload:
                logger.info(f"File previously uploaded {previous_upload['upload_count']} times, returning cached results")
                return jsonify({
                    'dishes': previous_upload['dishes'],
                    'generated_images': previous_upload['generated_images'],
                    'total_generated': len(previous_upload['generated_images']),
                    'skipped_images': [],
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
    # Get port from environment variable or default to 5051
    port = int(os.environ.get('PORT', 5051))
    app.run(host='0.0.0.0', port=port) 