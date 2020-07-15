import pandas as pd
from datetime import datetime

# First, read the csv file into a dict as `data`
csv_file = "test.csv"
df = pd.read_csv(csv_file, encoding="gbk")

# to get rid of the last column
data = df[df.columns[:-1]]
data.columns = df.columns[1:]
# print(df.to_html(classes=['table', 'table-striped']))


table_dict = {}
today = datetime.now()
weekday_table = ['一', '二', '三', '四', '五', '六', '日']

table_dict["month"] = {'{}月'.format(today.month): str(today.day)}
table_dict["weekday"] = {'星期': weekday_table[today.weekday()]}
table_dict["wether"] = {'天气': None}
var = 10 # just for testing now
table_dict["all"] = {'营业额': var}
