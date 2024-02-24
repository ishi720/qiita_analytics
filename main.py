#coding:utf-8
from flask import Flask, render_template
from get_qiita_myitem import get_qiita_myitem
import json

app = Flask(__name__)

qiita_data_str = get_qiita_myitem()
qiita_data = json.loads(qiita_data_str)

@app.route('/')
def index():
    return render_template('index.html', items=qiita_data)

if __name__ == '__main__':
    app.debug = True
    app.run()
