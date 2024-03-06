from flask import request, jsonify
import requests

def get_qiita_myitem_api(user_name, app):
    # user_name = request.args.get('user_name')
    bearer_token = app.config.get('QIITA_BEARER_TOKEN')

    # if not bearer_token or not user_name:
    #     return jsonify({'error': 'Bearerトークンとユーザー名が必要です'}), 400

    url = "https://qiita.com/api/v2/items"
    headers = {}
    params = {
        "query": f"user:{user_name}",
        "per_page": 50,
        "page": 1
    }
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
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

        # return jsonify(result)
        return result
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Qiita APIへのリクエストが失敗しました: {str(e)}'}), 500