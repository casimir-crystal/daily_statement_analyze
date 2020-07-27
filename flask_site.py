import os
import json
from datetime import datetime, timedelta
from csv_analyze import table_export
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
date = {}
logs_path = 'saved_logs'

if not os.path.exists(logs_path):
    os.makedirs(logs_path)


def get_filepath(date, file_suffix):
    return os.path.join(logs_path, '{date}.{file_suffix}'.format(
        date=date, file_suffix=file_suffix
    ))


@app.before_request
def before_request_func():
    date['today'] = datetime.today().strftime('%Y-%m-%d')
    date['yesterday'] = datetime.today() - timedelta(1) .strftime('%Y-%m-%d')


@app.route('/')
def index():
    if not os.path.exists(get_filepath(date['today'], 'csv')):
        return redirect(url_for('upload'))
    elif not os.path.exists(get_filepath(date['today'], 'json')):
        return redirect(url_for('information'))
    else:
        return redirect(url_for('result'))


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', date=date['today'])
    elif request.method == 'POST':
        request.files['file'].save(get_filepath(date['today'], 'csv'))
        return redirect(url_for('index'))


@app.route('/information/', methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        return render_template('information.html', date=date['today'])
    elif request.method == 'POST':
        req_dict = dict(request.form)
        if os.path.exists(get_filepath(date['yesterday'], 'json')):
            result_dict = table_export(get_filepath(date['today'], 'csv'),
                                       get_filepath(date['yesterday'], json), req_dict)
        else:
            result_dict = table_export(get_filepath(date['today'], 'csv'), req_dict)

        with open(get_filepath(logs_path, date['today'], 'json'), 'w') as f:
            json.dump(result_dict, f)
        return redirect(url_for('index'))


@app.route('/result/')
def result():
    with open(date['json_filepath']) as f:
        return render_template('result.html', data=json.load(f))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
