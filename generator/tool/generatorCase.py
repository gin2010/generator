# -*- coding: utf-8 -*-
# @Date : 2019/09/27
# @Author : water
# @Version  : v1.2
# @Desc  :自动生成单个字段的测试用例、根据excel表中的字段生成联合字段的测试用例及测试主流程
#         case:用例数据库的一条用例k-v字典
#         temp:内层报文模板

import json,xlrd,os
import configparser,copy,time
from operateMysqlClass import OperateMysql
from randomStringClass import GetString
from logSetClass import Log
from searchDict import search_dict_key,search_dict,del_dict_key
from mysqlOrm import Interface_FPQZ,SJ_GZ

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # generator路径

class Generator(object):

    def __init__(self):

        # 配置文件地址
        config_name = 'case_generator.ini'
        self.config_file = os.path.join(PATH, 'config', config_name)
        # 日志文件地址
        time_str = time.strftime('%Y%m%d%H%M', time.localtime())
        log_name = "case_generator_" + time_str + ".log"
        log_file = os.path.join(PATH, 'log', log_name)
        # 加载配置文件
        config = configparser.RawConfigParser()
        config.read(self.config_file,encoding="utf-8")
        # 加载配置文件--日志配置
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        self.logger.warning(config_name)
        '''
        # 单独日志配置于20191012替换，由于只能打印到控制台，无法输出到文件中
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        '''
        # 加载配置文件--加载用例excel
        self.case_excel = config.get("excel_name","case_excel")
        self.logger.debug(self.case_excel)

        # 加载配置文件--加载模板
        temp_path = os.path.join(PATH,'temp','cases',config.get("template","temp"))
        with open(temp_path, 'r') as f:
            self.temp = json.load(f)
            self.logger.info(self.temp)
        # 加载配置文件--加载明细字段
        self.mx_key = config.get("template","mx_key")

    def xml_2_dict(self,temp):
        pass

    def dict_2_xml(self,temp):
        pass

    def _read_common_sheet(self,path):
        '''
        读取excel用例表common sheet中的case_id,http_method等每个用例中固定的值，组成字典并返回；
        :param path:excel文件所在的路径
        :return
            :common_datas_dict:
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
        max_row = ws_common.nrows
        common_datas_dict = dict()
        for i in range(max_row):
            common_datas_dict[ws_common.cell(i, 0).value] = ws_common.cell(i, 1).value
        self.logger.debug(common_datas_dict)
        return common_datas_dict


    # def get_keys(self,path):
    def _read_temp_data(self,path):
        """
        读取用例表中的case sheet，并返回二维列表
        :param path:excel所在的路径
        :yield :每行数据列表4生成器

        """
        # 读取case sheet
        wb = xlrd.open_workbook(path)
        case_sheet = wb.sheet_by_name("case")
        max_row = case_sheet.nrows
        for i in range(1,max_row):
            yield case_sheet.row_values(i)  # 一次读取一行数据


    def generate_values(self,key_row):
        """
        :param temp:从template里加载的内层报文
        :param key_row:从excel模板case sheet中读取的每一行值组成的列表
        :return (key,string_list): （字段名，（描述，字段值））
        """
        get_string = GetString(self.logger)
        key = key_row[0] # 字段名
        if isinstance(key_row[2], str):
            # 对于double类型，分开总长度与小数位数
            len_and_digit = key_row[2].replace("，", ",").split(",")
        else:
            len_and_digit = []

        # 20200110修改，增加传入固定值
        if len(len_and_digit) == 2:
            string_list = get_string.random_string_main(key_row[1],int(len_and_digit[0]),int(len_and_digit[1]))
        else:
            string_list = get_string.random_string_main(key_row[1], int(key_row[2]))
        # 添加key_row中传入的固定值，描述统一用“输入值xxx”
        if key_row[3]:
            fix_values = key_row[3].replace("，", ",").split(",")
            self.logger.debug(key_row)
            self.logger.debug(fix_values)
            for x in fix_values:
                string_list.insert(-1,['输入值{}'.format(x),x]) # 从倒数第二位开始插入，因为模板是共用的，最后一个用例是删除
        self.logger.debug(string_list)
        return (key, string_list)


    def update_temp(self,temp,key,value):
        if value == "DEL":
            del_dict_key(temp, key)
        else:
            temp = search_dict_key(temp, key, value)


    def update_temp_other(self, temp, step, kwargs):
        '''
        增加此方法提高复用性
        可以根据需要传入接口中需要变化的值，比如 fphm,nsrsbh。
        使用step来实现值的累加，这样就不用全局变量了
        :param temp:
        :param target_key:本次修改的模板里的值，如果是fp_hm，则无需再顺序编号
        :param kwargs:内部值的key-value
        :return:
        '''
        fp_hm = str(int(kwargs['fp_hm']) + step - 10000)
        # kwargs.pop(target_key, None)  # 20200107-从字典里删除target_key(会影响到fpdm的数据)
        search_dict_key(temp, 'fp_hm',fp_hm)


    def update_case(self,case,step,temp,desc):
        """
        用于修改每次最后写入到mysql里各个字段的值
        :param case: submarine里面一条用例脚本全部值组成的字典
        :param step: 每次变化的step
        :param request:存放request_sql_param里的值及描述等
        :return:写入数据库的一条用例值组成的字典
        """
        case = copy.deepcopy(case)
        case["step"] = step
        case["test_desc"] = case["test_desc"] + "--" + desc
        case["request_name"] = desc
        # 20191227 增加修改模板其他变量的函数
        case["request_sql_param"] = json.dumps(temp, ensure_ascii=False)
        return case


    def generate_case_main(self):

        case_path = os.path.join(PATH, "data", 'cases', self.case_excel)
        common_datas = self._read_common_sheet(case_path)  # 1.从excel加载公共数据
        # origin_case = copy.deepcopy(common_datas)
        step = int(common_datas["step"])
        temp_datas = self._read_temp_data(case_path)  # 2.从excel加载case中单个或多个字段数据
        mysql = OperateMysql(self.config_file, self.logger) # 3.连接数据库
        for temp_data in temp_datas:
            # temp_data ['FHDM','varchar','8']
            (key,values_list) = self.generate_values(temp_data)  # 4.生成单个或多个变量值
            for value in values_list:
                # ["sql注入","1=1"]
                temp_copy = copy.deepcopy(self.temp)
                desc = key + "_" + value[0]  # 生成用例描述
                self.logger.debug(desc)
                self.logger.debug(temp_copy)
                self.update_temp(temp_copy,key,value[1])  # 5.循环keys，并修改对应模板temp里的值
                self.update_temp_other(temp_copy,step,common_datas)  # 6.修改模板temp里的其他值（如fphm）
                self.logger.debug(('---update-----',temp_copy))
                case = self.update_case(common_datas,step,temp_copy,desc)  # 7.将temp加入到case中，并修改case里其他值
                mysql.insert_sql(case)  # 8.case插入到数据库中
                step += 1
            step += 12
        mysql.close()


'''
下面是不同的接口实现
'''
class Generator_S_Case(Generator):

    # 修改父类的模板
    # single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类


class Generator_M_Case(Generator):

    # 修改父类的模板
    # 测试multiple用例生成
    def __init__(self):
        super().__init__()  # 初始化父类

    def split_temp(self,temp):
        '''
        将temp拆成两部分，主信息与明细（或清单）
        :param temp:
        :return:
        '''
        temp_mx = temp['kjmxs'][0]
        return temp_mx


    # def _read_temp_data(self,path):
    #     """
    #     读取用例表中的case sheet，并返回二维列表
    #     :param path:excel所在的路径
    #     :yield :每行数据列表4生成器
    #
    #     """
    #     # 读取case sheet
    #     wb = xlrd.open_workbook(path)
    #     case_sheet = wb.sheet_by_name("case")
    #     max_row = case_sheet.nrows
    #     max_column = case_sheet.ncols
    #     for i in range(1,max_row):
    #         desc = case_sheet.cell(i,1).value
    #         key_list = case_sheet.cell(i,2).value.split('\n')
    #         value_list = case_sheet.cell(i,3).value.split('\n')
    #         # 明细数据用两层列表来存储
    #         mx_lists = list()
    #         for j in range(4,max_column):
    #             if case_sheet.cell(i,j).value !="":
    #                 mx_lists.append(case_sheet.cell(i,j).value.split('\n'))
    #             else:
    #                 break
    #         if len(mx_lists) %2 ==0:
    #             yield (desc,key_list,value_list,mx_lists)
    #         else:
    #             self.logger.error("case({}) is wrong".format(desc))
    #             break

    def _read_temp_data(self,path):
        """
        读取用例表中的case sheet，并返回二维列表
        :param path:excel所在的路径
        :yield :每行数据列表4生成器

        """
        wb = xlrd.open_workbook(path)
        case_sheet = wb.sheet_by_name("case")
        max_row = case_sheet.nrows
        max_column = case_sheet.ncols
        for i in range(1,max_row):
            key_list = list()
            value_list = list()
            desc = case_sheet.cell(i,1).value
            key = case_sheet.cell(i,2).value.split('\n')
            value = case_sheet.cell(i,3).value.split('\n')
            for v in range(len(value)):
                if (key[v] not in ["GMF_NSRSBH","GMF_MC"]) and (value[v] not in ["", 'auto']):
                    key_list.append(key[v])
                    value_list.append(value[v])
            # 明细数据用两层列表来存储
            mx_lists = list()
            for j in range(4,max_column):
                if case_sheet.cell(i,j).value !="":
                    mx_lists.append(case_sheet.cell(i,j).value.split('\n'))
                else:
                    break
            if len(mx_lists) %2 == 0:
                yield (desc,key_list,value_list,mx_lists)
            else:
                self.logger.error("case({}) is wrong".format(desc))
                break


    def generate_request_json(self,temp):
        '''
        标准的multiple用例生成，包含多明细
        :param temp:
        :return:
        '''
        file_path = os.path.join(PATH,'data','cases',self.case_excel)
        datas = self._read_temp_data(file_path)
        temp_mx = self.split_temp(self.temp)
        for data in datas:
            (desc, key_list, value_list, mx_lists) = data
            temp_copy = copy.deepcopy(temp)
            # 替换mx中的值
            for i in range(len(mx_lists[0])):
                temp_copy = search_dict_key(temp_copy,mx_lists[0][i].lower(),mx_lists[1][i])
            if len(mx_lists)>=4:
                for i in range(2,len(mx_lists),2):
                    mx = copy.deepcopy(temp_mx)
                    for j in range(len(mx_lists[i])):
                        mx = search_dict_key(mx,mx_lists[i][j].lower(),mx_lists[i+1][j])
                    temp_copy['kjmxs'].append(mx)
            # 替换head中的值
            if len(key_list) == len(value_list) :
                for i in range(len(key_list)):
                    temp_copy = search_dict_key(temp_copy, key_list[i].lower(), value_list[i])
                yield (desc, temp_copy)
            else:
                self.logger.error("case({}) is wrong".format(desc))
                return

    def generate_case_main(self):
        datas = self.generate_request_json(self.temp)
        file_path = os.path.join(PATH,'data','cases',self.case_excel)
        common_datas = self._read_common_sheet(file_path)  # 1.从excel加载公共数据
        step = int(common_datas["step"])
        mysql = OperateMysql(self.config_file, self.logger) # 2.连接数据库
        # for temp_data in temp_datas:
        for data in datas:
            desc,temp_copy = data
            self.logger.debug(desc)
            self.logger.debug(temp_copy)
            case = self.update_case(common_datas,step,temp_copy,desc)  # 3.将temp加入到case中，并修改case里其他值
            mysql.insert_sql(case)  # 4.case插入到数据库中
            step += 2
        mysql.close()


# class Generator_tycx(Generator):
#     # 针对用例单独处理
#     # 20191206将统一查询excel用例步骤及数据写入到数据库中
#     # 统一查询（ofd）
#     def __init__(self):
#         super().__init__()  # 初始化父类
#
#     def generate_request_json(self,temp,data):
#         #处理case sheet 每一行数据
#         tycx_request = json.loads(data[1])
#         fphm = tycx_request['fP_HM']
#         fpdm = tycx_request['fP_DM']
#         redis_request = "redis get speed-invoice-{}".format(fpdm+fphm)
#         mongodb_request = '''mongo invoice find {"FP_DM":"%s","FP_HM":"%s"}''' % (fpdm,fphm)
#         cj_request = '''SELECT * FROM "fp_kj" where fpdm="%s" and fphm="%s";''' % (fpdm,fphm)
#         self.logger.debug("redis_request:{}".format(redis_request))
#         self.logger.debug("mongodb_request:{}".format(mongodb_request))
#         for d in data[3:]:
#             request = ""
#             url_sql = ""
#             http_method = ""
#             if d == "":
#                 break
#             elif d.startswith("Redis查询"):
#                 url_sql = redis_request
#             elif d.startswith("大数据"):
#                 url_sql = mongodb_request
#             elif d.startswith("发票号码代码查询"):
#                 url_sql = "/services/tycx/getInvoice"
#                 request = tycx_request
#                 http_method = "post"
#             elif d.startswith("采集库中查询"):
#                 url_sql = cj_request
#             else:
#                 self.logger.error(f"未能正确处理，请确认步骤描述是否错误：{d}")
#             self.logger.debug([data[0],d,url_sql,request])
#             yield [data[0],d,url_sql,request,http_method]
#
#
#     def update_cases(self,cases,step,request):
#         #传入的request为上面函数的返回 [data[0],d,url_sql,request,http_method]
#         case = copy.deepcopy(cases)
#         case["step"] = step
#         case["test_desc"] = case["test_desc"] + '-' + request[0]
#         case["request_name"] = request[1]
#         case['url_sql'] = request[2]
#         case['http_method'] = request[4]
#         if isinstance(request[3],dict):
#             case["request_sql_param"] = json.dumps(request[3], ensure_ascii=False)
#         else:
#             case["request_sql_param"] = request[3]
#         self.logger.debug("case:{}".format(case))
#         return case


class Generator_S_FPQZ(Generator):

    # 修改父类的模板
    # 测试single用例生成
    def __init__(self):
        super().__init__()  # 初始化父类


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


class Generator_Data_FPQZ(Generator):
    # 从datas_fp读取数据生成发票签章用例
    def __init__(self,class_list):
        self.class_list = class_list
        super().__init__()  # 初始化父类

    def get_keys(self):
        config_file =os.path.join(PATH, 'config', 'data_generator.ini')
        self.mysql_conn = OperateMysql(config_file)
        (cursor,db) = self.mysql_conn.get_dict_cursor()
        values = list()
        for class_object in self.class_list:
            sql_object = class_object(None)
            values.extend(sql_object.query(cursor))
        # [{'data_id': 100, 'data_sort': '手机号规则校验', 'data_desc': '前后空格-F', 'sj': ' 158585888 '},]
        return values

    def generate_case_main(self):
        '''从数据库datas_fp中读取数据生成测试脚本'''
        values = self.get_keys()
        self.mysql_conn.close()
        case_path = os.path.join(PATH, "data", 'cases', self.case_excel)
        common_datas = self._read_common_sheet(case_path)  # 1.从excel加载公共数据
        step = int(common_datas["step"])
        mysql = OperateMysql(self.config_file, self.logger) # 3.连接数据库
        for data in values:
            fpqz = Interface_FPQZ(None, **data)
            data_dict = fpqz.interface_dict()
            # {'gmf_sj': '15610 07697'}
            desc = data['data_sort'] + data['data_desc']
            temp_copy = copy.deepcopy(self.temp)
            self.update_temp(temp_copy, **data_dict)  # 5.循环keys，并修改对应模板temp里的值
            self.update_temp_other(temp_copy, step, common_datas)  # 6.修改模板temp里的其他值（如fphm）
            self.logger.debug(('---update-----', temp_copy))
            case = self.update_case(common_datas, step, temp_copy, desc)  # 7.将temp加入到case中，并修改case里其他值
            mysql.insert_sql(case)  # 8.case插入到数据库中
            step += 1
        mysql.close()

    def update_temp(self,temp,mx_key=None,*args,**kwargs):
        if not mx_key:
            temp = search_dict(temp, **kwargs)
        else:
            pass


if __name__ =="__main__":
    # 测试generatorCase类
    # generate = Generator()
    # generate.generate_single_case()

    # 测试_read_multiple_excel
    # generate = Generator()
    # multiple_case_path = os.path.join(PATH, "data", 'cases',generate.multiple_case_excel)
    # print(multiple_case_path)
    # datas, commons = generate._read_multiple_excel(multiple_case_path)
    # print(datas)
    # 测试
    generate = Generator()
    generate.generate_case_main()