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


    def _read_common_sheet(self,path):
        '''
        读取excel用例表common sheet中的case_id,http_method等每个用例中固定的值，组成字典并返回；
        并可以扩展字段的数量 如：common_sheet["aoto"] = ws_common.cell(7, 1).value
        :param path:excel文件所在的路径
        :return
            :common_dict:
                {'case_id': '24000001',
                'http_method': 'post',
                'url_sql': '/services/tyjs/saveInvoice',
                'step': '10000',
                'test_desc': '发票采集-单字段校验',
                'out_put': '',
                'fphm_start': '10000000'}
        '''
        wb = xlrd.open_workbook(path)
        ws_common = wb.sheet_by_name("common")
        common_sheet = dict()
        common_sheet["case_id"] = ws_common.cell(0, 1).value
        common_sheet["http_method"] = ws_common.cell(1, 1).value
        common_sheet["url_sql"] = ws_common.cell(2, 1).value
        common_sheet["step"] = ws_common.cell(3, 1).value
        common_sheet["test_desc"] = ws_common.cell(4, 1).value
        common_sheet["out_put"] = ws_common.cell(5, 1).value
        common_sheet["start"] = ws_common.cell(6, 1).value
        self.logger.debug(common_sheet)
        return common_sheet


    def _read_case_sheet(self,path):
        """
        读取用例表中的case sheet，并返回二维列表
        :param path:excel所在的路径
        :yield :每行数据列表的生成器

        """
        # 读取case sheet
        wb = xlrd.open_workbook(path)
        case_sheet = wb.sheet_by_name("case")
        max_row = case_sheet.nrows
        for i in range(1,max_row):
            yield case_sheet.row_values(i)




    def generate_request_json(self,temp,start,data):
        """
        修改传入的temp中部分字段的值，然后返回requests列表，最终保存到request_sql_param中。
        由于不同的接口内层报文不一致，因此将此方法针对不同的接口报文类型**重写**，
        不同的接口通过修改配置文件中模板文件temp与模板类型
        发票采集模板使用：
            1修改发票号码、发票代码；
            2将内层报文参数inner_param的值修改为inner_param_value并返回
        :param temp:从template里加载的内层报文
        :param start:从excel模板common中读取的start，用于控制发票号码等需要变化的值
        :return requests: 每行生成的新temp，及其他需要加入到写入到数据库字段的值
        """
        # 修改模板中发票号码
        get_string = GetString(self.logger)
        if isinstance(data[2], str):
            length = data[2].replace("，", ",").split(",")
            data.pop()
            data.extend(length)
        if len(data) == 4:
            string_list = get_string.random_string_main(data[1],int(data[2]),int(data[3]))
        else:
            string_list = get_string.random_string_main(data[1], int(data[2]))
        for l in string_list:
            temp = search_dict_key(temp,data[0],l[1])
            yield (data[0] + "-" + l[0],temp)


    def update_cases(self,case,step,request):
        """
        用于修改每次最后写入到mysql里各个字段的值
        :param case: 字典类型，存放mysql中部分字段对应的值
        :param step: 每次变化的step
        :param request:存放request_sql_param里的值及描述等
        :return:
        """
        case = copy.deepcopy(case)
        case["step"] = step
        # cases["test_desc"] = request[0]
        case["request_name"] = request[0]
        case["request_sql_param"] = json.dumps(request[1], ensure_ascii=False)
        return case


    def generate_case(self,flag):
        '''
        生成单个字段的测试用例
        temp里的值在update_temp里修改，
        请求sql数据库（除request_sql_param外）全部在此函数里修改
        :param flag: 1表示生成single用例  2表示生成multiple用例
        :return:
        '''
        if flag == 1:
            case_path = os.path.join(self.generate_path,"data",self.single_case_excel)
        elif flag == 2:
            case_path = os.path.join(self.generate_path, "data", self.multiple_case_excel)
        else:
            raise NotImplementedError
        # cases对应mysql一条用例，cases为字典类型、key与mysql里的值相同
        cases = self._read_common_sheet(case_path)
        datas = self._read_case_sheet(case_path)
        self.logger.debug(["{}-type:{}".format(cases,type(cases))])
        self.logger.debug(["{}-type:{}".format(datas, type(datas))])
        # 连接mysql数据库
        mysql = OperateMysql(self.logger)
        # 定义初始step
        step = int(cases["step"])
        for row in datas:
            # row 为case sheet第一行数据的列表
            temp_one = copy.deepcopy(self.temp)
            requests = self.generate_request_json(temp_one, cases["start"], row)
            for request in requests:
                # case_datas的结构如下：
                # [{'resquest_param': 'fp_dm','param_sort': 'VARCHAR', 'length': '10'},
                #  {'resquest_param': 'kprq', 'param_sort': 'DATETIME', 'length': ''}]
                self.logger.debug(["request:", request])
                step += 1
                cases = self.update_cases(cases,step,request)
                mysql.insert_sql(cases)
            step += 10
        mysql.close()



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