import requests
import json

def get_qiita_myitem(bearer_token: str, user_name: str) -> str:

    url = "https://qiita.com/api/v2/items"
    headers = {}
    params = {
        "query": f"user:{user_name}",
        "per_page": 50,
        "page": 1
    }

    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    r = requests.get(url, headers=headers, params=params)

    items = r.json()

    result = []

    for item in items:
        page_data = {
            'title': item['title'],
            'url': item['url'],
            'likes_count': item['likes_count'],
            'stocks_count': item['stocks_count'],
            'page_views_count': item['page_views_count'],
            'updated_at': item['updated_at']
        }
        result.append(page_data)

    return json.dumps(result, indent=2, ensure_ascii=False)
