import csv
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from collections import UserDict


class NumbericDict(UserDict):
    def __setitem__(self, key, value):
        try:
            value = float(value)
            if int(value) == value:
                value = int(value)
            else:
                # value = value // 0.01 / 100  # 保留两位小数
                # value = round(value, 2)  # 四舍五入，奇进偶舍：https://www.cnblogs.com/xieqiankun/p/the_truth_of_round.html
                value = float(Decimal(str(value)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))  # 通常的四舍五入
        except (ValueError, TypeError):
            # it's not a number, that's fine
            pass
        finally:
            self.data[key] = value


def table_export(csv_filename, form_dict, today=datetime.now(), last_result=None):
    """
    完整的table构建函数。接受由收银机生成并由用户上传的csv文件名为参数。
    """

    with open(csv_filename, encoding="gbk") as f:
        reader = csv.DictReader(f)

        csv_dict = {}
        for row in reader:
            key = row.pop('收款方式')
            csv_dict[key] = row

    table_dict = NumbericDict()
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
    table_dict['美团外卖'] = form_dict['meituan_turnover']
    table_dict['线上合计'] = form_dict['meituan_turnover']
    table_dict['线上GC'] = form_dict['meituan_sells']
    table_dict['线上AC'] = table_dict['线上合计'] / table_dict['线上GC']
    table_dict['现金'] = csv_dict['现金支付']['总金额(元)']
    table_dict['微信'] = csv_dict['微信支付']['总金额(元)']
    table_dict['支付宝'] = csv_dict['支付宝支付']['总金额(元)']
    table_dict['口碑掌柜'] = form_dict['koubei_turnover']
    table_dict['开店宝(美团)'] = form_dict['kaidianbao_turnover']
    table_dict['银行App'] = ''
    table_dict['商场'] = ''
    table_dict['POS机GC'] = ''
    table_dict['POS机AC'] = ''
    table_dict['小程序'] = form_dict['xiaochengxu_turnover']
    table_dict['小程序GC'] = form_dict['xiaochengxu_sells']
    table_dict['小程序AC'] = table_dict['小程序'] / table_dict['小程序GC']
    table_dict['线下合计'] = table_dict['现金'] + table_dict['微信'] + table_dict['支付宝'] + table_dict['口碑掌柜'] + table_dict['开店宝(美团)'] + table_dict['小程序']
    table_dict['线下GC'] = sum(map(int, [csv_dict[key]['单数'] for key in ['现金支付', '微信支付', '支付宝支付']])) + int(form_dict['xiaochengxu_sells'])
    table_dict['线下AC'] = table_dict['线下合计'] / table_dict['线下GC']
    table_dict['储蓄卡/福利券'] = csv_dict['会员卡支付']['总金额(元)']
    table_dict['签名'] = ''

    table_dict['营业额'] = table_dict['线上合计'] + table_dict['线下合计']
    table_dict['GC'] = table_dict['线上GC'] + table_dict['线下GC']
    table_dict['AC'] = table_dict['营业额'] / table_dict['GC']

    # 检查 `last_result` 是否传入，再检查有无‘累计营业额’键且非空
    if last_result and last_result.get('累计营业额'):
        table_dict['累计营业额'] = table_dict['营业额'] + float(last_result['累计营业额'])
        table_dict['累计GC'] = table_dict['GC'] + int(last_result['累计GC'])
    elif form_dict.get('yesterday_all_turnover') and form_dict.get('yesterday_all_gc'):
        table_dict['累计营业额'] = table_dict['营业额'] + float(form_dict['yesterday_all_turnover'])
        table_dict['累计GC'] = table_dict['GC'] + int(form_dict['yesterday_all_gc'])

    return dict(table_dict)  # 返回标准dict对象
