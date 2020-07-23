import json
from os import path
from datetime import datetime
from csv_analyze import table_export
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
data_file = {}


@app.before_request
def before_request_func():
    today = datetime.today().strftime('%Y-%m-%d')
    data_file['today'] = today
    data_file['csv_filename'] = today+'.csv'
    data_file['csv_filepath'] = path.join('data_files',
                                          data_file['csv_filename'])
    data_file['json_filename'] = today+'.json'
    data_file['json_filepath'] = path.join('data_files',
                                           data_file['json_filename'])


@app.route('/')
def index():
    if not path.exists(data_file['csv_filepath']):
        return redirect(url_for('upload'))
    elif not path.exists(data_file['json_filepath']):
        return redirect(url_for('information'))
    else:
        return redirect(url_for('result'))


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html', date=data_file['today'])
    elif request.method == 'POST':
        request.files['file'].save(data_file['csv_filepath'])
        return redirect(url_for('index'))


@app.route('/information/', methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        return render_template('information.html', date=data_file['today'])
    elif request.method == 'POST':
        req_dict = dict(request.form)
        result_dict = table_export(data_file['csv_filepath'], req_dict)
        with open(data_file['json_filepath'], 'w') as f:
            json.dump(result_dict, f)
        return redirect(url_for('index'))


@app.route('/result/')
def result():
    with open(data_file['json_filepath']) as f:
        return render_template('result.html', data=json.load(f))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
