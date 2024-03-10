from flask import Flask, request, render_template
from get_qiita_myitem import get_qiita_myitem
from get_item_like import get_item_like
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():

    user_name = request.args.get('search', '')

    qiita_data_str = get_qiita_myitem(user_name)
    qiita_data = json.loads(qiita_data_str)

    return render_template('index.html', items=qiita_data, user_name=user_name)

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')


@app.route('/api/get_item_like', methods=['GET'])
def api_get_item_like ():
    return get_item_like(request.args.get('item_id'))

if __name__ == '__main__':
    app.debug = True
    app.run()
