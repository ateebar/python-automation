import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone

# Çəkiləcək RSS feed-lərin siyahısı
NEWS_SOURCES = {
    "BBC News (Global)": "https://feeds.bbci.co.uk/news/rss.xml",
    "Associated Press (AP)": "https://feedx.net/rss/ap.xml",
    "Global Voices": "https://globalvoices.org/feed/",
    "Yahoo News (US)": "https://news.yahoo.com/rss/us",
    "Phys.org (Science & Tech)": "https://phys.org/rss-feed/"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_feed_news(source_name, feed_url, max_items=15):
    print(f"🔄 [{source_name}] Məlumat çəkilir...")
    try:
        response = requests.get(feed_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')
        
        # Bu günün tarixi (məsələn: '21 Oct 2026' formatında UTC üzrə)
        today_str = datetime.now(timezone.utc).strftime('%d %b %Y')
        
        extracted_articles = []
        for item in items[:max_items]:
            title = item.title.text.strip() if item.title else "Başlıq yoxdur"
            link = item.link.text.strip() if item.link else "Link yoxdur"
            pub_date = item.pubDate.text.strip() if item.pubDate else ""
            
            # Yalnız bugünkü tarixi ehtiva edən xəbərləri süzgəcdən keçirək
            # (RSS tarix formatı adətən 'Wed, 21 Oct 2026 07:06:10 GMT' kimidir)
            if today_str in pub_date:
                extracted_articles.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "pub_date": pub_date
                })
            
        print(f"✅ [{source_name}] Bu günə aid {len(extracted_articles)} xəbər tapıldı.")
        return extracted_articles
    except Exception as e:
        print(f"❌ [{source_name}] Xəta baş verdi: {e}")
        return []

def main():
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    print(f"=== BUGÜNKÜ XƏBƏRLƏR ÇƏKİLİR ({current_time} UTC) ===\n")
    
    all_news = []
    
    for source_name, feed_url in NEWS_SOURCES.items():
        articles = fetch_feed_news(source_name, feed_url, max_items=20)
        all_news.extend(articles)
        
    print("\n" + "=" * 60)
    print(f"CƏMİ BUGÜNKÜ XƏBƏR SAYI: {len(all_news)}")
    print("=" * 60)
    
    for i, news in enumerate(all_news, 1):
        print(f"{i}. [{news['source']}] {news['title']}")
        print(f"   📅 {news['pub_date']}")
        print(f"   🔗 {news['link']}\n")
        
    # Nəticələri JSON faylı kimi yaddaşa yazaq (Hər dəfə yalnız bugünkü təmiz siyahı yazılacaq)
    with open("latest_news.json", "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)
        
    print("💾 Yalnız bugünkü xəbərlər 'latest_news.json' faylına yeniləndi!")

if __name__ == "__main__":
    main()
