import requests
import json
import pandas as pd
import configparser

def get_item_like(item_id: str) -> str:
    """
    Qiitaから記事の一覧を取得する
    Args:
        bearer_token (str): Qiitaアクセストークン
        item_id (str): 記事のID
    Returns:
        str: 指定されたQiitaの記事一覧
    """
    config = configparser.ConfigParser()
    config.read("config.cfg", 'UTF-8')
    bearer_token = config['QIITA']['BEARER_TOKEN']
    result = []

    url = f"https://qiita.com/api/v2/items/{item_id}/likes"
    headers = {}
    params = {
        "per_page": 100,
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

    return json.dumps(result_dict)

