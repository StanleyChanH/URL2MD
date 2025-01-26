import requests

def fetch_html(url: str) -> str:
    """
    获取网页HTML内容
    :param url: 目标网页URL
    :return: 网页HTML内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    try:
        response = session.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"<html><body>Error fetching URL: {str(e)}</body></html>"