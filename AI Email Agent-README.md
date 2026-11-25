# 📧 AI Email Agent – Generate & Send Professional Emails

An AI-powered email assistant built using **Python, LangChain, Ollama, Gradio, and Gmail API**.

Generate professional emails from simple natural-language instructions, review the generated content, and send emails directly through your Gmail account.

## ✨ Features

- 🤖 **AI Email Generation:** Generate professional emails using Llama 3.2.
- 📝 **Structured Output:** Automatically generates separate email subjects and bodies using Pydantic.
- 📩 **Gmail Integration:** Send emails directly using the official Gmail API.
- ✅ **Email Validation:** Validate recipient email addresses using Pydantic's `EmailStr`.
- 👀 **Review Before Sending:** Edit and review generated emails before sending.
- 🔐 **OAuth 2.0 Authentication:** Securely authorize Gmail access.
- 🌐 **Interactive Interface:** Simple and user-friendly Gradio interface.
- 🚫 **Fact Protection:** Instructs the LLM not to invent personal information or commitments.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM integration and structured output |
| Ollama | Runs the local Llama model |
| Llama 3.2 (3B) | Email generation |
| Pydantic | Structured output and email validation |
| Gradio | Interactive web interface |
| Gmail API | Sending emails |
| Google OAuth 2.0 | Gmail authorization |

## 🏗️ Architecture

```text
          👤 User
             |
             ▼
       🌐 Gradio UI
             |
             ▼
      📧 Recipient Email
      📝 Email Description
             |
             ▼
       📋 Email Validation
             |
             ▼
       🧠 LangChain + Ollama
             |
             ▼
      🤖 Llama 3.2 (3B)
             |
             ▼
       📦 Pydantic Output
             |
       ┌─────┴─────┐
       ▼           ▼
    Subject       Body
       |           |
       └─────┬─────┘
             |
             ▼
       👀 User Review
             |
             ▼
       📩 Gmail API
             |
             ▼
       ✅ Email Sent
```

## 📂 Project Structure

```text
AI-Email-Agent/
│
├── main.py
├── credentials.json
├── token.json
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** `credentials.json` and `token.json` are generated or obtained during Google OAuth setup. Never upload them to a public repository.

## ⚙️ Prerequisites

Before running the application, make sure you have:

- Python 3.10 or later.
- Ollama installed.
- Llama 3.2 (3B) model downloaded.
- A Google account.
- Gmail API enabled in Google Cloud Console.
- Google OAuth Desktop application credentials.

## 🚀 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Email-Agent
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install gradio langchain-ollama pydantic email-validator google-auth google-auth-oauthlib google-api-python-client
```

### 4️⃣ Install and start Ollama

Download Ollama:

https://ollama.com/download

Download the model:

```bash
ollama pull llama3.2:3b
```

Make sure the Ollama service is running.

### 5️⃣ Configure Gmail API

Follow these steps:

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Create a Google Cloud project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen.
5. Create OAuth Client ID credentials.
6. Select **Desktop App** as the application type.
7. Download the OAuth credentials JSON file.
8. Rename it to `credentials.json`.
9. Place it in the project root directory.

The application requests this Gmail permission:

```text
https://www.googleapis.com/auth/gmail.send
```

On the first execution, Google OAuth authorization opens in your browser. Authorize the application using the intended Gmail account.

The generated `token.json` stores the authorization tokens for subsequent runs.

### 6️⃣ Run the application

```bash
python main.py
```

Open the Gradio interface in your browser.

## 💡 How to Use

**Step 1:** Enter the recipient's email address.

**Step 2:** Describe the email you want to generate.

Example:

```text
Write a professional email requesting
permission to attend a technical interview
on a different date due to an unavoidable
personal commitment.
```

**Step 3:** Click `Generate Email`.

**Step 4:** Review and edit the generated subject and body.

**Step 5:** Click `Send Email` to send it through Gmail.

🎉 Your email is sent!

## 🔒 Security & Privacy

- Never upload `credentials.json` to GitHub.
- Never upload `token.json` to GitHub.
- Do not expose OAuth credentials or access tokens.
- Review generated emails before sending.
- Use Gmail's OAuth authorization instead of storing Gmail passwords.

Recommended `.gitignore`:

```gitignore
.env
credentials.json
token.json
venv/
__pycache__/
*.pyc
```

## ⚠️ Troubleshooting

| Problem | Possible Solution |
|---|---|
| Ollama connection error | Make sure Ollama is running |
| Model not found | Run `ollama pull llama3.2:3b` |
| Invalid email address | Check the recipient address |
| Gmail API error | Verify Gmail API is enabled |
| OAuth error | Check OAuth credentials and consent configuration |
| Structured output error | Verify model and LangChain structured-output compatibility |
| Missing Python package | Install the required dependencies |

## 🔮 Future Enhancements

- ✍️ Multiple email writing styles.
- 🌍 Multilingual email generation.
- 📎 Email attachment support.
- 📬 Gmail inbox integration.
- 📨 Reply and follow-up email generation.
- 💾 Save generated email drafts.
- 🎯 Context-aware email personalization.

## 👨‍💻 Author

Developed using Python, LangChain, Ollama, Gradio, and Google APIs.

⭐ If you find this project useful, consider giving it a star on GitHub!

---

**Disclaimer:** This application generates email content using an AI model. Always review generated content before sending it.