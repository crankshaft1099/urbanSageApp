# Local Chatbot

A simple chatbot that can be hosted locally and makes API calls for each user message.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Chatbot

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Customizing the API

To modify the API endpoint, edit the `test_fun` function in `app.py`. Currently, it's a placeholder function that returns a simple response. Replace it with your actual API call implementation.

## Features

- Modern, responsive UI
- Real-time message updates
- Error handling
- Support for both click and Enter key to send messages 