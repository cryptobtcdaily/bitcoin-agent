import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import json
from datetime import datetime
from fetch_news import fetch_news, fetch_price
from ai_writer import generate_full_content
from build_page import build_page

# ── Logging helper ────────────────────────────────────────────────────────────

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ── Save content as backup JSON ───────────────────────────────────────────────

def save_backup(content):
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)

    filename = f"{backup_dir}/content_{datetime.today().strftime('%Y-%m-%d')}.json"

    # Convert content to JSON-safe format
    backup = {
        "date": content["date"],
        "price": content["price"],
        "change": content["change"],
        "intro": content["intro"],
        "market_section": content["market_section"],
        "articles": [
            {
                "written": a["written"],
                "original": a["original"]
            }
            for a in content["articles"]
        ]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)

    log(f"Backup saved to {filename}")

# ── Main agent pipeline ───────────────────────────────────────────────────────

def run_agent():
    log("=" * 50)
    log("Bitcoin Daily Agent Starting...")
    log("=" * 50)

    # Step 1 — Fetch news
    log("Step 1: Fetching Bitcoin news and price...")
    try:
        articles = fetch_news(max_articles=6)
        price_data = fetch_price()
        log(f"Got {len(articles)} articles")
        log(f"Bitcoin price: {price_data['price']} {price_data['change']}")
    except Exception as e:
        log(f"ERROR fetching news: {e}")
        return False

    # Step 2 — Generate full AI content
    log("Step 2: Generating full AI content (this takes a few minutes)...")
    try:
        content = generate_full_content(articles, price_data)
        log("AI content generated successfully")
    except Exception as e:
        log(f"ERROR generating content: {e}")
        return False

    # Step 3 — Save backup
    log("Step 3: Saving content backup...")
    try:
        save_backup(content)
    except Exception as e:
        log(f"WARNING: Backup failed (non-critical): {e}")

    # Step 4 — Build webpage
    log("Step 4: Building webpage...")
    try:
        build_page(content)
        log("Webpage built successfully")
    except Exception as e:
        log(f"ERROR building page: {e}")
        return False

    log("=" * 50)
    log("Agent completed successfully!")
    log(f"Webpage updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}")
    log("=" * 50)
    return True

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    success = run_agent()
    if not success:
        log("Agent finished with errors. Check logs above.")
        exit(1)