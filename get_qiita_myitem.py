import requests
import json
import configparser

def get_qiita_myitem(user_name: str) -> str:
    """
    Qiitaから記事の一覧を取得する
    Args:
        user_name (str): Qiitaのアカウント名
    Returns:
        str: 指定されたQiitaの記事一覧
    """
    config = configparser.ConfigParser()
    config.read("config.cfg", 'UTF-8')
    bearer_token = config['QIITA']['BEARER_TOKEN']
    result = []

    if user_name == "":
        return json.dumps(result, indent=2, ensure_ascii=False)

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

    for item in items:
        if item['private'] == False:
            page_data = {
                'title': item['title'],
                'id': item['id'],
                'url': item['url'],
                'likes_count': item['likes_count'],
                'stocks_count': item['stocks_count'],
                'page_views_count': item['page_views_count'],
                'updated_at': item['updated_at']
            }
            result.append(page_data)

    return json.dumps(result, indent=2, ensure_ascii=False)
