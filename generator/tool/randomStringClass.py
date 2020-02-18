# -*- coding: utf-8 -*-
# @Date : 2019-8-28
# @Author : water
# @Desc  :实现传入字符类型与长度，返回固定长度的字符
# @Version : v1.0
# 20191120--增加Decimal来处理大整数与浮点数相加时候，小数点后面直接舍去
#

import random,math,string,os,time
import logging,configparser
from decimal import Decimal
#from logSetClass import Log

# 实现不同字段类型的路由功能
TYPES_DICT = dict()

class GetString:

    # 初始化并加载所有的类型的全部strings
    def __init__(self,logger=None):
        CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config","case_generator.ini")
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"config")
        chinese_path = os.path.join(self.data_path, 'chinese.config')
        fanti_path = os.path.join(self.data_path, 'fanti.config')
        nanti_path = os.path.join(self.data_path, 'nanti.config')
        # 加载generator.ini中datetime_format
        config = configparser.RawConfigParser()
        config.read(CONFIG_FILE,encoding="utf-8")  # 读取文件
        self.datetime_format = config.get("template", "datetime_format")
        # 加载generator.ini中chinese_len
        self.ch_len = int(config.get("template", "chinese_len"))
        # 日志配置
        if logger:
            self.logger = logger
        else:
            logging.basicConfig(level=10, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)

        #  定义变量存放类型及对应函数
        self.types_dict = dict()

        """
        20191012单独在每个文件中配置一份，会出现重复打印的问题
        log_name = "generator.log"
        log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', log_name)
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        """
        """
        单独日志配置于20191012替换，由于只能打印到控制台，无法输出到文件中
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        """
        # 加载常用汉字
        f1 = open(chinese_path, 'r', encoding='UTF-8')
        self.chineses = f1.readline().replace(' ','')
        # self.logger.debug(self.chineses[:10])
        self.logger.debug("chinese is ok")
        f1.close()
        # 加载常用繁体字
        f2 = open(fanti_path, 'r', encoding='UTF-8')
        self.fantis = f2.readline()
        # self.logger.debug(self.fantis[1:2])
        self.logger.debug("fantizi is ok")
        f2.close()
        #加载常用难检字
        f3 = open(nanti_path, 'r', encoding='UTF-8')
        self.nantis = f3.readline()
        # self.logger.debug(self.nantis[1:10])
        self.logger.debug("nantizi is ok")
        f3.close()
        #加载数字
        self.numbers = string.digits
        # self.logger.debug(self.numbers)
        self.logger.debug("number is ok")
        #加载全角数字
        self.qj_numbers = "０１２３４５６７８９"
        # self.logger.debug(self.qj_numbers)
        self.logger.debug("quanjiao number is ok")
        #加载小写字母
        self.lower_alphabet = string.ascii_lowercase
        # self.logger.debug(self.lower_alphabet)
        self.logger.debug("lower alphabet is ok")
        #加载大写字母
        self.upper_alphabet = string.ascii_uppercase
        # self.logger.debug(self.upper_alphabet)
        self.logger.debug("upper alphabet is ok")
        #加载大小写字母
        self.all_alphabet = string.ascii_letters
        # self.logger.debug(self.all_alphabet)
        self.logger.debug("all alphabet is ok")
        #加载特殊特号
        remove_symbols = ["'",'"','@','#']
        self.symbols = string.punctuation
        for s in remove_symbols:
            self.symbols = self.symbols.replace(s,"")
        self.logger.debug(self.symbols)
        self.logger.debug("symbol is ok")


    @staticmethod
    def _random_count(sort,length):
        """
        根据传入的sort列表中数据类型及总长度length，生成sort中每种数据类型的长度，合计长度 = length
        :param length:
        :return:
        """
        if length == len(sort):
            sort_count = dict()
            for i in range(len(sort)):
                sort_count[sort[i]] = 1
            return sort_count
        else:
            while True:
                sort_count = dict()
                for i in range(len(sort) - 1):
                    sort_count[sort[i]] = random.randint(1, length - len(sort))
                sort_count[sort[len(sort) - 1]] = length - sum(sort_count.values())
                if sort_count[sort[len(sort) - 1]] > 1:
                    break
            return sort_count


    def _random_string_multiple(self,sort,length):
        """
        按length与类型生成相应长度的string
        :param sort:输入的待测试字段的类型
        :param length:输入的待测试字段的长度
        :return:
        """
        sort_count = self._random_count(sort,length)
        self.logger.debug(sort_count)
        # 添加数字
        result = random.choices(self.numbers,k=sort_count.get('SZ',0))
        # 添加大写字母
        result.extend(random.choices(self.upper_alphabet,k=sort_count.get('ZMD',0)))
        # 添加小写字母
        result.extend(random.choices(self.lower_alphabet,k=sort_count.get('ZMX',0)))
        # 添加汉字
        result.extend(random.choices(self.chineses,k=sort_count.get('HZ',0)))
        # 添加难体
        result.extend(random.choices(self.nantis,k=sort_count.get('NT',0)))
        # 添加繁体
        result.extend(random.choices(self.fantis,k=sort_count.get('FT',0)))
        # 添加特殊符号
        result.extend(random.choices(self.symbols, k=sort_count.get('FH', 0)))
        # 添加全角数字
        result.extend(random.choices(self.qj_numbers, k=sort_count.get('QJSZ', 0)))
        # 打乱顺序
        random.shuffle(result)
        results = "".join(result)
        return results

    @staticmethod
    def _random_int_and_double(ninteger=1,ndigit=0):
        """
        按位置生成小数、浮点类型
        不能使用round函数，因为会转为-1.6029630240618248e+18类型
        "%.2f"不会损失小数，但是float类型会自动将较长的小数进行科学计数，此时会损失小数部分
        :param ninteger:整数位数
        :param ndigit:小数位数
        :return:
        """
        results = Decimal(random.randint(1,10**ninteger))
        if ndigit != 0:
            results = results/(10**ndigit)
        return str(results)

    def _random_datetime(self,start_year,end_year):
        """
        生成此期间随机日期："2019-08-11 14:17:39"
        :param start_year:
        :param end_year:
        :return:
        """
        a1 = (start_year, 1, 1, 0, 0, 0, 0, 0, 0)
        a2 = (end_year, 12, 31, 23, 59, 59, 0, 0, 0)
        start = time.mktime(a1)
        end = time.mktime(a2)
        t = random.randint(start, end)
        date_tuple = time.localtime(t)
        # result = time.strftime(self.datetime_format, date_tuple)
        return date_tuple


    def type_route(attr_type):
        def f1(func):
            TYPES_DICT[attr_type] = func
            def f2():
                return func()
            return f2
        return f1

    @type_route("VARCHAR")
    def _varchar_case(self,length,ndigit=0):
        """
        生成VARCHAR的通用测试用例
        :param length:
        :return:
        """
        length = int(length)
        results = list()
        # 1.生成length位的数字
        results.append([f"生成{length}位的数字T", self._random_string_multiple(['SZ'], length)])
        # 2.生成length+1位的数字
        results.append([f"生成{length+1}位的数字F", self._random_string_multiple(['SZ'], length + 1)])
        # 3.生成length位的数字（两边有空格）
        results.append([f"生成{length}位的数字（两边有空格）T", "   " + self._random_string_multiple(['SZ'], length) + "  "])
        # 4.生成length位的数字（中间有空格）
        result = self._random_string_multiple(['SZ'], length)
        results.append([f"生成{length}位的数字（中间有空格）F",result[:math.floor(length / 2)] + "   " + result[math.floor(length / 2):length]])
        # 5.生成length位的大写字母
        results.append([f"生成{length}位的大写字母T", self._random_string_multiple(['ZMD'], length)])
        # 6.生成length+1位的大写字母
        results.append([f"生成{length+1}位的大写字母F", self._random_string_multiple(['ZMD'], length + 1)])
        # 7.生成length位的小写字母
        results.append([f"生成{length}位的小写字母T", self._random_string_multiple(['ZMX'], length)])
        # 8.生成length+1位的小写字母
        results.append([f"生成{length+1}位的小写字母F", self._random_string_multiple(['ZMX'], length + 1)])
        # 9.生成length位的小写字母、数字
        if length >= 2:
            results.append([f"生成{length}位的小写字母、数字T", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 10.生成length+1位的小写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length + 1)])
        # 11.生成length位大写字母、数字
        if length >= 2:
            results.append([f"生成{length}位大写字母、数字T", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 12.生成length+1位大写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length + 1)])
        # 13.生成length位大小写字母、数字
        if length >= 3:
            results.append([f"生成{length}位大小写字母、数字T", self._random_string_multiple(['ZMD', 'ZMX', 'SZ'], length)])
        # 14.生成length位全角数字
        # results.append([f"生成{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 15.生成length位大小写字母
        if length >= 2:
            results.append([f"生成{length}位大小写字母T", self._random_string_multiple(['ZMD', 'ZMX'], length)])
        # 16.生成length位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的汉字T", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的汉字T", self._random_string_multiple(['HZ'], length)])
        # 17.生成length+1位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)+1}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len) + 1)])
        else:
            results.append([f"生成{length+1}位的汉字F", self._random_string_multiple(['HZ'], length + 1)])
        # 18.生成length位的繁体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的繁体字T", self._random_string_multiple(['FT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的繁体字T", self._random_string_multiple(['FT'], length)])
        # 19.生成length位的难体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的难体字T", self._random_string_multiple(['NT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的难体字T", self._random_string_multiple(['NT'], length)])
        # 20.生成length位的特殊符号
        results.append([f"生成{length}位的特殊符号T", self._random_string_multiple(['FH'], length)])
        # 21.生成空值
        results.append(["生成空值F", ''])
        # 22.生成null值
        results.append(["生成null值F", None])
        # 23.sql注入 'or'1'='1
        results.append(["sql注入1T", self._random_string_multiple(['SZ'], length) + "'' or ''1''=''1"])
        # 24.sql注入'
        results.append(["sql注入2T", "''"])
        # 25.生成length-1位的数字
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的数字T", self._random_string_multiple(['SZ'], length - 1)])
        # 26.生成length-1位的大写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的大写字母F", self._random_string_multiple(['ZMD'], length - 1)])
        # 27.生成length-1位的小写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的小写字母F", self._random_string_multiple(['ZMX'], length - 1)])
        # 28.删除此节点
        results.append(["删除报文中此节点F",'DEL'])
        self.logger.info(results)
        return results

    @type_route("CHAR")
    def _char_case(self,length,ndigit=0):
        """
        生成INT的通用测试用例
        :return:
        """
        length = int(length)
        results = list()
        # 1生成length位的数字
        results.append([f"生成{length}位的数字T", self._random_string_multiple(['SZ'], length)])
        # 2生成length+1位的数字
        results.append([f"生成{length+1}位的数字F", self._random_string_multiple(['SZ'], length + 1)])
        # 3生成length位的数字（两边有空格）
        results.append([f"生成{length}位的数字（两边有空格）F", "   " + self._random_string_multiple(['SZ'], length) + "  "])
        # 4生成length位的数字（中间有空格）
        # result = self._random_string_multiple(['SZ'], length)
        # results.append([f"生成{length}位的数字（中间有空格）F",result[:math.floor(length / 2)] + "   " + result[math.floor(length / 2):length]])
        # 5生成length位的大写字母
        results.append([f"生成{length}位的大写字母T", self._random_string_multiple(['ZMD'], length)])
        # 6生成length+1位的大写字母
        results.append([f"生成{length+1}位的大写字母F", self._random_string_multiple(['ZMD'], length + 1)])
        # 7生成length位的小写字母
        results.append([f"生成{length}位的小写字母F", self._random_string_multiple(['ZMX'], length)])
        # 8生成length+1位的小写字母
        results.append([f"生成{length+1}位的小写字母F", self._random_string_multiple(['ZMX'], length + 1)])
        # 9生成length位的小写字母、数字
        if length >= 2:
            results.append([f"生成{length}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 10生成length+1位的小写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length + 1)])
        # 11生成length位大写字母、数字
        if length >= 2:
            results.append([f"生成{length}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 12生成length+1位大写字母、数字
        if length + 1 >= 2:
            results.append([f"生成{length+1}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length + 1)])
        # 13生成length位大小写字母、数字
        if length >= 3:
            results.append([f"生成{length}位大小写字母、数字F", self._random_string_multiple(['ZMD', 'ZMX', 'SZ'], length)])
        # 14生成length位全角数字
        results.append([f"生成{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 15生成length位大小写字母
        if length >= 2:
            results.append([f"生成{length}位大小写字母F", self._random_string_multiple(['ZMD', 'ZMX'], length)])
        # 16生成length位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的汉字F", self._random_string_multiple(['HZ'], length)])
        # 17生成length+1位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)+1}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len) + 1)])
        else:
            results.append([f"生成{length+1}位的汉字F", self._random_string_multiple(['HZ'], length + 1)])
        # # 18生成length位的繁体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的繁体字F", self._random_string_multiple(['FT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的繁体字F", self._random_string_multiple(['FT'], length)])
        # # 19生成length位的难体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的难体字F", self._random_string_multiple(['NT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的难体字F", self._random_string_multiple(['NT'], length)])
        # 20生成length位的特殊符号
        results.append([f"生成{length}位的特殊符号F", self._random_string_multiple(['FH'], length)])
        # 21生成空值
        results.append(["生成空值F", ''])
        # 22生成null值
        results.append(["生成null值F", None])
        # 23sql注入 'or '1'='1
        results.append(["sql注入1F", self._random_string_multiple(['SZ'], length) + "'' or ''1''=''1"])
        # 24.sql注入'
        results.append(["sql注入2F", "''"])
        # 25.超长位数数字
        results.append([f"生成超长位数数字T", self._random_string_multiple(['SZ'], length + length)])
        # 26.值为0
        # results.append([f"值为0T", '0'])
        # 27.值为1
        # results.append([f"值为1T", '1'])
        # 28.值为2
        # if length == 1:  # 20200110通过传入固定值来代替
            # results.append([f"值为2T", '2'])
        # 29.值为3
        # if length == 1:
            # results.append([f"值为3", '3'])
        # 30.值为4
        # if length == 1:
            # results.append([f"值为4", '4'])
        # 31.值为5
        # if length == 1:
            # results.append([f"值为5", '5'])
        # 32.生成length-1位的数字
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的数字F", self._random_string_multiple(['SZ'], length - 1)])
        # 33.生成length-1位的大写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的大写字母F", self._random_string_multiple(['ZMD'], length - 1)])
        # 34.生成length-1位的小写字母
        if length - 1 >= 1:
            results.append([f"生成{length-1}位的小写字母F", self._random_string_multiple(['ZMX'], length - 1)])
        # 35.删除此节点
        results.append(["删除报文中此节点F",'DEL'])
        self.logger.debug(results)
        return results

    @type_route("DATETIME")
    def _datetime_case(self,length=19,ndigit=0):
        """
        生成DATETIME的通用测试用例
        :param length: "2019-08-11 14:17:39"共19位
        :return:
        """
        results = list()
        f = lambda t: time.strftime(self.datetime_format,time.localtime(time.mktime(t)))
        # 1 2019年正确日期时间
        results.append([f"2019年正确日期T", time.strftime(self.datetime_format,self._random_datetime(2019, 2019))])
        # 2 错误月13月
        results.append([f"错误月13月F", f((2018,12,11,14,17,39,1,1,0)).replace("12","13")])
        # 3 错误日12月32日
        results.append([f"错误日12月32日F", f((2018,12,31,11,10,55,1,1,0)).replace("31","32")])
        # 4 错误时25时
        results.append([f"错误时25时F", f((2019,5,11,23,1,59,1,1,0)).replace("23","25")])
        # 5 错误分60分
        results.append([f"错误分60分F", f((2019,9,11,0,55,39,1,1,0)).replace("55","60")])
        # 6 错误秒60秒
        results.append([f"错误秒60秒F", f((2018,11,11,11,11,55,1,1,0)).replace("55","60")])
        # 7 不存在的2月29日
        results.append([f"不存在的2月29日F", f((2019,2,27,1,18,40,1,1,0)).replace("27","29")])
        # 8 秒有小数
        if f((2017,1,11,14,17,39,1,1,0)).find("39") != -1:
            results.append([f"秒有小数F", f((2017,1,11,14,17,39,1,1,0)).replace("39","39.33")])
        # 9 正确日期时间前后有空格
        results.append([f"正确日期时间前后有空格F", "    " + f((2019,1,11,22,1,37,1,1,0)) + "      "])
        # 10 正确日期与时间之间多个空格
        results.append([f"正确日期与时间之间多个空格F", f((2019,3,11,8,22,9,1,1,0)).replace("11","11     ")])
        # 11 正确日期与时间之间没有空格
        if f((2019,3,31,8,22,9,1,1,0)).find(" ") != -1:
            results.append([f"正确日期与时间之间没有空格F", f((2019,3,31,8,22,9,1,1,0)).replace(" ","")])
        # 12 年份前多一个0
        results.append([f"年份前多一个0F", "0" + f((2019,9,11,10,18,39,1,1,0))])
        # 13 日期为length位小写字母
        results.append([f"日期为{length}位的小写字母F", self._random_string_multiple(['ZMX'], length)])
        # 14 日期为length位的大写字母
        results.append([f"日期为{length}位的大写字母F", self._random_string_multiple(['ZMD'], length)])
        # 15 日期为length位的小写字母、数字
        results.append([f"日期为{length}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 16 日期为length位大写字母、数字
        results.append([f"日期为{length}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 17 日期为length位全角数字
        results.append([f"日期为{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 18 日期为length位的汉字
        if length >= 2:
            results.append([f"日期为{math.floor(length/self.ch_len)}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len))])
        else:
            results.append([f"日期为{length}位的汉字F", self._random_string_multiple(['HZ'], length)])
        # # 19 日期为length位的繁体字
        # if length >= 2:
        #     results.append([f"日期为{math.floor(length/self.ch_len)}位的繁体字F", self._random_string_multiple(['FT'], math.floor(length/self.ch_len))])
        # else:
        #     results.append([f"日期为{length}位的繁体字F", self._random_string_multiple(['FT'], length)])
        # # 20 日期为length位的难体字
        # if length >= 2:
        #     results.append([f"日期为{math.floor(length/self.ch_len)}位的难体字F", self._random_string_multiple(['NT'], math.floor(length/self.ch_len))])
        # else:
        #     results.append([f"日期为{length}位的难体字F", self._random_string_multiple(['NT'], length)])
        # 21 日期为length位的特殊符号
        # results.append([f"日期为{length}位的特殊符号F", self._random_string_multiple(['FH'], length)])
        # 22 日期为空值
        results.append(["日期为空值F", ''])
        # 23 日期为null值
        results.append(["日期为null值F", None])
        # 24 sql注入 'or '1'='1
        results.append(["sql注入1F", "'' or ''1''=''1"])
        # 25.sql注入'
        results.append(["sql注入2F", "''"])
        # 26 日期为正确四位年月日时分秒
        results.append([f"日期为正确四位年月日时分秒", time.strftime("%Y%m%d%H%M%S", self._random_datetime(2019, 2019))])
        # 27 日期为正确年月日
        results.append([f"日期为正确四位年月日时分秒", time.strftime("%Y%m%d", self._random_datetime(2019, 2019))])
        # 28 日期为正确年-月-日 时分秒
        results.append([f"日期为正确四位年-月-日 时:分:秒", time.strftime("%Y-%m-%d %H:%M:%S",self._random_datetime(2019, 2019))])
        # 28 日期为正确年-月-日 时分
        results.append([f"日期为正确四位年-月-日 时:分", time.strftime("%Y-%m-%d %H:%M",self._random_datetime(2019, 2019))])
        # 29 日期为正确年月日时
        results.append([f"日期为正确四位年-月-日 时", time.strftime("%Y-%m-%d %H",self._random_datetime(2019, 2019))])
        # 30 日期为正确年月日
        results.append([f"日期为正确四位年-月-日", time.strftime("%Y-%m-%d",self._random_datetime(2019, 2019))])
        # 31 日期为正确年月
        results.append([f"日期为正确四位年-月", time.strftime("%Y-%m",self._random_datetime(2019, 2019))])
        # 32 日期为正确年
        results.append([f"日期为正确四位年", time.strftime("%Y",self._random_datetime(2019, 2019))])
        # 33 日期为正确年-月-日 时分秒
        results.append([f"日期为正确两位年-月-日 时:分:秒", time.strftime("%y-%m-%d %H:%M:%S", self._random_datetime(2019, 2019))])
        # 34 日期为正确年月-日 时分
        results.append([f"日期为正确两位年-月-日 时:分", time.strftime("%y-%m-%d %H:%M", self._random_datetime(2019, 2019))])
        # 35 日期为正确年月日时
        results.append([f"日期为正确两位年-月-日 时", time.strftime("%y-%m-%d %H", self._random_datetime(2019, 2019))])
        # 36 日期为正确年月日
        results.append([f"日期为正确两位年-月-日", time.strftime("%y-%m-%d", self._random_datetime(2019, 2019))])
        # 37 日期为正确年月
        results.append([f"日期为正确两位年-月", time.strftime("%y-%m", self._random_datetime(2019, 2019))])
        # 38 日期为正确两位年月日时分秒
        results.append([f"日期为两位年月日时分秒", time.strftime("%y%m%d%H%M%S", self._random_datetime(2019, 2019))])
        # 39 日期为正确两位年月日
        results.append([f"日期为两位年月日时分秒", time.strftime("%y%m%d", self._random_datetime(2019, 2019))])

        # 40 删除此节点
        results.append(["删除报文中此节点F",'DEL'])
        self.logger.debug(results)
        return results

    @type_route("INT")
    def _int_case(self,length,ndigit=0):
        """
        生成CHAR的通用测试用例
        :return:
        """
        length = int(length)
        results = list()
        # 1生成length位的正数
        results.append([f"生成{length}位的正数T", self._random_int_and_double(length)])
        # 2生成length+1位的正数
        results.append([f"生成{length+1}位的正数F", self._random_int_and_double(length + 1)])
        # 3生成length位的正数（两边有空格）
        results.append([f"生成{length}位的正数（两边有空格）F", "   " + self._random_int_and_double(length) + "  "])
        # 4生成length位的负数
        results.append([f"生成{length}位的负数F", "-" + self._random_int_and_double(length) ])
        # 5生成length+1位的负数
        results.append([f"生成{length+1}位的负数F", "-" + self._random_int_and_double(length + 1)])
        # 6生成length位的小写字母
        results.append([f"生成{length}位的小写字母F", self._random_string_multiple(['ZMX'], length)])
        # 7生成length位的大写字母
        results.append([f"生成{length}位的大写字母F", self._random_string_multiple(['ZMD'], length)])
        # 8生成length位的小写字母、数字
        if length >= 2:
            results.append([f"生成{length}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 9生成length位大写字母、数字
        if length >= 2:
            results.append([f"生成{length}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 10生成length位全角数字
        results.append([f"生成{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 11生成length位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的汉字F", self._random_string_multiple(['HZ'], length)])
        # # 12生成length位的繁体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的繁体字F", self._random_string_multiple(['FT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的繁体字F", self._random_string_multiple(['FT'], length)])
        # # 13生成length位的难体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的难体字F", self._random_string_multiple(['NT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的难体字F", self._random_string_multiple(['NT'], length)])
        # 14生成length位的特殊符号
        results.append([f"生成{length}位的特殊符号F", self._random_string_multiple(['FH'], length)])
        # 15生成空值
        results.append(["生成空值F", ''])
        # 16生成null值
        results.append(["生成null值F", None])
        # 17sql注入 'or '1'='1
        results.append(["sql注入1F", self._random_int_and_double(1) + "'' or ''1''=''1"])
        # 18.sql注入 '
        results.append(["sql注入2F", "''"])
        # 19.删除此节点
        results.append(["删除报文中此节点F",'DEL'])
        self.logger.debug(results)
        return results

    @type_route("DOUBLE")
    def _double_case(self, length,ndigit):
        """
        生成DOUBLE的通用测试用例
        :param length:数字总位数（含小数位数）
        :param ndigit:小数位数
        :return:
        """
        length = int(length)
        results = list()
        # 1生成length ndigit位的正小数
        results.append([f"生成{length},{ndigit}位的正小数T", self._random_int_and_double(length - ndigit, ndigit)])
        # 2生成length+1位的正小数
        results.append([f"生成{length+1}位的正数F", self._random_int_and_double(length+1,ndigit)])
        # 3生成length位的正小数（两边有空格）
        results.append([f"生成{length},{ndigit}位的正小数（两边有空格）F","   " + self._random_int_and_double(length - ndigit, ndigit) + "  "])
        # 4生成length位的负小数
        results.append([f"生成{length},{ndigit}位的负小数F", "-" + self._random_int_and_double(length - ndigit, ndigit)])
        # 5生成length+1位的负小数
        results.append([f"生成{length+1}位的负数F", "-" + self._random_int_and_double(length+1,ndigit)])
        # 6生成length位的小写字母
        results.append([f"生成{length}位的小写字母F", self._random_string_multiple(['ZMX'], length)])
        # 7生成length位的大写字母
        results.append([f"生成{length}位的大写字母F", self._random_string_multiple(['ZMD'], length)])
        # 8生成length位的小写字母、数字
        if length >= 2:
            results.append([f"生成{length}位的小写字母、数字F", self._random_string_multiple(['ZMX', 'SZ'], length)])
        # 9生成length位大写字母、数字
        if length >= 2:
            results.append([f"生成{length}位大写字母、数字F", self._random_string_multiple(['ZMD', 'SZ'], length)])
        # 10生成length位全角数字
        # results.append([f"生成{length}位全角数字F", self._random_string_multiple(['QJSZ'], length)])
        # 11生成length位的汉字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的汉字F", self._random_string_multiple(['HZ'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的汉字F", self._random_string_multiple(['HZ'], length)])
        # 12生成length位的繁体字
        if length >=2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的繁体字F", self._random_string_multiple(['FT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的繁体字F", self._random_string_multiple(['FT'], length)])
        # 13生成length位的难体字
        if length >= 2:
            results.append([f"生成{math.floor(length/self.ch_len)}位的难体字F", self._random_string_multiple(['NT'], math.floor(length/self.ch_len))])
        else:
            results.append([f"生成{length}位的难体字F", self._random_string_multiple(['NT'], length)])
        # 14生成length位的特殊符号
        results.append([f"生成{length}位的特殊符号F", self._random_string_multiple(['FH'], length)])
        # 15生成空值
        results.append(["生成空值F", ''])
        # 16生成null值
        results.append(["生成null值F", None])
        # 17sql注入 'or '1'='1
        results.append(["sql注入1F", self._random_int_and_double(1, 3) + "'' or ''1''=''1"])
        # 18.sql注入 '
        results.append(["sql注入2F", "''"])
        # 19.删除此节点
        results.append(["删除报文中此节点F",'DEL'])
        self.logger.debug(results)
        return results

    @type_route('NSRSBH')
    def random_string_nsrsbh(self, length,ndigit):
        '''针对纳税人识别号不同位数不同类型进行单独生成'''
        pass

    # 20200110--将此函数功能改为路由
    def random_string_main(self,sort,length=10,ndigit=2):
        sort_upper = sort.strip().upper()
        try:
            string_list = TYPES_DICT[sort_upper](self,length,ndigit)
        except Exception as e:
            self.logger.error("输入的sort值有误{}，{}".format(sort_upper,e))
            raise SortError("输入的sort值有误：{}，程序终止！！".format(sort_upper))
        return string_list

    # def random_string_main(self,sort,length=10,ndigit=2):
    #     if sort.strip().upper() == "VARCHAR":
    #         string_list = self._varchar_case(length)
    #         # [['生成11位的数字', '34140688517'], ['生成12位的数字', '031856900374']]
    #     elif sort.strip().upper() == "CHAR":
    #         string_list = self._char_case(length)
    #     elif sort.strip().upper() == "DATETIME":
    #         string_list = self._datetime_case(length)
    #     elif sort.strip().upper() == "INT":
    #         string_list = self._int_case(length)
    #     elif sort.strip().upper() == "DOUBLE":
    #         string_list = self._double_case(length,ndigit)
    #     else:
    #         self.logger.error("输入的sort值有误{}".format(sort))
    #         raise SortError("输入的sort值有误：{}，程序终止！！".format(sort))
    #     return string_list


class SortError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo



if __name__=="__main__":
    get_string = GetString()
    # results = get_string._random_string_multiple(["QJSZ","SZ","ZMX","ZMD","FT"],20)
    # results = get_string._random_string_multiple(["SZ"], 1)
    # results = get_string.random_string_main("datetime",20)
    get_string._random_int_and_double(20,2)


