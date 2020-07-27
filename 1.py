class NumbericDict(dict):
    def __setitem__(self, key, value):
        try:
            value = float(value)
            if int(value) == value:
                value = int(value)
            else:
                # value = value // 0.01 / 100  # 保留两位小数
                # value = round(value, 2)  # 四舍五入，奇进偶舍：https://www.cnblogs.com/xieqiankun/p/the_truth_of_round.html
                value = Decimal(str(value)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)  # 通常的四舍五入
        except (ValueError, TypeError):
            # it's not a number, that's fine
            pass
        finally:
            self.data[key] = value
