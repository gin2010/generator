# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.2
# @Desc  :重新做了抽象，每次改写generate_request_json与update_cases方法即可
#         generate_request_json：影响的是写入数据库中request_sql_param内容；
#         update_cases:影响最终传入到mysql insert语句中全部值的字典；
#         发票采集模板使用：
#         1修改发票号码、发票代码；
#         2将内层报文参数inner_param的值修改为inner_param_value并返回
#         :param temp:内层报文（从模板文件中读取的）
#         :param step:测试用例step（从excel模板common中读取的step）
#         :param fphm:发票号码（从excel模板common中读取的起始发票号码）
#         :param inner_key:内层报文中需要更新的key（从excel模板case中读取的每一行request_param的值），相当于每次修改的字段
#         :param inner_value:内层报文中需要更新的key对应的value（GetString返回的字段值，一次传入一个）
#         :return temp: 转换为json格式的内层报文，写入到数据库request_sql_param的内容


import json,sys,os,copy,xlrd,configparser
from tool.operateMysqlClass import OperateMysql
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator
from tool.searchDict import search_dict_key
from randomStringClass import GetString


class Generator_S_Demo(Generator):

    # 修改父类的模板
    # 测试single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类


class Generator_M_Demo(Generator):

    # 修改父类的模板
    # 测试multiple用例生成
    def __init__(self):
        super().__init__()  # 初始化父类

    def generate_request_json(self,temp,data):

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

    # 20191206将统一查询excel用例步骤及数据写入到数据库中
    # 统一查询（ofd）
    def __init__(self):
        super().__init__()  # 初始化父类

    def generate_request_json(self,temp,data):
        #处理case sheet 每一行数据
        tycx_request = json.loads(data[1])
        fphm = tycx_request['fP_HM']
        fpdm = tycx_request['fP_DM']
        redis_request = "redis get speed-invoice-{}".format(fpdm+fphm)
        mongodb_request = '''mongo invoice find {"FP_DM":"%s","FP_HM":"%s"}''' % (fpdm,fphm)
        cj_request = '''SELECT * FROM "fp_kj" where fpdm="%s" and fphm="%s";''' % (fpdm,fphm)
        self.logger.debug("redis_request:{}".format(redis_request))
        self.logger.debug("mongodb_request:{}".format(mongodb_request))
        for d in data[3:]:
            request = ""
            url_sql = ""
            http_method = ""
            if d == "":
                break
            elif d.startswith("Redis查询"):
                url_sql = redis_request
            elif d.startswith("大数据"):
                url_sql = mongodb_request
            elif d.startswith("发票号码代码查询"):
                url_sql = "/services/tycx/getInvoice"
                request = tycx_request
                http_method = "post"
            elif d.startswith("采集库中查询"):
                url_sql = cj_request
            else:
                self.logger.error(f"未能正确处理，请确认步骤描述是否错误：{d}")
            self.logger.debug([data[0],d,url_sql,request])
            yield [data[0],d,url_sql,request,http_method]


    def update_cases(self,cases,step,request):
        #传入的request为上面函数的返回 [data[0],d,url_sql,request,http_method]
        case = copy.deepcopy(cases)
        case["step"] = step
        case["test_desc"] = case["test_desc"] + '-' + request[0]
        case["request_name"] = request[1]
        case['url_sql'] = request[2]
        case['http_method'] = request[4]
        if isinstance(request[3],dict):
            case["request_sql_param"] = json.dumps(request[3], ensure_ascii=False)
        else:
            case["request_sql_param"] = request[3]
        self.logger.debug("case:{}".format(case))
        return case



def single_demo():
    # 测试single，值传入1
    generate = Generator_S_Demo()
    generate.generate_case(1)


def multiple_demo():
    # 测试mutiple，值传入2
    generate = Generator_M_Demo()
    generate.generate_case(2)


def tycx():
    # 统一查询（ofd）用例导入
    generate = Generator_tycx()
    generate.generate_case(2)


def fpqz_json():
    # 发票签章json
    generate1 = Generator_S_Demo()
    # single
    generate1.generate_case(1)
    # multiple
    # generate2 = Generator()
    # generate2.generate_case(2)


def main():
    #interface_name = Generator().interface_name #初始化整个类，效率低
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', "generator.ini")
    config = configparser.RawConfigParser()
    config.read(config_file, encoding="utf-8")
    interface_name = config.get("template","interface_name")
    # 使用如下方法实现switch_case
    controller = {"single_demo":single_demo,
                  "multiple_demo":multiple_demo,
                  "tycx":tycx,
                  "fpqz_json":fpqz_json,
                  }
    controller.get(interface_name)()


if __name__ == "__main__":
    main()
