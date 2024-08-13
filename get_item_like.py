import requests
import json
import pandas as pd
import configparser

def get_item_like(item_id: str) -> str:
    """
    Qiita記事がいいねされた日付を集計する
    Args:
        item_id (str): 記事のID
    Returns:
        str: 指定されたQiitaの記事一覧
    """
    config = configparser.ConfigParser()
    config.read("config.cfg", 'UTF-8')
    bearer_token = config['QIITA']['BEARER_TOKEN']
    result = []
    per_page = 100

    # ページ件数を取得
    url = f"https://qiita.com/api/v2/items/{item_id}/"
    headers = {}
    params = {}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    r = requests.get(url, headers=headers, params=params)
    item_data = r.json()
    page_count = (int(item_data['likes_count']) + per_page - 1) // per_page
    item_title = item_data['title']

    # いいね数をカウント
    for page in range(1, page_count + 1):
        url = f"https://qiita.com/api/v2/items/{item_id}/likes"
        headers = {}
        params = {
            "page": page,
            "per_page": per_page
        }
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        r = requests.get(url, headers=headers, params=params)
        users = r.json()
        for user in users:
            result.append(user['created_at'])

    # 日付単位で集計
    dates = pd.to_datetime(result)
    dates = pd.Series(index=dates)
    dates = dates.to_period("D").index
    result_dict = dates.value_counts().sort_index().to_dict()
    result_dict = {str(key): value for key, value in result_dict.items()}
    return_data = {
        "title": item_title,
        "likes": result_dict
    }

    return json.dumps(return_data)
