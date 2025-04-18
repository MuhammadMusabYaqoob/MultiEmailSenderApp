import streamlit as st
import csv, smtplib, ssl
from datetime import date
from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from streamlit_quill import st_quill

st.set_page_config(page_title="Email Sender App", page_icon="📧", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #F5EEDD;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 10px;
        background-color: #fff;
    }
    .stTextArea textarea {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a123;
        color: #fff;
        transform: scale(1.05);
        transition: all 0.3s ease;
    }
    .stFileUploader > div {
        background-color: #f0f0f5;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def send_email(from_address, password, to_address, subject, html_body, attachments=[]):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject

        msg.attach(MIMEText(html_body, 'html'))

        for attachment in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment.name}"')
            msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())

    except smtplib.SMTPAuthenticationError:
        raise Exception("🔒 Authentication failed. Please check your email and app password.")
    except smtplib.SMTPRecipientsRefused:
        raise Exception(f"❌ Recipient address refused: {to_address}")
    except smtplib.SMTPException as e:
        raise Exception(f"📡 SMTP error occurred: {e}")
    except Exception as e:
        raise Exception(f"⚠️ An unexpected error occurred: {e}")

st.title("📧 Send Multiple Emails App")

with st.expander("Step 1: Enable App Password in Gmail"):
    st.markdown("""
    **Before you can send emails, you need to enable an App Password:**

    1. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
    2. Turn on **2-Step Verification** (if it's off)
    3. After enabling it, scroll down to **App passwords** option
    4. Click **App passwords** > Type anything (e.g **Mail**) > Click **Generate**
    5. Copy the 16-character password and paste it below
    """)

st.header("Step 2: Sender Email Info")
from_address = st.text_input("Enter your Gmail address", placeholder="jhon@example.com")
password = st.text_input("App Password with Spaces", type="password", placeholder="xxxx xxxx xxxx xxxx", help="Paste the 16-character password generated from your Google Account")

st.header("Step 3: Email Content")
subject_template = st.text_input("Enter Email Subject", placeholder="Job Hiring")

st.markdown("**Compose your email below**")
body_template = st_quill(html=True)
st.markdown(
    "<span style='color: red; font-weight: bold;'>⚠️ Note:</span> "
    "Files and images will not be sent in the email body. Use attachments for files.",
    unsafe_allow_html=True
)


attachments = st.file_uploader("Attach file(s) (optional)", type=None, accept_multiple_files=True)

st.header("Step 4: Add Recipient Emails")
email_data = []

uploaded_file = st.file_uploader("Upload CSV with name and email (e.g. John, john@example.com)", type="csv")
if uploaded_file is not None:
    try:
        content = StringIO(uploaded_file.getvalue().decode("utf-8"))
        reader = csv.reader(content)
        email_data = [(row[0], row[1]) for row in reader if len(row) == 2]
        if not email_data:
            st.warning("⚠️ The uploaded file is empty or incorrectly formatted.")
        else:
            st.success(f"📁 Uploaded {len(email_data)} recipients from file.")
    except Exception as e:
        st.error(f"❗ Error reading CSV file: {e}")
else:
    st.write("Or enter emails manually:")
    manual_entries = []
    num_manual = st.number_input("How many people do you want to add?", min_value=1, value=1)
    for i in range(num_manual):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Name {i+1}", key=f"name_{i}")
        with col2:
            email = st.text_input(f"Email {i+1}", key=f"email_{i}")
        if name and email:
            manual_entries.append((name, email))
    email_data = manual_entries

if st.button("Send Emails"):
    try:
        if not from_address or not password:
            st.error("🔐 Please enter your email and app password.")
        elif not subject_template:
            st.error("✉️ Please enter a subject for the email.")
        elif not body_template:
            st.error("📝 Please compose the email body.")
        elif not email_data:
            st.error("📭 No recipient emails provided.")
        else:
            today = date.today().strftime('%B %d %Y')
            success_count = 0
            for name, email in email_data:
                try:
                    subject = subject_template
                    html_body = body_template.format(name=name, date=today)
                    send_email(from_address, password, email, subject, html_body, attachments)
                    success_count += 1
                except Exception as e:
                    st.error(f"❌ Failed to send to {email}: {e}")

            if success_count:
                st.success(f"✅ Successfully sent emails to {success_count} recipient(s).")
            else:
                st.warning("⚠️ No emails were sent successfully.")
    except Exception as e:
        st.error(f"🚨 Unexpected error: {e}")
