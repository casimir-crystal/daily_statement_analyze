import csv
from datetime import datetime


def table_export(csv_filename, form_dict, today=datetime.now()):
    """
    完整的table构建函数。接受由收银机生成并由用户上传的csv文件名为参数。
    """

    def float_or_int(s):
        if '.' in str(s):
            return round(float(s), 2)
        else:
            return int(s)

    # First, read the csv file into a dict as `data`
    with open(csv_filename, encoding="gbk") as f:
        reader = csv.DictReader(f)

        csv_dict = {}
        for row in reader:
            key = row.pop('收款方式')
            csv_dict[key] = row

    table_dict = {}
    weekday_table = ['一', '二', '三', '四', '五', '六', '日']

    table_dict['{}月'.format(today.month)] = str(today.day)
    table_dict['星期'] = weekday_table[today.weekday()]
    table_dict['天气'] = ''
    table_dict['营业额'] = None
    table_dict['GC'] = None
    table_dict['AC'] = None
    table_dict['累计营业额'] = ''
    table_dict['累计GC'] = ''
    table_dict['饿了么'] = ''
    table_dict['美团外卖'] = float_or_int(form_dict['meituan_turnover'])
    table_dict['线上合计'] = float_or_int(form_dict['meituan_turnover'])
    table_dict['线上GC'] = int(float(form_dict['meituan_sells']))
    table_dict['线上AC'] = float_or_int(table_dict['线上合计'] / table_dict['线上GC'])
    table_dict['现金'] = int(float(csv_dict['现金支付']['总金额(元)']))
    table_dict['微信'] = float_or_int(csv_dict['微信支付']['总金额(元)'])
    table_dict['支付宝'] = float_or_int(csv_dict['支付宝支付']['总金额(元)'])
    table_dict['口碑掌柜'] = float_or_int(form_dict['koubei_turnover'])
    table_dict['开店宝(美团)'] = float_or_int(form_dict['kaidianbao_turnover'])
    table_dict['银行App'] = ''
    table_dict['商场'] = ''
    table_dict['POS机GC'] = ''
    table_dict['POS机AC'] = ''
    table_dict['小程序'] = float_or_int(csv_dict['开个店支付']['总金额(元)'])
    table_dict['小程序GC'] = int(float(csv_dict['开个店支付']['单数']))
    table_dict['小程序AC'] = float_or_int(table_dict['小程序'] / table_dict['小程序GC'])
    table_dict['线下合计'] = table_dict['现金'] + table_dict['微信'] + table_dict['支付宝'] + table_dict['口碑掌柜'] + table_dict['开店宝(美团)'] + table_dict['小程序']
    table_dict['线下GC'] = sum(map(int, [csv_dict[key]['单数'] for key in ['现金支付', '微信支付', '支付宝支付', '开个店支付']])) + int(form_dict['kaidianbao_sells']) + int(form_dict['koubei_sells'])
    table_dict['线下AC'] = ''
    table_dict['储蓄卡/福利券'] = ''
    table_dict['签名'] = ''

    table_dict['营业额'] = table_dict['线上合计'] + table_dict['线下合计']
    table_dict['GC'] = table_dict['线上GC'] + table_dict['线下GC']
    table_dict['AC'] = float_or_int(table_dict['营业额'] / table_dict['GC'])

    return table_dict
