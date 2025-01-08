import requests

# API URL for fetching news
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(company_name, api_key, max_articles=3):
    """
    Fetch the latest news articles for a given company.
    
    Args:
        company_name (str): Name of the company to search for.
        api_key (str): API key for News API.
        max_articles (int): Maximum number of articles to fetch.

    Returns:
        list: A list of dictionaries containing news articles.
    """
    params = {
        "q": company_name,
        "pageSize": max_articles,
        "apiKey": api_key,
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    articles = response.json().get("articles", [])
    
    # Simplify article structure
    simplified_articles = [
        {
            "title": article.get("title"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name"),
        }
        for article in articles
    ]
    
    return simplified_articles
