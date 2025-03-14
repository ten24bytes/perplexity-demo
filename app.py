import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

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
    model_id = data.get('model', 'sonar')  # Default to 'sonar' if not specified
    
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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)
        
        # Print response details for debugging
        print(f"Status code: {response.status_code}")
        print(f"Response content: {response.text}")
        
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
        return jsonify({"error": f"API request failed: {error_detail}"}), 500
    except (KeyError, IndexError) as e:
        return jsonify({"error": f"Failed to parse API response: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)