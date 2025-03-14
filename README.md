# Perplexity API Chat Interface

This is a web application that provides a chat interface for interacting with the Perplexity AI models.

## Features

- Interactive chat interface
- Support for multiple Perplexity models
- Simple and intuitive UI

## File Structure

- `app.py`: Main application file containing routes and logic
- `templates/index.html`: Main page template

## Routes

- `/`: Home page displaying available models
- `/chat`: Endpoint for processing chat requests

## Usage

1. Clone the repository
2. Install dependencies
3. Run the application with `python app.py`
4. Access the interface in your browser at `http://localhost:5000`

## Configuration

Available models are configured in the `PERPLEXITY_MODELS` variable in `app.py`.

## Note

This application requires proper configuration of Perplexity API credentials. Refer to the Perplexity API documentation for more details on authentication.