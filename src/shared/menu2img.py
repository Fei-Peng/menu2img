import os
import sys
import requests
import time
import base64
from PIL import Image

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
API_TOKEN = os.getenv("OPENAI_API_KEY")

def extract_dishes(image_path):
    if not API_TOKEN:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable.")
        return []
    
    try:
        # Encode the image to base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4.1",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract only the menu items (food dishes) from this menu image. Return them as a simple list, one dish per line. Ignore prices, descriptions, headers, and other text. Only return the actual food dish names."
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
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse the response into a list of dishes
            dishes = [line.strip() for line in content.split('\n') if line.strip()]
            
            # Clean up any numbering or bullet points
            cleaned_dishes = []
            for dish in dishes:
                # Remove common prefixes like "1.", "-", "•", etc.
                dish = dish.lstrip('0123456789.-• ')
                if dish and len(dish) > 2:  # Only keep meaningful dish names
                    cleaned_dishes.append(dish)
            
            return cleaned_dishes
        else:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error extracting dishes: {e}")
        return []

def generate_image_with_openai(prompt, output_path):
    if not API_TOKEN:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable.")
        return False
    
    try:
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
        
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                return True
            else:
                print(f"Failed to download image: {img_response.status_code}")
                return False
        else:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error generating image for '{prompt}': {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python menu2img.py <menu_image_path>")
        sys.exit(1)
    menu_image_path = sys.argv[1]
    if not API_TOKEN:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable.")
        sys.exit(1)
    dishes = extract_dishes(menu_image_path)
    
    if not dishes:
        print("No dishes found in the menu image. Please check:")
        print("- The image contains a readable menu")
        print("- The image quality is good enough")
        print("- The menu items are clearly visible")
        sys.exit(1)
    
    print(f"Found {len(dishes)} dishes:")
    for dish in dishes:
        print(f"- {dish}")
    os.makedirs("dishes", exist_ok=True)
    for dish in dishes:
        filename = os.path.join("dishes", f"{dish.replace(' ', '_')}.png")
        print(f"Generating image for: {dish}")
        success = generate_image_with_openai(dish, filename)
        if success:
            print(f"Saved: {filename}")
        time.sleep(5)  # Avoid rate limits

if __name__ == "__main__":
    main() 