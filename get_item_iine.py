import requests
import json

def get_item_iine(bearer_token: str, item_id: str) -> str:
    """
    Qiitaから記事の一覧を取得する
    Args:
        bearer_token (str): Qiitaアクセストークン
        user_name (str): Qiitaのアカウント名
    Returns:
        str: 指定されたQiitaの記事一覧
    """
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
        data = {
            'created_at': user['created_at'],
        }
        result.append(data)

    # TODO created_atを日付単位で集計する

    return json.dumps(result, indent=2, ensure_ascii=False)
