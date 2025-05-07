import os
import requests
import logging  # Add logging import
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)  # Ensure .env overrides system variables

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL", "https://api.perplexity.ai/chat/completions")  # Default API URL if not set in .env
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")  # Configurable system prompt

if not PERPLEXITY_API_KEY:
    raise ValueError("No Perplexity API key found. Please set PERPLEXITY_API_KEY in .env file.")

# Current supported models from Perplexity API documentation
PERPLEXITY_MODELS = [
    {"id": "sonar-deep-research", "name": "Sonar Deep Research", "context": "128k", "description": "Advanced research capabilities with deep information processing."},
    {"id": "sonar-reasoning-pro", "name": "Sonar Reasoning Pro", "context": "128k", "description": "Enhanced reasoning capabilities for complex problem solving."},
    {"id": "sonar-reasoning", "name": "Sonar Reasoning", "context": "128k", "description": "Strong reasoning capabilities for problem solving."},
    {"id": "sonar-pro", "name": "Sonar Pro", "context": "200k", "description": "Premium model with extended context window (200k)."},
    {"id": "sonar", "name": "Sonar", "context": "128k", "description": "General purpose conversational model."},
    {"id": "r1-1776", "name": "R1-1776", "context": "128k", "description": "Open source model with strong reasoning capabilities."}
]


@app.route('/')
def index():
    return render_template('index.html', models=PERPLEXITY_MODELS)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    model_id = data.get('model', 'sonar')

    try:
        temperature = float(data.get('temperature', 0.7))
        if not (0 <= temperature < 2):
            logging.warning(f"Invalid temperature value received: {temperature}. Falling back to default or API default.")
            # Optionally, return a 400 error or use a default valid value
            # return jsonify({"error": "Temperature must be between 0 (inclusive) and 2 (exclusive)."}), 400
            # For now, let the API handle it or use its default by not overriding if invalid
    except ValueError:
        logging.warning("Invalid temperature format received. Falling back to default or API default.")
        # return jsonify({"error": "Invalid temperature value."}), 400
        temperature = 0.7  # Default fallback

    try:
        max_tokens = int(data.get('max_tokens', 512))
        if max_tokens <= 0:
            logging.warning(f"Invalid max_tokens value received: {max_tokens}. Falling back to default or API default.")
            # Optionally, return a 400 error or use a default valid value
            # return jsonify({"error": "Max tokens must be a positive integer."}), 400
            # For now, let the API handle it or use its default by not overriding if invalid
    except ValueError:
        logging.warning("Invalid max_tokens format received. Falling back to default or API default.")
        # return jsonify({"error": "Invalid max_tokens value."}), 400
        max_tokens = 512  # Default fallback

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Prepare the request to Perplexity API
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},  # Use configurable system prompt
            {"role": "user", "content": user_message}
        ],
        # Only include parameters if they are valid or you want to send them anyway
        # The Perplexity API has its own defaults if these are not sent
    }
    # Add temperature to payload if it's valid or you decide to send it
    if 0 <= temperature < 2:
        payload["temperature"] = temperature

    # Add max_tokens to payload if it's valid or you decide to send it
    if max_tokens > 0:
        payload["max_tokens"] = max_tokens

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)

        # Log response details
        logging.info(f"API Request to {model_id} - Status: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"API Error Response: {response.text}")

        response.raise_for_status()

        result = response.json()
        assistant_response = result["choices"][0]["message"]["content"]

        return jsonify({"response": assistant_response})

    except requests.exceptions.RequestException as e:
        error_detail = str(e)
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = f"{e} - Response: {e.response.text}"
            except:
                pass
        logging.error(f"API request failed: {error_detail}")  # Log the error
        return jsonify({"error": f"API request failed: {error_detail}"}), 500
    except (KeyError, IndexError) as e:
        logging.error(f"Failed to parse API response: {str(e)}")  # Log the error
        return jsonify({"error": f"Failed to parse API response: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
