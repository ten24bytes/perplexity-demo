# Perplexity API Chat Interface

This is a web application that provides a chat interface for interacting with the Perplexity AI models through their official API.

## Features

- Interactive chat interface with real-time responses
- Support for multiple Perplexity AI models
- Customizable model parameters (temperature and max tokens)
- Markdown rendering for AI responses
- Model information display (context window size and description)
- Error handling with user-friendly messages
- Simple and intuitive UI

## File Structure

- `app.py`: Main application file containing routes and API logic
- `templates/index.html`: Main page template with the chat interface
- `static/css/style.css`: Styling for the chat interface
- `static/js/script.js`: Frontend JavaScript for handling interactions
- `.env`: Environment variables configuration file

## Routes

- `/`: Home page displaying the chat interface and available models
- `/chat`: API endpoint for processing chat requests and returning AI responses

## Environment Variables

The application uses the following environment variables that should be set in a `.env` file:

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)
- `PERPLEXITY_API_URL`: The Perplexity API endpoint (defaults to `https://api.perplexity.ai/chat/completions`)
- `SYSTEM_PROMPT`: The system prompt to use for all conversations (defaults to "You are a helpful assistant.")

## Supported Models

The application supports the following Perplexity AI models:

- Sonar Deep Research: Advanced research capabilities with deep information processing
- Sonar Reasoning Pro: Enhanced reasoning capabilities for complex problem solving
- Sonar Reasoning: Strong reasoning capabilities for problem solving
- Sonar Pro: Premium model with extended context window (200k)
- Sonar: General purpose conversational model
- R1-1776: Open source model with strong reasoning capabilities

## Usage

1. Clone the repository
2. Create a `.env` file with your Perplexity API credentials:
   ```env
   PERPLEXITY_API_KEY=your_api_key_here
   PERPLEXITY_API_URL=https://api.perplexity.ai/chat/completions
   SYSTEM_PROMPT=You are a helpful AI assistant
   ```
3. Install dependencies with `pip install -r requirements.txt` or using the pyproject.toml
4. Run the application with `python app.py`
5. Access the interface in your browser at `http://localhost:5000`

## Parameter Settings

Users can adjust the following parameters through the interface:

- **Temperature**: Controls the randomness of the AI's responses (0.0 to 2.0)
- **Max Tokens**: Limits the length of the AI's responses (10 to 2000)

## Configuration

The available models are configured in the `PERPLEXITY_MODELS` variable in `app.py` and can be updated as new models become available.

## Requirements

- Python 3.12+
- Flask
- python-dotenv
- requests

## Alternative Setup with uv Package Manager

This project can also be set up using [uv](https://astral.sh/uv/), an extremely fast Python package and project manager written in Rust that's 10-100x faster than pip. uv provides a drop-in replacement for common pip, pip-tools, and virtualenv commands.

### Installing uv

First, install uv with the official standalone installer:

#### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

```powershell
# PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

### Setting Up the Project with uv

1. Clone the repository
2. Create a `.env` file as described in the Usage section above
3. Create and activate a virtual environment:
   ```bash
   uv venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
4. Install dependencies using uv:

   ```bash
   # Install from requirements.txt
   uv pip sync requirements.txt

   # Or install from pyproject.toml
   uv sync
   ```

5. Run the application:
   ```bash
   python app.py
   # Or using uv run
   uv run app.py
   ```

### Managing Dependencies with uv

uv offers several advantages for managing this project's dependencies:

- Update dependencies: `uv pip compile requirements.in --output-file requirements.txt`
- Add a new dependency: `uv add flask`
- Lock dependencies: `uv lock`
- Install a development tool: `uv tool install ruff`

The project already includes a `uv.lock` file for reproducible installations.

For more information about uv, refer to the [uv documentation](https://docs.astral.sh/uv/).

## Note

This application requires proper configuration of Perplexity API credentials. You must obtain an API key from Perplexity and add it to your `.env` file. Refer to the [Perplexity API documentation](https://docs.perplexity.ai/) for more details on authentication and API usage.
