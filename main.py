import base64
from pathlib import Path
from email.mime.text import MIMEText
import gradio as gr
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field, EmailStr, TypeAdapter
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
llm = ChatOllama(model="llama3.2:3b", temperature=0.3)

class GeneratedEmail(BaseModel):
    subject: str = Field(description="Professional email subject")
    body: str = Field(description="Complete professional email body")

email_generator = llm.with_structured_output(GeneratedEmail)

def validate_email(recipient):
    return str(TypeAdapter(EmailStr).validate_python(recipient.strip()))

def generate_email(recipient, description):
    recipient = validate_email(recipient)
    if not description or not description.strip():
        raise ValueError("Email description cannot be empty.")
    email = email_generator.invoke(f"""
    Generate a professional email.
    Recipient: {recipient}
    User instructions: {description}
    Generate an appropriate subject and complete email body.
    Do not invent personal information, dates, names, commitments, or facts that the user has not provided.
    Return only the generated subject and body.
    """)
    return {"recipient": recipient, "subject": email.subject, "body": email.body}

def authenticate_gmail():
    creds = None
    token_path = BASE_DIR / "token.json"
    credentials_path = BASE_DIR / "credentials.json"
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def send_email(recipient, subject, body):
    recipient = validate_email(recipient)
    if not subject or not subject.strip():
        raise ValueError("Subject cannot be empty.")
    if not body or not body.strip():
        raise ValueError("Email body cannot be empty.")
    service = authenticate_gmail()
    message = MIMEText(body, "plain", "utf-8")
    message["to"] = recipient
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    result = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
    return {"status": "success", "message_id": result["id"], "recipient": recipient}

def generate_email_ui(recipient, description):
    try:
        result = generate_email(recipient, description)
        return result["subject"], result["body"], "Email generated successfully."
    except Exception as e:
        return "", "", f"Error: {str(e)}"

def send_email_ui(recipient, subject, body):
    try:
        result = send_email(recipient, subject, body)
        return f"Email sent successfully! Message ID: {result['message_id']}"
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(title="AI Email Agent") as demo:
    gr.Markdown("# AI Email Agent")
    gr.Markdown("Generate professional emails using Ollama and send them through Gmail.")
    recipient = gr.Textbox(label="Recipient Email")
    description = gr.Textbox(label="Describe the email", lines=4)
    generate_btn = gr.Button("Generate Email")
    subject = gr.Textbox(label="Subject")
    body = gr.Textbox(label="Email Body", lines=10)
    generate_status = gr.Textbox(label="Generation Status", interactive=False)
    generate_btn.click(generate_email_ui, inputs=[recipient, description], outputs=[subject, body, generate_status])
    gr.Markdown("### Review your email before sending")
    send_btn = gr.Button("Send Email", variant="primary")
    send_status = gr.Textbox(label="Sending Status", interactive=False)
    send_btn.click(send_email_ui, inputs=[recipient, subject, body], outputs=send_status)

if __name__ == "__main__":
    demo.launch()