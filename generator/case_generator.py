# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.3
# @Desc  :主程序，直接运行此程序生成submarine测试用例


import os,configparser
from tool.generatorCase import Generator_S_Case,Generator_S_FPQZ,Generator_M_Case,Generator_Data_FPQZ
from tool.mysqlOrm import SJ_GZ,Yhzc_GZ
# 添加tool工具包到系统变量中
# tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
# sys.path.append(tool)


# 路由功能
ROUTE = dict()
def myroute(interface):
    def dict_func(func):
        ROUTE[interface] = func
        def call_func():
            return func()
        return call_func
    return dict_func

@myroute("single_demo")
def single_demo():
    # 测试single，值传入1
    generate = Generator_S_Case()
    generate.generate_case_main()

@myroute("multiple_demo")
def multiple_demo():
    # 测试mutiple，值传入2
    generate = Generator_M_Case()
    generate.generate_case_main()

# @myroute("tycx")
# def tycx():
#     # 统一查询（ofd）用例导入
#     generate = Generator_tycx()
#     generate.generate_case_main()

@myroute("fpqz_json")
def fpqz_json():
    # 发票签章json
    generate1 = Generator_S_FPQZ()
    generate1.generate_case_main()


@myroute("fpqz_json_data")
def fpqz_json_data():
    # 发票签章json
    tables = [SJ_GZ,Yhzc_GZ]
    generate = Generator_Data_FPQZ(tables)
    generate.generate_case_main()


@myroute("fpcj_json")
def fpcj_json():
    # 发票采集json
    generate1 = Generator_S_FPCJ()
    # single
    generate1.generate_case_main()
    # multiple
    # generate2 = Generator()
    # generate2.generate_case()


def main():
    #interface_name = Generator().interface_name #初始化整个类，效率低
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', "case_generator.ini")
    config = configparser.RawConfigParser()
    config.read(config_file, encoding="utf-8")
    interface_name = config.get("template","interface_name")
    ROUTE[interface_name]()


if __name__ == "__main__":
    main()
