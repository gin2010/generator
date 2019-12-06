# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.2
# @Desc  :每次改写update_temp_single方法，更改最终传入到request_sql_param中内层报文的内容，由于不同的接口内层报文不一致，
#         因此将此方法针对不同的接口报文类型**重写**，不同的接口通过修改配置文件中模板文件temp与模板类型
#         发票采集模板使用：
#         1修改发票号码、发票代码；
#         2将内层报文参数inner_param的值修改为inner_param_value并返回
#         :param temp:内层报文（从模板文件中读取的）
#         :param step:测试用例step（从excel模板common中读取的step）
#         :param fphm:发票号码（从excel模板common中读取的起始发票号码）
#         :param inner_key:内层报文中需要更新的key（从excel模板case中读取的每一行request_param的值），相当于每次修改的字段
#         :param inner_value:内层报文中需要更新的key对应的value（GetString返回的字段值，一次传入一个）
#         :return temp: 转换为json格式的内层报文，写入到数据库request_sql_param的内容


import json,sys,os,time,random,copy,xlrd
from tool.operateMysqlClass import OperateMysql
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator
from tool.search_dict import search_dict_key


class Generator_Demo(Generator):

    # 修改父类的模板
    # 测试single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类


class Generator_M_Demo(Generator):

    # 修改父类的模板
    # 测试multiple用例生成
    def __init__(self):
        super().__init__()  # 初始化父类

    def generate_request_json(self,temp,start,data):

        keys = data[2].split(sep="\n")
        values = data[3].split(sep="\n")
        if len(keys) == len(values):
            for i in range(len(keys)):
                temp = search_dict_key(temp, keys[i], values[i])
            yield (data[1], temp)
        else:
            self.logger.error("data({}) is wrong".format(data))
            return


class Generator_tycx(Generator):

    # 修改父类的模板
    # 统一查询（ofd）
    def __init__(self):
        super().__init__()  # 初始化父类

    def generate_request_json(self,temp,start,data):

        keys = data[2].split(sep="\n")
        values = data[3].split(sep="\n")
        if len(keys) == len(values):
            for i in range(len(keys)):
                temp = search_dict_key(temp, keys[i], values[i])
            yield (data[1], temp)
        else:
            self.logger.error("data({}) is wrong".format(data))
            return



if __name__ == "__main__":
    # 测试single
    # generate = Generator_Demo()
    # generate.generate_case(1)
    # 测试mutiple
    generate = Generator_M_Demo()
    generate.generate_case(2)

