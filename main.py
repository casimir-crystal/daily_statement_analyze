# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime

# First, read the csv file into a dict as `data`
csv_file = "test.csv"
df = pd.read_csv(csv_file, encoding="gbk")

# to get rid of the last column
data = df[df.columns[:-1]]
data.columns = df.columns[1:]


table_dict = {}
today = datetime.now()
weekday_table = ['一', '二', '三', '四', '五', '六', '日']
temp = 'temp_value'  # just for testing now
input_value = 'input_value'  # just for testing now

table_dict['{}月'.format(today.month)] = str(today.day)
table_dict['星期'] = weekday_table[today.weekday()]
table_dict['天气'] = None
table_dict['营业额'] = temp
table_dict['GC'] = temp
table_dict['AC'] = temp
table_dict['累计营业额'] = temp
table_dict['累计GC'] = temp
table_dict['饿了么'] = None
table_dict['美团外卖'] = input_value
table_dict['线上合计'] = None
table_dict['线上GC'] = None
table_dict['线上AC'] = None
table_dict['现金'] = input_value
table_dict['微信'] = temp
table_dict['支付宝'] = temp
table_dict['口碑掌柜'] = input_value
table_dict['开店宝(美团)'] = input_value
table_dict['银行App'] = None
table_dict['商场'] = None
table_dict['POS机GC'] = None
table_dict['POS机AC'] = None
table_dict['小程序'] = temp
table_dict['小程序GC'] = None
table_dict['小程序AC'] = None
table_dict['线下合计'] = None
table_dict['线下GC'] = None
table_dict['线下AC'] = None
table_dict['储蓄卡/福利券'] = None
table_dict['签名'] = None

df = pd.DataFrame([table_dict])
print(df.to_html(classes=['table', 'table-striped'], index=False))
