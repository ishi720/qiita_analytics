from flask import Flask, request, render_template
from get_qiita_myitem import get_qiita_myitem
import json

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

@app.route('/', methods=['GET', 'POST'])
def index():

    user_name = ''

    if request.method == 'POST':
        user_name = request.form.get('search', '')

    qiita_data_str = get_qiita_myitem(app.config['QIITA_BEARER_TOKEN'], user_name)
    qiita_data = json.loads(qiita_data_str)

    return render_template('index.html', items=qiita_data)


if __name__ == '__main__':
    app.debug = True
    app.run()
