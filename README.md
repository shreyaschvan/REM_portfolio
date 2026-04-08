# 🚀 Rohit — Portfolio & Assignment Hub

A personal portfolio and assignment management website built with **Streamlit**.

## ✨ Features

- **Work Profile** — About, skills, education, and projects  
- **Assignment Manager** — Upload, view, and delete PDF assignments  
- **Contact Page** — Social links and a quick message form  
- **Modern UI** — Dark glassmorphism theme with smooth animations  

## 🏃 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub  
2. Go to [share.streamlit.io](https://share.streamlit.io)  
3. Click **"New app"** → select your repo → set main file to `app.py`  
4. Click **"Deploy"**  

Your app will be live at `https://<your-app>.streamlit.app` 🎉

## 📁 Project Structure

```
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme & server config
├── .gitignore
├── uploaded_assignments/   # Runtime PDF storage (git-ignored)
└── README.md
```

## ✏️ Customize

Edit the `PROFILE` dictionary inside `app.py` to update your personal information, skills, education, and projects.
