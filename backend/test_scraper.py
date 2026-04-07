import requests
from bs4 import BeautifulSoup

def test():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36',
    }
    
    url = "https://dir.indiamart.com/search.mp?ss=laptop"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print("IndiaMART Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        names = soup.select('.cardlinks')
        prices = soup.select('.prc')
        
        print("Found names:", len(names), "prices:", len(prices))
        for i in range(min(5, len(names), len(prices))):
            print(names[i].text.strip()[:40], " | ", prices[i].text.strip())
            
    except Exception as e:
        print("Error:", e)

test()
