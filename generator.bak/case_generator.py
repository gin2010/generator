# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.3
# @Desc  :主程序，直接运行此程序即可


import json,sys,os,copy,xlrd,configparser
from tool.operateMysqlClass import OperateMysql
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator
from tool.searchDict import search_dict_key,search_dict
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


class Generator_S_FPQZ(Generator):

    # 修改父类的模板
    # 测试single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类

    def modify_temp_other(self,temp,step,target_key,**kwargs):
        '''
        增加此方法提高复用性
        可以根据需要传入接口中需要变化的值，比如 fphm,nsrsbh。
        使用step来实现值的累加，这样就不用全局变量了
        :param temp:
        :param kwargs:内部值的key-value
        :return:
        '''
        kwargs['fp_hm'] = str(int(kwargs['fp_hm']) + step - 10000)
        super().modify_temp_other(temp,step,target_key,**kwargs)
        return temp


class Generator_S_FPCJ(Generator):

    # 修改父类的模板
    # 测试single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类

    def modify_temp_other(self,temp,step,target_key,**kwargs):
        '''
        增加此方法提高复用性
        可以根据需要传入接口中需要变化的值，比如 fphm,nsrsbh。
        使用step来实现值的累加，这样就不用全局变量了
        :param temp:
        :param kwargs:内部值的key-value
        :return:
        '''
        kwargs['FPHM'] = str(int(kwargs['FPHM']) + step - 10000)
        super().modify_temp_other(temp,step,target_key,**kwargs)
        return temp

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
    generate = Generator_S_Demo()
    generate.generate_case(1)

@myroute("multiple_demo")
def multiple_demo():
    # 测试mutiple，值传入2
    generate = Generator_M_Demo()
    generate.generate_case(2)

@myroute("tycx")
def tycx():
    # 统一查询（ofd）用例导入
    generate = Generator_tycx()
    generate.generate_case(2)

@myroute("fpqz_json")
def fpqz_json():
    # 发票签章json
    generate1 = Generator_S_FPQZ()
    # single
    generate1.generate_case(1)
    # multiple
    # generate2 = Generator()
    # generate2.generate_case(2)

@myroute("fpcj_json")
def fpcj_json():
    # 发票采集json
    generate1 = Generator_S_FPCJ()
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
    ROUTE[interface_name]()


if __name__ == "__main__":
    main()
