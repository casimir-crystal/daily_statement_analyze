import os
import json
from datetime import datetime
from csv_analyze import table_export
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
logs_data = {}
logs_path = 'logs_data'
if not os.path.exists(logs_path):
    os.makedirs(logs_path)


@app.before_request
def before_request_func():
    today = datetime.today().strftime('%Y-%m-%d')
    logs_data['today'] = today
    logs_data['csv_filepath'] = os.path.join(logs_path, today+'.csv')
    logs_data['json_filepath'] = os.path.join(logs_path, today+'.json')


@app.route('/')
def index():
    if not os.path.exists(logs_data['csv_filepath']):
        return redirect(url_for('upload'))
    elif not os.path.exists(logs_data['json_filepath']):
        return redirect(url_for('information'))
    else:
        return redirect(url_for('result'))


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', date=logs_data['today'])
    elif request.method == 'POST':
        request.files['file'].save(logs_data['csv_filepath'])
        return redirect(url_for('index'))


@app.route('/information/', methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        return render_template('information.html', date=logs_data['today'])
    elif request.method == 'POST':
        req_dict = dict(request.form)
        result_dict = table_export(logs_data['csv_filepath'], req_dict)
        with open(logs_data['json_filepath'], 'w') as f:
            json.dump(result_dict, f)
        return redirect(url_for('index'))


@app.route('/result/')
def result():
    with open(logs_data['json_filepath']) as f:
        return render_template('result.html', data=json.load(f))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
