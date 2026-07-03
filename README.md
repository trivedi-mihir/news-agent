# 🚀 AI News Email Agent

An intelligent Python-based automation that fetches the latest technology news, filters relevant articles, generates AI-powered summaries, and delivers a beautifully formatted newsletter directly to your inbox.

## ✨ Features

* 📰 Fetches the latest technology news from NewsAPI
* 🤖 AI-powered article summarization
* ⚡ Supports multiple AI providers

  * Groq (Recommended)
  * Cohere
  * Hugging Face
  * OpenAI
  * Local summarizer (No API required)
* 🔍 Filters articles using custom keywords
* 📧 Sends responsive HTML email newsletters
* ⏰ Daily automated scheduling
* 🎯 Customizable news sources and keywords
* 🛡️ Automatic fallback to local summarization if AI APIs fail

---

# 📌 Tech Stack

* Python 3.x
* NewsAPI
* Groq API
* Requests
* Schedule
* SMTP (Gmail)
* HTML Email Templates

---

# 📂 Project Structure

```
AI-News-Agent/
│
├── news_agent.py        # Main application
├── README.md

```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-News-Agent.git

cd AI-News-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually

```bash
pip install requests schedule
```

---

# 🔑 Configuration

Open **news_agent.py** and update the configuration section.

## News API

Create a free account at:

https://newsapi.org

Replace

```python
NEWS_API_KEY="YOUR_KEY"
```

---

## Groq API (Recommended)

Create a free API key:

https://console.groq.com

Replace

```python
GROQ_API_KEY="YOUR_KEY"
```

---

## Email Configuration

```python
EMAIL_ADDRESS="your_email@gmail.com"

EMAIL_PASSWORD="your_gmail_app_password"

RECIPIENTS=[
    "recipient1@gmail.com",
    "recipient2@gmail.com"
]
```

> **Important:** Use a Gmail App Password instead of your normal Gmail password.

---

# 📰 Supported AI Providers

| Provider         | Free         | Speed |
| ---------------- | ------------ | ----- |
| Groq             | ✅            | ⭐⭐⭐⭐⭐ |
| Cohere           | ✅            | ⭐⭐⭐⭐  |
| Hugging Face     | ✅            | ⭐⭐⭐   |
| OpenAI           | Paid / Trial | ⭐⭐⭐⭐⭐ |
| Local Summarizer | ✅            | ⭐⭐    |

Simply change

```python
AI_PROVIDER="groq"
```

to

```python
AI_PROVIDER="cohere"
```

or

```python
AI_PROVIDER="huggingface"
```

or

```python
AI_PROVIDER="openai"
```

or

```python
AI_PROVIDER="local"
```

---

# 🚀 Running the Project

Run once

```bash
python news_agent.py
```

Choose

```
1
```

to send a test newsletter.

---

Run Daily Scheduler

```bash
python news_agent.py
```

Choose

```
2
```

The application will automatically send newsletters every day at the configured time.

---

# 📧 Email Output

Each email contains:

* AI-generated summary
* Key Highlights
* AI & Emerging Tech Updates
* Major Tech Companies
* Industry Trends
* Direct links to original articles

---

# 🎯 Customization

### Change News Sources

```python
NEWS_SOURCES=[
    "techcrunch",
    "the-verge",
    "wired",
    "ars-technica"
]
```

---

### Change Keywords

```python
NEWS_KEYWORDS=[
    "AI",
    "Cloud",
    "Cybersecurity",
    "Google",
    "Microsoft",
    "Apple",
    "Startup"
]
```

---

### Change Schedule

```python
SCHEDULE_TIME="09:00"
```

Example

```python
SCHEDULE_TIME="18:30"
```

---

# 📸 Screenshots

Add screenshots here after running the project.

```
screenshots/

email-preview.png

terminal-output.png
```

---

# 🔮 Future Improvements

* Web dashboard
* Database support
* User authentication
* Newsletter analytics
* Multiple newsletter categories
* RSS feed support
* Docker support
* GitHub Actions automation
* AI-powered sentiment analysis
* PDF report generation

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Mihir Trivedi**

* Full Stack Developer
* Cloud Enthusiast
* AI Automation Developer
* Cybersecurity Learner

If you found this project useful, consider giving it a ⭐ on GitHub.
