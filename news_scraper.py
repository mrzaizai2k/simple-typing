import requests
from bs4 import BeautifulSoup
from typing import Literal

class NewsScraper:
    '''
    Scrape news from vnexpress.net (Vietnamese) or e.vnexpress.net (English)
    '''
    def __init__(self):
        pass

    def take_text_from_link(self, url: str, mode: Literal['vi', 'en'] = 'vi') -> str:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if mode == 'vi':
                content_div = soup.find('article', class_='fck_detail')
                if content_div:
                    return ' '.join([p.text.strip() for p in content_div.find_all('p')])
            else:  # English mode
                content_div = soup.find('div', class_='fck_detail')
                if content_div:
                    return ' '.join([p.text.strip() for p in content_div.find_all('p', class_='Normal')])
            return ""
        except Exception as e:
            print(f"Error fetching content from {url}: {str(e)}")
            return ""

    def fetch_news(self, mode: Literal['vi', 'en'] = 'vi') -> list:
        url = "https://vnexpress.net/" if mode == 'vi' else "https://e.vnexpress.net/"
        news_items = []

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            if mode == 'vi':
                articles = soup.find_all('a', class_='thumb thumb-5x3')
                for article in articles:
                    article_url = article.get('href')
                    title = article.get('title', '').strip()
                    if article_url and 'eclick' not in article_url:
                        news_items.append({
                            'url': article_url,
                            'title': title,
                            'description': '',
                            'content': self.take_text_from_link(article_url, mode='vi')
                        })

            else:  # English mode
                articles = soup.find_all('div', class_='block_folder row')
                for article in articles:
                    link = article.find('a', class_='thumb_news_site thumb_5x3')
                    article_url = link.get('href') if link else None
                    title = link.get('title', '').strip() if link else ''
                    description = article.find('div', class_='lead_news_site').text.strip() if article.find('div', class_='lead_news_site') else ''
                    if article_url and 'eclick' not in article_url:
                        news_items.append({
                            'url': article_url,
                            'title': title,
                            'description': description,
                            'content': self.take_text_from_link(article_url, mode='en')
                        })

        except Exception as e:
            print(f"Error fetching news from {url}: {str(e)}")

        return news_items

if __name__ == "__main__":
    scraper = NewsScraper()
    results = scraper.fetch_news(mode='vi')  # or 'vi' for Vietnamese
    print("len(results)", len(results))
    print("results", results[0].keys())
    for news in results[:2]:
        print(news)