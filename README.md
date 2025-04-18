
# 📧 Send Multiple Emails App with Streamlit

A beautiful and user-friendly Streamlit web app to send personalized bulk emails using Gmail. Features rich text email body, file attachments, and customizable recipient list via CSV upload or manual entry.

---

## ✨ Features

- 🔐 Secure Gmail authentication via App Passwords  
- 📝 Rich-text email editor using `streamlit-quill` (bold, italic, links, etc.)  
- 📎 Attach one or more files to be sent with the email  
- 📤 Send bulk emails to users listed in a CSV or added manually  
- 🎨 Beautiful custom interface with styled inputs, hover effects, and alerts  
- 💡 Error handling with friendly emoji feedback  

---

## 📁 Project Structure

```
📦 your_project/
├── Send_Multiple_Emails.py     # Main Streamlit app
├── user_emails.csv                  # (Optional) CSV with sample name,email data
└── README.md                   # This file
```

---


1. **Clone this repository:**

```bash
git clone https://github.com/MuhammadMusabYaqoob/Send_Multiple_Emails.git
cd Send_Multiple_Emails
```

2. **Create a virtual environment and activate it (optional but recommended)**

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not present, use:

```bash
pip install streamlit streamlit-quill
```

---

## 🚀 Run the App

```bash
streamlit run Send_Multiple_Emails.py
```

---

## 🧠 Gmail App Password Setup

To send emails, Gmail requires an App Password:

1. Go to [Google Account Security Settings](https://myaccount.google.com/security)  
2. Enable **2-Step Verification**  
3. After enabling, find **App passwords**  
4. Generate one for "Mail" → "Windows Computer"  
5. Copy the password and paste it in the app  

---

## 📊 CSV Format

To bulk upload recipients, prepare a CSV file like:

```csv
John, john@example.com
Jane, jane@example.com
```

Only `name, email` format supported.

---


---

## 📄 License

This project is open-source and free to use.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.
