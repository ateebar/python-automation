import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    # Nümunə olaraq sitat yayan sadə test saytından məlumat çəkək
    url = "http://quotes.toscrape.com/"
    
    print(f"Məlumat çəkilir: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('span', class_='text')
        
        print("\n--- Əldə edilən ilk 5 sitat ---")
        for i, quote in enumerate(quotes[:5], 1):
            print(f"{i}. {quote.get_text()}")
    else:
        print("Səhifəyə qoşulmaq mümkün olmadı:", response.status_code)

if __name__ == "__main__":
    scrape_quotes()
