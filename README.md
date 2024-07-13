# Legal Advice Chatbot

A simple legal advice chatbot using API integration with advanced language models like ChatGPT or Gemini.

## Features

- Provides legal advice on specific areas like family law and employment law.
- Uses advanced NLP models for accurate and context-aware responses.
- Simple web interface for user interaction.

## Tech Stack

- **API**: OpenAI (ChatGPT), Gemini, or similar
- **Web Framework**: Flask
- **Programming Language**: Python

## Prerequisites

- Python 3.7+
- OpenAI or Gemini API key

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/legal-advice-chatbot.git
    cd legal-advice-chatbot
    ```

2. **Create and Activate Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up API Key**

    - Create a `.env` file in the project root:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Running the Application

```bash
python app.py
