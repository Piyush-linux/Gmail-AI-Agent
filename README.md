# 📧 Gmail Agent Summarizer

This Python application uses the Gmail API and OpenAI API to summarize the last 10 emails in your Gmail account.

## ✨ Features
- 🚀 Fetches the most recent 10 emails from your Gmail account.
- 📩 Retrieves and cleans the email content (text and HTML).
- 🤖 Summarizes the email content using OpenAI's GPT-based API.

## 🐍 Python Setup
```sh
mkdir gmail-ai-agent
cd gmail-ai-agent
python -m venv ./venv
source ./venv/bin/activate
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client beautifulsoup4 openai
```

## ☁️ Google Cloud Setup
1. 🌐 Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2. ✅ Enable the Gmail API for your project.
3. 🛠 Configure the OAuth Consent Screen:
   - Fill in the required details.
   - Add the scope `https://www.googleapis.com/auth/gmail.readonly`.
4. 🗂 Create credentials for the OAuth client:
   - Choose **Desktop App** as the application type.
   - Download the credentials file and rename it to `credentials.json`.

## 🔑 OpenAI API Setup
1. ✍️ Create an account on [OpenAI](https://openai.com/).
2. 🔐 Generate an API key from the [OpenAI API Portal](https://platform.openai.com/account/api-keys).

## 🏃‍♂️ Run the Code
1. 🔧 Export your OpenAI API key as an environment variable:
```sh
export OPENAI_API_KEY='your-openai-api-key'
```

2. ▶️ Run the application:
```sh
python app.py
```

## 🛠 How It Works
1. **Authenticate with Gmail API**:
   - Handles OAuth2 authentication.
   - Stores and refreshes credentials using `token.pickle`.
2. **Fetch Recent Emails**:
   - Retrieves up to 10 recent emails from your Gmail inbox.
   - Extracts subject, sender, date, and content.
3. **Clean and Summarize Content**:
   - Parses and cleans email content using BeautifulSoup.
   - Summarizes email content using OpenAI's GPT model.
4. **Output Summaries**:
   - Displays a concise summary of each email.

## 📋 Notes
- 🗃 Ensure that `credentials.json` is in the same directory as the Python script.
- 🔄 The `token.pickle` file will be created during the first run to store authentication tokens.
- 📜 Ensure your OpenAI API key is kept secure and not hardcoded in the script.

## 📜 License
This project is licensed under the MIT License. Feel free to modify and distribute it as needed.
