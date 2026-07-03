import os
import json
import smtplib
import schedule
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

CONFIG = {
    # AI Provider Selection
    # Options: "groq", "cohere", "huggingface", "local", "openai"
    "AI_PROVIDER": "groq",  # RECOMMENDED: Groq is FREE & FASTEST
    
    # News API Configuration
    "NEWS_API_KEY": "35b10403b86d4a6cb0b04007ac52843a",  # Get free key from newsapi.org
    "NEWS_SOURCES": ["techcrunch", "the-verge", "wired", "ars-technica"],
    "NEWS_KEYWORDS": ["AI", "artificial intelligence", "cloud", "cybersecurity", 
                      "startup", "tech", "Google", "Apple", "Microsoft", "OpenAI"],
    
    # AI API Keys (Only need ONE based on AI_PROVIDER choice)
    "GROQ_API_KEY": "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",  # FREE - Get from console.groq.com
    
    
    # Email Configuration
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "EMAIL_ADDRESS": "mihir123trivedi@gmail.com",
    "EMAIL_PASSWORD": "cafooljbxtgmkevt",  # Use App Password for Gmail
    "RECIPIENTS": ["trivedimihir260@gmail.com","darjiparth331@gmail.com","nishasharma24102004@gmail.com"],
    
    # Settings
    "SCHEDULE_TIME": "09:00",  # Daily at 9 AM
    "DAYS_BACK": 1,  # Fetch news from last N days
    "MAX_ARTICLES": 10,
}

def fetch_tech_news():
    """Fetch latest tech news from News API"""
    print("📰 Fetching tech news...")
    
    from_date = (datetime.now() - timedelta(days=CONFIG["DAYS_BACK"])).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": CONFIG["NEWS_API_KEY"],
        "sources": ",".join(CONFIG["NEWS_SOURCES"]),
        "from": from_date,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 50
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "ok":
            articles = data.get("articles", [])
            print(f"✅ Found {len(articles)} articles")
            return articles
        else:
            print(f"❌ News API error: {data.get('message', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"❌ Error fetching news: {str(e)}")
        return []

def filter_relevant_articles(articles):
    """Filter articles based on keywords"""
    print("🔍 Filtering relevant articles...")
    
    relevant = []
    keywords_lower = [k.lower() for k in CONFIG["NEWS_KEYWORDS"]]
    
    for article in articles:
        title = article.get("title", "").lower()
        description = article.get("description", "").lower()
        content = article.get("content", "").lower()
        
        text = f"{title} {description} {content}"
        
        for keyword in keywords_lower:
            if keyword in text:
                relevant.append(article)
                break
    
    relevant = relevant[:CONFIG["MAX_ARTICLES"]]
    print(f"✅ Filtered to {len(relevant)} relevant articles")
    return relevant

def summarize_with_groq(articles_text, prompt):
    """Use Groq API (FREE & FASTEST) - llama3-70b"""
    print("🧠 Using Groq AI (FREE)...")
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {CONFIG['GROQ_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",  # FREE model
                "messages": [
                    {"role": "system", "content": "You are a professional tech news analyst."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Groq API error: {str(e)}")
        return None

def summarize_with_cohere(articles_text, prompt):
    """Use Cohere API (FREE tier)"""
    print("🧠 Using Cohere AI (FREE)...")
    
    try:
        response = requests.post(
            "https://api.cohere.ai/v1/generate",
            headers={
                "Authorization": f"Bearer {CONFIG['COHERE_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "command",  # FREE model
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.7
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["generations"][0]["text"]
    except Exception as e:
        print(f"❌ Cohere API error: {str(e)}")
        return None

def summarize_with_huggingface(articles_text, prompt):
    """Use Hugging Face Inference API (FREE)"""
    print("🧠 Using Hugging Face AI (FREE)...")
    
    try:
        # Using Mistral-7B model (free)
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers={
                "Authorization": f"Bearer {CONFIG['HUGGINGFACE_API_KEY']}"
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.7
                }
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"].split(prompt)[-1].strip()
    except Exception as e:
        print(f"❌ Hugging Face API error: {str(e)}")
        return None

def summarize_with_openai(articles_text, prompt):
    """Use OpenAI API ($5 FREE credit for new users)"""
    print("🧠 Using OpenAI GPT-3.5 (FREE $5 credit)...")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {CONFIG['OPENAI_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",  # Cheap & good
                "messages": [
                    {"role": "system", "content": "You are a professional tech news analyst."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return None

def summarize_locally(articles_text, prompt):
    """Use local summarization (NO API NEEDED - 100% FREE & OFFLINE)"""
    print("🧠 Using local summarization (FREE & OFFLINE)...")
    
    
    lines = []
    lines.append("## 📊 Tech News Summary\n")
    lines.append("### Key Highlights\n")
    
    # Extract first 3 articles as highlights
    articles_list = articles_text.split("\n\n")
    for i, article in enumerate(articles_list[:3], 1):
        if "Title:" in article or str(i) + "." in article:
            title_line = [line for line in article.split("\n") if "Title:" in line or ". " in line][0]
            lines.append(f"• {title_line.split(':', 1)[-1].strip()}")
    
    lines.append("\n### Today's Tech Topics\n")
    
    # Count keywords in articles
    keyword_counts = {}
    for keyword in CONFIG["NEWS_KEYWORDS"]:
        count = articles_text.lower().count(keyword.lower())
        if count > 0:
            keyword_counts[keyword] = count
    
    # List top topics
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for keyword, count in sorted_keywords:
        lines.append(f"• **{keyword}** - {count} mentions")
    
    lines.append("\n### Industry Focus\n")
    lines.append("Multiple developments across AI, cloud computing, and major tech companies. ")
    lines.append("Key trends indicate continued innovation in artificial intelligence and cybersecurity sectors.")
    
    lines.append("\n### Recommendation\n")
    lines.append("Review the full articles below for detailed insights into these emerging technologies and market developments.")
    
    return "\n".join(lines)

def summarize_with_ai(articles):
    """Main AI summarization router - uses selected provider"""
    
    if not articles:
        return "No relevant tech news found today."
    
    # Prepare article data
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"\n{i}. Title: {article['title']}\n"
        articles_text += f"   Source: {article['source']['name']}\n"
        articles_text += f"   Description: {article.get('description', 'N/A')}\n"
        articles_text += f"   URL: {article['url']}\n"
    
    # Create prompt
    prompt = f"""You are a tech news analyst. Analyze these recent tech articles and create a professional summary.

Articles:
{articles_text}

Create a well-structured summary with these sections:
1. **Key Highlights** - Most important news (2-3 bullet points)
2. **AI & Emerging Tech** - AI-related developments
3. **Major Tech Companies** - Updates from big tech firms
4. **Trends & Analysis** - Overall patterns and implications

Keep it professional, concise, and actionable. Focus on business impact and future relevance.
Write in a newsletter style that's engaging but professional."""

    # Route to selected AI provider
    provider = CONFIG["AI_PROVIDER"].lower()
    
    if provider == "groq":
        summary = summarize_with_groq(articles_text, prompt)
    elif provider == "cohere":
        summary = summarize_with_cohere(articles_text, prompt)
    elif provider == "huggingface":
        summary = summarize_with_huggingface(articles_text, prompt)
    elif provider == "openai":
        summary = summarize_with_openai(articles_text, prompt)
    elif provider == "local":
        summary = summarize_locally(articles_text, prompt)
    else:
        print(f"⚠️ Unknown AI provider: {provider}. Using local summarization.")
        summary = summarize_locally(articles_text, prompt)
    
    # Fallback to local if API fails
    if not summary:
        print("⚠️ AI API failed. Using local summarization as fallback.")
        summary = summarize_locally(articles_text, prompt)
    
    print("✅ Summary generated successfully")
    return summary

def generate_email_html(summary, articles):
    """Generate HTML email content"""
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # Article links section
    links_html = ""
    for i, article in enumerate(articles[:5], 1):
        links_html += f"""
        <tr>
            <td style="padding: 10px 0; border-bottom: 1px solid #eee;">
                <strong>{i}. {article['title']}</strong><br>
                <span style="color: #666; font-size: 15px;">{article['source']['name']}</span><br>
                <a href="{article['url']}" style="color: #0066cc; text-decoration: none;">Read Full Article →</a>
            </td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.9; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 28px;">🚀 Tech News Digest</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px; opacity: 0.9;">{date_str}</p>
        </div>
        
        <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
            
            <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px;">
                <h2 style="color: #667eea; margin-top: 0;">📊 AI-Generated Summary</h2>
                <div style="color: #444; white-space: pre-line;">
{summary}
                </div>
            </div>
            
            <div style="background: white; padding: 25px; border-radius: 8px;">
                <h2 style="color: #667eea; margin-top: 0;">🔗 Top Articles</h2>
                <table style="width: 100%; border-collapse: collapse;">
{links_html}
                </table>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd;">
                <p style="color: #666; font-size: 17px;">
                    Generated by AI News Agent (100% FREE)<br>
                    Powered by {CONFIG['AI_PROVIDER'].upper()} AI<br>
                    <a href="mailto:{CONFIG['EMAIL_ADDRESS']}?subject=Unsubscribe" style="color: #999;">Unsubscribe</a>
                </p>
            </div>
            
        </div>
        
    </body>
    </html>
    """
    
    return html

def send_email(subject, html_content):
    """Send email via SMTP"""
    print("📧 Sending email...")
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = CONFIG['EMAIL_ADDRESS']
        msg['To'] = ", ".join(CONFIG['RECIPIENTS'])
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(CONFIG['SMTP_SERVER'], CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(CONFIG['EMAIL_ADDRESS'], CONFIG['EMAIL_PASSWORD'])
            server.send_message(msg)
        
        print(f"✅ Email sent to {len(CONFIG['RECIPIENTS'])} recipients")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False
def run_news_agent():
    """Main workflow - fetch, analyze, and send"""
    print("\n" + "="*50)
    print(f"🤖 AI News Agent Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Using AI Provider: {CONFIG['AI_PROVIDER'].upper()}")
    print("="*50)
    
    # Step 1: Fetch news
    articles = fetch_tech_news()
    if not articles:
        print("⚠️ No articles found. Exiting.")
        return
    
    # Step 2: Filter relevant articles
    relevant_articles = filter_relevant_articles(articles)
    if not relevant_articles:
        print("⚠️ No relevant articles found. Exiting.")
        return
    
    # Step 3: Generate AI summary
    summary = summarize_with_ai(relevant_articles)
    
    # Step 4: Generate email HTML
    email_html = generate_email_html(summary, relevant_articles)
    
    # Step 5: Send email
    subject = f"Tech News Digest - {datetime.now().strftime('%B %d, %Y')}"
    send_email(subject, email_html)
    
    print("="*50)
    print("✅ News Agent Completed Successfully!")
    print("="*50 + "\n")

def start_scheduler():
    """Schedule the news agent to run daily"""
    print(f"⏰ Scheduler started. Will run daily at {CONFIG['SCHEDULE_TIME']}")
    
    schedule.every().day.at(CONFIG['SCHEDULE_TIME']).do(run_news_agent)
    
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    print("\n🚀 AI News Email Agent (100% FREE VERSION)")
    print("=" * 50)
    
    print(f"\n✅ Current AI Provider: {CONFIG['AI_PROVIDER'].upper()}")
    print("\nAvailable FREE AI Providers:")
    print("  • groq       - FREE & Fastest ")
    
    # Validate configuration
    if CONFIG["NEWS_API_KEY"] == "your_newsapi_key_here":
        print("\n⚠️  Please set your NEWS_API_KEY in the CONFIG section")
    
    provider = CONFIG["AI_PROVIDER"].lower()
    if provider == "groq" and CONFIG["GROQ_API_KEY"] == "your_groq_api_key_here":
        print("⚠️  Please set your GROQ_API_KEY (FREE from console.groq.com)")
    elif provider == "cohere" and CONFIG["COHERE_API_KEY"] == "your_cohere_api_key_here":
        print("⚠️  Please set your COHERE_API_KEY (FREE from cohere.com)")
    elif provider == "huggingface" and CONFIG["HUGGINGFACE_API_KEY"] == "your_hf_api_key_here":
        print("⚠️  Please set your HUGGINGFACE_API_KEY (FREE from huggingface.co)")
    elif provider == "openai" and CONFIG["OPENAI_API_KEY"] == "your_openai_api_key_here":
        print("⚠️  Please set your OPENAI_API_KEY (FREE $5 credit)")
    elif provider == "local":
        print("✅ Using local AI - No API key needed!")
    
    if CONFIG["EMAIL_PASSWORD"] == "your_app_password":
        print("⚠️  Please set your EMAIL_PASSWORD in the CONFIG section")
    
    print("\nOptions:")
    print("1. Run once now (test)")
    print("2. Start scheduler (daily automation)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        run_news_agent()
    elif choice == "2":
        start_scheduler()
    else:
        print("Invalid choice. Exiting.")