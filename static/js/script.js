// filepath: d:\Code\perplexity-demo\static\js\script.js
document.addEventListener('DOMContentLoaded', function () {
  const chatContainer = document.getElementById('chat-container');
  const messageForm = document.getElementById('message-form');
  const messageInput = document.getElementById('message-input');
  const modelSelector = document.getElementById('model-selector');
  const modelDescription = document.getElementById('model-description');
  const modelContext = document.getElementById('model-context');
  const temperatureSlider = document.getElementById('temperature-slider');
  const temperatureValue = document.getElementById('temperature-value');
  const maxTokensSlider = document.getElementById('max-tokens-slider');
  const maxTokensValue = document.getElementById('max-tokens-value');

  // Display details for the initially selected model
  updateModelDetails();

  // Update the details when a different model is selected
  modelSelector.addEventListener('change', updateModelDetails);

  // Update slider value displays
  temperatureSlider.addEventListener('input', function () {
    temperatureValue.textContent = this.value;
  });
  maxTokensSlider.addEventListener('input', function () {
    maxTokensValue.textContent = this.value;
  });

  function updateModelDetails() {
    const selectedOption = modelSelector.options[modelSelector.selectedIndex];
    const description = selectedOption.getAttribute('data-description');
    const context = selectedOption.getAttribute('data-context');

    modelDescription.textContent = description;
    modelContext.textContent = context;
  }

  messageForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    const selectedModel = modelSelector.value;
    const temperature = temperatureSlider.value;
    const maxTokens = maxTokensSlider.value;

    // Add user message to chat
    addMessage('user', message);
    messageInput.value = '';

    // Add loading indicator
    const loadingElement = document.createElement('div');
    loadingElement.className = 'loading';
    loadingElement.textContent = 'Thinking...';
    chatContainer.appendChild(loadingElement);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          model: selectedModel,
          temperature: temperature,
          max_tokens: maxTokens,
        }),
      });

      // Remove loading indicator
      chatContainer.removeChild(loadingElement);

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || 'API request failed');
      }

      addMessage('assistant', data.response);
    } catch (error) {
      // Remove loading indicator if it still exists
      if (loadingElement.parentNode) {
        chatContainer.removeChild(loadingElement);
      }

      console.error('Error:', error);

      // Create an error message element
      const errorElement = document.createElement('div');
      errorElement.className = 'error-message';
      errorElement.textContent = `Error: ${
        error.message || 'Something went wrong. Please try again.'
      }`;
      chatContainer.appendChild(errorElement);

      // Remove the error message after 5 seconds
      setTimeout(() => {
        if (errorElement.parentNode) {
          chatContainer.removeChild(errorElement);
        }
      }, 5000);
    }
  });

  function addMessage(role, content) {
    const messageElement = document.createElement('div');
    messageElement.className =
      role === 'user' ? 'user-message' : 'assistant-message';
    messageElement.textContent = content;
    chatContainer.appendChild(messageElement);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
});
