# -*- coding: utf-8 -*-
# @Date : 2019/09/27
# @Author : water
# @Version  : v1.1
# @Desc  :自动生成单个字段的测试用例、根据excel表中的字段生成联合字段的测试用例及测试主流程


import json,xlrd,os
import configparser,copy,time
from operateMysqlClass import OperateMysql
from randomStringClass import GetString
from logSetClass import Log
from tool.search_dict import search_dict_key

class Generator(object):

    def __init__(self):

        # 配置文件地址
        config_name = 'generator.ini'
        self.generate_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.generate_path, 'config', config_name)
        # 日志文件地址
        log_name = "generator.log"
        log_file = os.path.join(self.generate_path, 'log', log_name)
        # 加载配置文件中的内容
        config = configparser.RawConfigParser()
        config.read(self.config_file,encoding="utf-8")
        # 日志配置
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        self.logger.warning(config_name)
        '''
        # 单独日志配置于20191012替换，由于只能打印到控制台，无法输出到文件中
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        '''
        # 加载用例excel
        if config.has_section("excel_name") :  # 是否存在excel_name
            if config.has_option("excel_name", "single_case"): # 是否存在single_case
                self.single_case_excel = config.get("excel_name","single_case")
            if config.has_option("excel_name", "multiple_case"): # 是否存在multiple_case
                self.multiple_case_excel = config.get("excel_name","multiple_case")
        self.logger.debug([self.single_case_excel,self.multiple_case_excel])
        # 加载模板
        temp_path = os.path.join(self.generate_path,'config',config.get("template","temp"))
        with open(temp_path, 'r') as f:
            self.temp = json.load(f)
            self.logger.info(self.temp)


    def _read_single_excel(self,path):
        '''
        读取excel表common sheet中的case_id,http_method等每个用例中固定的值，组成字典
        读取excel表中case sheet中的step,request_param等每个用例中变化的值，组成如下类型的字典
        :param path:文件路径
        :return
            :case_list:
                [{'resquest_param': 'FPQQLSH', 'param_sort': 'VARCHAR', 'length': 64.0},
                {'resquest_param': 'XSF_NSRMC', 'param_sort': 'VARCHAR', 'length': 200.0},...]
            :common_dict:
                {'case_id': '24000001',
                'http_method': 'post',
                'url_sql': '/services/tyjs/saveInvoice',
                'step': '1000',
                'test_desc': '发票采集-单字段校验',
                'out_put': '',
                'fphm_start': '10000000'}
        '''
        #读取case sheet
        wb = xlrd.open_workbook(path)
        ws_case = wb.sheet_by_name("case")
        max_row_case = ws_case.nrows
        case_list = list()  # 列表里存放excel列名：每行数据组成的字典
        for r in range(1, max_row_case):
            d = dict()
            d['resquest_param'] = ws_case.cell(r, 0).value
            d['param_sort'] = ws_case.cell(r, 1).value
            self.logger.info(ws_case.cell(r, 2).value)
            length = ws_case.cell(r, 2).value
            if isinstance(length,str):
                length = length.replace("，",",").split(",")
                d['ndigit'] = int(length[1])
                d['length'] = int(length[0])
            else:
                d['length'] = int(length)
            case_list.append(d)
        self.logger.debug(case_list)
        #读取common sheet
        ws_common = wb.sheet_by_name("common")
        common_dict = dict()
        common_dict["case_id"] = ws_common.cell(0, 1).value
        common_dict["http_method"] = ws_common.cell(1, 1).value
        common_dict["url_sql"] = ws_common.cell(2, 1).value
        common_dict["step"] = ws_common.cell(3, 1).value
        common_dict["test_desc"] = ws_common.cell(4, 1).value
        common_dict["out_put"] = ws_common.cell(5, 1).value
        common_dict["fphm_start"] = ws_common.cell(6, 1).value
        self.logger.debug(common_dict)
        return case_list, common_dict


    def _read_multiple_excel(self,path):
        """
        读取multiple 用例excel表
        :param path:multiple excel所在的路径
        :return cases:
        [{
        "case_name": "CEZS_GZ编码表版本号为空但扣除额有值F",
        "head": {"KPLX": "0", "DKBZ": "0", "SGBZ": "", "BMB_BBH": "","QD_BZ": "0","QDXMMC": ""},
        "mx": [{"XMMC": "*谷物* 花生", "XMDJ": "", "XMJE": "1100", "SL": "0.03", "SE": "30",},
            {"XMMC": "*谷物* 花生", "XMDJ": "", "XMJE": "1100", "SL": "0.03", "SE": "30",}]
        },
        {...}]
        """
        wb = xlrd.open_workbook(path)
        # 读取case sheet
        ws_case = wb.sheet_by_name("case")
        cases = list()
        max_row = ws_case.nrows
        max_column = ws_case.ncols
        self.logger.info(max_column)
        for r in range(1, max_row):
            case = dict()
            case["case_name"] = ws_case.cell(r, 1).value
            if isinstance(ws_case.cell(r, 2).value,str):
                case['key'] = ws_case.cell(r, 2).value.split(sep="\n")
            else:
                case['key'] = ws_case.cell(r, 2).value
            if isinstance(ws_case.cell(r, 3).value,str):
                case['value'] = ws_case.cell(r, 3).value.split(sep="\n")
            else:
                case['value'] = ws_case.cell(r, 3).value
            cases.append(case)
        # 读取common sheet
        ws_common = wb.sheet_by_name("common")
        common_dict = dict()
        common_dict["case_id"] = ws_common.cell(0, 1).value
        common_dict["http_method"] = ws_common.cell(1, 1).value
        common_dict["url_sql"] = ws_common.cell(2, 1).value
        common_dict["step"] = ws_common.cell(3, 1).value
        common_dict["test_desc"] = ws_common.cell(4, 1).value
        common_dict["out_put"] = ws_common.cell(5, 1).value
        common_dict["fphm_start"] = ws_common.cell(6, 1).value
        self.logger.debug(common_dict)
        return cases, common_dict


    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        """
        此方法只是更改最终传入到request_sql_param中内层报文的内容，由于不同的接口内层报文不一致，
        因此将此方法针对不同的接口报文类型**重写**，不同的接口通过修改配置文件中模板文件temp与模板类型
        发票采集模板使用：
            1修改发票号码、发票代码；
            2将内层报文参数inner_param的值修改为inner_param_value并返回
        :param temp:内层报文
        :param step:测试用例step（从excel模板common中读取的step）
        :param fphm:发票号码（从excel模板common中读取的起始发票号码）
        :param inner_key:内层报文中需要更新的key（从excel模板case中读取的每一行request_param的值），相当于每次修改的字段
        :param inner_value:内层报文中需要更新的key对应的value（GetString返回的字段值，一次传入一个）
        :return temp: 转换为json格式的内层报文
        """
        # 修改模板中发票号码
        temp['FPXX']['FP_KJ']['FPHM'] = int(fphm) + step
        # 修改模板中的发票代码
        temp['FPXX']['FP_KJ']['FPDM'] = "24" + time.strftime("%y%m") + "000240"
        inner_key = inner_key.upper()
        # 发票主信息
        if inner_param in temp['FPXX']['FP_KJ'].keys():
            temp['FPXX']['FP_KJ'][inner_param] = inner_value
        # 发票开具明细
        elif inner_param in temp['FPXX']['FP_KJ_MX'][0].keys():
            temp['FPXX']['FP_KJ_MX'][0][inner_param] = inner_value
        # 发票物流信息
        elif inner_param in temp['FPXX']['FP_WLXX'][0].keys():
            temp['FPXX']['FP_WLXX'][0][inner_param] = inner_value
        # 发票支付信息
        elif inner_param in temp['FPXX']['FP_ZFXX'].keys():
            temp['FPXX']['FP_WLXX'][0][inner_param] = inner_value
        else:
            self.logger.error(f"未找到{inner_key}!!!!!!!")

        return json.dumps(temp, ensure_ascii=False)


    def update_temp_multiple(self,temp,step,fphm,inner_keys,inner_values):
        """
        此方法只是更改最终传入到request_sql_param中内层报文的内容，由于不同的接口内层报文不一致，
        因此将此方法针对不同的接口报文类型**重写**，不同的接口通过修改配置文件中模板文件temp与模板类型
        发票采集模板使用：
            1修改发票号码、发票代码；
            2将内层报文参数inner_param的值修改为inner_param_value并返回
        :param temp:内层报文
        :param step:测试用例step
        :param fphm:发票号码
        :param inner_key:内层报文中需要更新的key，是一个列表存放的
        :param inner_value:内层报文中需要更新的key对应的value，是一个列表存放的
        :return temp: 转换为json格式的内层报文
        """
        temp = copy.deepcopy(temp)
        # 修改模板中发票号码
        temp['head']['pjhm'] = int(fphm) + step
        # 修改模板中发票代码
        temp['head']['pjdm'] = "24" + time.strftime("%y%m") + "000241"
        # 用inner_keys、inner_values里的值更新temp里对应的值
        for i in range(len(inner_keys)):
            temp = search_dict_key(temp, inner_keys[i], inner_values[i])
        return json.dumps(temp, ensure_ascii=False)


    def generate_single_case(self):
        '''
        生成单个字段的测试用例
        temp里的值在update_temp里修改，
        请求sql数据库（除request_sql_param外）全部在此函数里修改
        :return:
        '''
        single_case_path = os.path.join(self.generate_path,"data",self.single_case_excel)
        case_datas, common_datas = self._read_single_excel(single_case_path)
        self.logger.debug([case_datas,common_datas])
        step = int(common_datas["step"])
        # 连接mysql数据库
        opsql = OperateMysql(self.logger)
        for d in case_datas:
            # case_datas的结构如下：
            # [{'resquest_param': 'fp_dm','param_sort': 'VARCHAR', 'length': '10'},
            #  {'resquest_param': 'kprq', 'param_sort': 'DATETIME', 'length': ''}]
            # single_temp = copy.deepcopy(self.temp)
            self.logger.debug(["d:",d])
            get_string = GetString(self.logger)
            if d.get("ndigit")==None:
                string_list = get_string.random_string_main(d["param_sort"], d["length"])
            else:
                string_list = get_string.random_string_main(d["param_sort"],d["length"],d["ndigit"])
            for l in string_list:
                step += 1
                common_datas["step"] = step
                common_datas["request_name"] = str(d["resquest_param"]) + "--" + l[0]
                common_datas["request_sql_param"] = self.update_temp_single(self.temp,step,common_datas["fphm_start"],d["resquest_param"], l[1])
                opsql.insert_sql(common_datas)
            step += 10
        opsql.close()


    def generate_multiple_case(self):
        '''
        生成联合字段与主流程的测试用例
        :return:
        '''
        multiple_case_path = os.path.join(self.generate_path, "data", self.multiple_case_excel)
        datas, commons = self._read_multiple_excel(multiple_case_path)
        self.logger.debug(datas)
        opsql = OperateMysql(self.logger)
        step = int(commons["step"])
        for data in datas:
            step += 1
            commons["step"] = step
            commons["request_name"] = data['case_name']
            commons["request_sql_param"] = self.update_temp_multiple(self.temp,step,commons["fphm_start"],data["key"],data["value"])
            self.logger.info(commons)
            opsql.insert_sql(commons)
        opsql.close()
        self.logger.warning("------ end ------！")


if __name__ =="__main__":
    # 测试generatorCase类
    # generate = Generator()
    # generate.generate_single_case()

    # 测试_read_multiple_excel
    # generate = Generator()
    # multiple_case_path = os.path.join(generate.generate_path, "data", generate.multiple_case_excel)
    # print(multiple_case_path)
    # datas, commons = generate._read_multiple_excel(multiple_case_path)
    # print(datas)

    # 测试randomStringClass类
    get_string = GetString(self.logger)
    results = get_string.random_string_main("datetime",10)
    print(results)