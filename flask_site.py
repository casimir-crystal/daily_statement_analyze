import os
import json
from datetime import datetime, timedelta
from csv_analyze import table_export
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
date = {}  # 定义一个全局字典，用来在每次请求页面时刷新当日的日期
logs_path = 'saved_logs'  # 数据保存的文件夹名称

if not os.path.exists(logs_path):
    os.makedirs(logs_path)  # 如果当前路径不存在该文件夹则创建


def get_filepath(date, file_suffix):
    """构造文件路径(filepath)的函数
    输入格式化后的日期字符串YYYY-MM-DD，和后缀名.csv或.json，
    返回字符串(str)"""
    return os.path.join(logs_path, '{date}.{file_suffix}'.format(
        date=date, file_suffix=file_suffix
    ))


@app.before_request
def before_request_func():
    # 每个请求都运行一次，确保日期准确
    today = datetime.today()
    date['today'] = today.strftime('%Y-%m-%d')  # YYYY-MM-DD, 2020-08-20 for example
    date['yesterday'] = (today - timedelta(1)).strftime('%Y-%m-%d')


@app.route('/')
def index():
    # 如果不存在.csv文件，则请求上传
    # 如果不存在所需数据.json文件，则请求额外的信息来生成
    # 如果以上文件都有，则直接返回结果
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
        # 保存上传的文件为 saved_logs/2020-08-20.csv
        request.files['file'].save(get_filepath(date['today'], 'csv'))
        return redirect(url_for('index'))


@app.route('/information/', methods=['GET', 'POST'])
def information():
    if request.method == 'GET':
        return render_template('information.html', date=date['today'])
    elif request.method == 'POST':
        req_dict = dict(request.form)  # 首先获取表单提交的信息，转换为dict
        if os.path.exists(get_filepath(date['yesterday'], 'json')):
            # 如果存在昨日数据，则直接提取昨日的总营业额传入`table_export`
            # TODO: 如果不存在，则要求用户主动输入
            result_dict = table_export(get_filepath(date['today'], 'csv'),
                                       get_filepath(date['yesterday'], 'json'), req_dict)
        else:
            # 如果不存在，则直接抛给`table_export`处理
            result_dict = table_export(get_filepath(date['today'], 'csv'), req_dict)

        # 将返回结果转换为json，以日期命名保存为json文件
        with open(get_filepath(date['today'], 'json'), 'w') as f:
            json.dump(result_dict, f)

        return redirect(url_for('result'))  # 直接重定向至result;


@app.route('/result/')
def result():
    # 获取当日日期的数据，通过`render_template`转换为表格
    with open(get_filepath(date['today'], 'json')) as f:
        return render_template('result.html', data=json.load(f))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
