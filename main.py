from flask import Flask, request, render_template
from get_qiita_myitem import get_qiita_myitem
from get_item_iine import get_item_iine
import json

app = Flask(__name__)

# app.config.from_pyfile('config.cfg')

@app.route('/', methods=['GET'])
def index():

    user_name = ''

    user_name = request.args.get('search', '')

    qiita_data_str = get_qiita_myitem(user_name)
    qiita_data = json.loads(qiita_data_str)

    return render_template('index.html', items=qiita_data, user_name=user_name)

@app.route('/analytics', methods=['GET'])
def analytics():

    item_id = request.args.get('item_id', '')
    iine_date = get_item_iine(item_id)
    qiita_data = json.loads(iine_date)
    return render_template('analytics.html', iine_date=qiita_data)


if __name__ == '__main__':
    app.debug = True
    app.run()
