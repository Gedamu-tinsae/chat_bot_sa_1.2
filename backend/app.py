from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import difflib
import os
import re
from huggingface_hub import InferenceClient
import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Hugging Face API Key
HF_API_KEY = os.getenv('HF_API_KEY') 
if not HF_API_KEY:
    raise ValueError("Hugging Face API key is not set!")

# Initialize InferenceClient with Hugging Face API key
client = InferenceClient(api_key=HF_API_KEY)

# Load responses from the JSON file
try:
    with open('responses.json', 'r') as f:
        responses = json.load(f)
except FileNotFoundError:
    logger.error("The responses.json file is missing!")
    responses = {}
except json.JSONDecodeError:
    logger.error("The responses.json file is not a valid JSON!")
    responses = {}

# # Scraping function
# def scrape_information(query):
#     """Scrape information from a specific website based on the query."""
#     try:
#         url = f"https://example.com/search?q={query}"  
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Replace with the correct HTML tags and classes
#         result = soup.find('div', class_='result-class')
#         return result.text.strip() if result else "No information found."
#     except Exception as e:
#         logger.error(f"Error while scraping: {e}")
#         return "Sorry, I couldn't fetch the information right now."

# # Scraping function-notion
# def scrape_information(query):
#     """Scrape information from a specific Notion page based on the query."""
#     try:
#         # The Notion page URL
#         url = "https://persistventure.notion.site/Persist-Ventures-x-Systemic-Altruism-Captains-Program-6715273ec3d347fd8bf230563ba0b539"
        
#         # Make a request to fetch the page content
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()
        
#         # Parse the page using BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
#         logger.info(f"soup: {soup}")
        
#         # Find the relevant content in the Notion page
#         # Notion uses <div> tags with specific classes for content blocks
#         content_blocks = soup.find_all('div', class_='notion-text-block')  # Adjust class based on Notion's structure
#         logger.info(f"content_blocks info: {content_blocks}")

        
#         # Extract and filter text content matching the query
#         for block in content_blocks:
#             text = block.get_text(strip=True)
#             if query.lower() in text.lower():
#                 return text
#             logger.info(f"Scrapped info: {text}")
        
        
#         return "No matching information found for your query."
    
#     except Exception as e:
#         logger.error(f"Error while scraping Notion page: {e}")
#         return "Sorry, I couldn't fetch the information from the Notion page."


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_information(query):
    """Scrape information from a specific Notion page based on the query."""
    try:
        # The Notion page URL
        url = "https://persistventure.notion.site/Persist-Ventures-x-Systemic-Altruism-Captains-Program-6715273ec3d347fd8bf230563ba0b539"
        
        # Set up Selenium WebDriver with headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run browser in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")

        # Use webdriver_manager to automatically manage ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the Notion page
        driver.get(url)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "notion-selectable"))
        )

        # Get the rendered page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find content blocks matching Notion's structure
        content_blocks = soup.find_all('div', class_='notion-selectable notion-text-block')
        logger.info(f"Content blocks found: {len(content_blocks)}")

        # Clean up and split query
        query = query.lower().replace("realtime", "").strip()  # Remove 'realtime' from the query
        query_words = query.split()  # Split the remaining query into words

        matching_blocks = []

        # Extract and filter text content matching any of the query words
        for block in content_blocks:
            text = block.get_text(strip=True).lower()
            logger.info(f"Block text: {text}")

            # Check if any of the words in the query match the block
            if any(word in text for word in query_words):
                matching_blocks.append(text)

        driver.quit()

        if matching_blocks:
            return "\n\n".join(matching_blocks)  # Join all matching blocks with a newline separator
        else:
            return "No matching information found for your query."
    
    except TimeoutException:
        logger.error("The page took too long to load.")
        return "Sorry, the Notion page is taking too long to load."
    except Exception as e:
        logger.error(f"Error while scraping Notion page with Selenium: {e}")
        return "Sorry, I couldn't fetch the information from the Notion page."


# Check if the user message is gibberish
def is_gibberish(user_message):
    if len(user_message) < 1:
        return True
    if bool(re.match(r'^[^a-zA-Z0-9\s]*$', user_message)):  # Corrected regex with raw string
        return True
    return False

@app.route('/')
def home():
    return "Backend is running!"

def get_best_match(user_message):
    questions = list(responses.keys())
    closest_match = difflib.get_close_matches(user_message, questions, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None

def get_bot_response(user_message):
    user_message = user_message.lower()
    if user_message in responses:
        return responses[user_message]
    for key in responses:
        if key in user_message:
            return responses[key]
    return None

def get_hugging_face_response(user_message, context=None):
    """Fetch response from Hugging Face model."""
    messages = [
        {"role": "system", "content": context or "You are a helpful assistant."},  # Use context from JSON
        {"role": "user", "content": user_message},
    ]

    try:
        # Call the model for a response
        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-alpha",  # Replace with your preferred model
            messages=messages,
            max_tokens=500,
        )
        assistant_response = completion.choices[0].message
        logger.info(f"api response: {assistant_response}")
        return assistant_response['content']
    except Exception as e:
        logger.error(f"Error from Hugging Face: {e}")
        return f"Error occurred: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        logger.info(f"User message: {user_message}")

        # Check for gibberish and return default response if it's gibberish
        if is_gibberish(user_message):
            logger.info(f"User message is gibberish: {user_message}")
            return jsonify({'response': responses.get('default', 'Sorry, I didn\'t understand that.')})

        # Limit the character length of the user's message 
        if len(user_message) > 200:
            user_message = user_message[:200]  # Truncate the message

        # Handle real-time information queries
        if "realtime" in user_message or "current" in user_message:
            scraped_response = scrape_information(user_message)
            logger.info(f"Scraped information: {scraped_response}")

            # Send the scraped data to the Hugging Face model for further processing
            model_response = get_hugging_face_response(user_message, context=scraped_response)
            logger.info(f"Processed model response: {model_response}")
            
            # Truncate the response if too long
            if len(model_response) > 250:
                model_response = model_response[:250] + "..."

            return jsonify({'response': model_response})

        # Check for a response in the JSON file
        matched_question = get_best_match(user_message)
        logger.info(f"matched_question: {matched_question}")
        json_response = responses.get(matched_question) if matched_question else None
        logger.info(f"json_response: {json_response}")

        # Combine JSON response and model response
        if json_response:
            # Pass the JSON response as context to the Hugging Face model
            final_response = get_hugging_face_response(user_message, context=json_response)
            logger.info(f"Matched final response: {final_response}")
        else:
            # Use the model alone if no match is found in JSON
            final_response = get_hugging_face_response(user_message)
            logger.info(f"api final response: {final_response}")

        # Truncate overly long responses
        if len(final_response) > 250:
            final_response = final_response[:250] + "..."

        return jsonify({'response': final_response})

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
