import os
import sys
import json
from datetime import datetime, timedelta

logs_path = 'saved_logs'
yesterday = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
last_json_file = os.path.join(logs_path, yesterday+'.json')

if not os.path.exists(logs_path):
    os.mkdir(logs_path)

if os.path.exists(last_json_file):
    with open(last_json_file) as f:
        working_json_dict = json.load(f)
else:
    working_json_dict = {}

if working_json_dict.get('累计营业额'):
    print('已存在昨日的累计营业额，是否仍需更改？\n')
    print('昨日累计营业额：', working_json_dict['累计营业额'])
    print('昨日累计GC：', working_json_dict['累计GC'])
    confirm = input('输入 Y/y:')

    if confirm not in 'Yy':
        print('操作取消')
        sys.exit(0)

working_json_dict['累计营业额'] = float(input('输入累计营业额：'))
working_json_dict['累计GC'] = int(input('输入累计GC：'))

with open(last_json_file, 'w') as f:
    working_json_dict = json.dump(working_json_dict, f)
