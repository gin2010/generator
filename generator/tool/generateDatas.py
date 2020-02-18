# -*- coding: utf-8 -*-
# @Date : 2020-01-14
# @Author : water
# @Version  : v1.0
# @Desc  :

import os,configparser,time
from logSetClass import Log
import xlrd,copy,json
from mysqlOrm import Yhzc_GZ,SJ_GZ,Email_GZ
from operateMysqlClass import OperateMysql

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # data_generator路径
class GenerateDatas(object):

    def __init__(self):
        time_str = time.strftime('%Y%m%d%H%M',time.localtime())
        log_name = "data_generator_" + time_str + ".log"
        log_file = os.path.join(PATH, 'log', log_name)
        self.config_file = os.path.join(PATH,'config','data_generator.ini')
        # 加载配置文件
        config = configparser.RawConfigParser()
        config.read(self.config_file,encoding="utf-8")
        # 加载配置文件--日志配置
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        # 加载配置文件--excel路径
        self.data_excel = os.path.join(PATH,'data','datas',config.get("excel_name","data_excel"))
        # 加载配置文件--step
        self.step = config.get("excel_name","step")
        # 加载配置文件--模板temp
        temp_file = config.get("template","temp")
        temp_path = os.path.join(PATH,'temp','datas',temp_file)
        with open(temp_path,'r') as f:
            self.template = json.load(f)
            self.logger.debug(self.template)
            self.logger.debug(type(self.template))


    def _read_excel(self,sheet_name):
        '''
        读取excel里的数据，按行返回list类型
        :return:
        [
        'UCSEC13.8.3',
        '100%先征后退',
         1.0,
         '',
         '17%,16%,11%,10%,13%,9%,6%,5%,4%,3%,1.5%,0%,1%,15%',
         '1.开票申请可以添加此优惠政策\n2.此优惠政策支持税率：17%13%11%6%5%4%3%0%',
         '暂不支持0%',
         '']
        '''
        wb = xlrd.open_workbook(self.data_excel)
        ws = wb.sheet_by_name(sheet_name)
        max_row = ws.nrows
        for row in range(1,max_row):
            yield ws.row_values(row)


    def yhzc_2_database(self):
        '''
        data: [
        'UCSEC13.8.3',
        '100%先征后退',
         1.0,
         '',
         '17%,16%,11%,10%,13%,9%,6%,5%,4%,3%,1.5%,0%,1%,15%',
         '1.开票申请可以添加此优惠政策\n2.此优惠政策支持税率：17%13%11%6%5%4%3%0%',
         '暂不支持0%',
         '']

        '''
        # 连接数据库
        mysql_conn = OperateMysql(self.config_file)
        (cursor,db) = mysql_conn.get_attr()

        # 读取excel数据
        datas = self._read_excel("yhzc_gz")
        id = int(self.step)
        for data in datas:
            temp = copy.deepcopy(self.template)
            data_desc = data[1]
            temp['data_sort'] = "发票优惠政策规则校验"
            temp['mx_yhzcbs'] = int(data[2])
            temp['mx_lslbz'] =data[3]
            temp['mx_zzstsgl'] = data[1]
            temp['mx_hsbz'] = 0
            temp['mx_kce'] = None
            temp['mx_spbm'] = "1010101070000000000"
            slv_list = data[4].replace('，',',').split(",")
            for slv in slv_list:
                flag = '-F'
                if slv in data[5]:
                    flag = '-T'
                temp['mx_slv'] = self.percent_2_float(slv)
                temp['mx_xmje'] = 10000
                temp['mx_xmdj'] = 10000
                temp['mx_xmsl'] = 1
                temp['mx_se'] = self.percent_2_float(slv) * 10000
                temp['hjje'] = temp['mx_xmje']
                temp['hjse'] = temp['mx_se']
                temp['jshj'] = temp['hjse'] + temp['hjje']
                temp['data_id'] = id
                temp['data_desc'] = data_desc + "-税率为" + slv + flag
                id += 1
                self.logger.debug(temp)
                yhzc_table = Yhzc_GZ(self.logger,**temp)
                yhzc_table.insert(cursor,db)
                self.logger.warning('data_id:{}--->成功'.format(temp['data_id']))
            id += 12 # 用例数据之间留12个位置
        mysql_conn.close()


    def single_2_database(self):
        '''
        data
        ['UCSEC1.2.16.94', '正常11位199开头', '19989898989', 'GMF_SJ=19989898989']
        '''
        # 连接数据库
        mysql_conn = OperateMysql(self.config_file)
        (cursor,db) = mysql_conn.get_cursor()

        # 加载excel数据
        datas = self._read_excel('email') #2
        id = int(self.step)
        for data in datas:
            temp = dict()
            data_desc = data[1]
            temp['data_id'] = id
            temp['data_sort'] = "邮箱规则校验" #1
            temp['nsrsbh'] =data[2] # 4改为对应数据库字段
            flag = '-F'
            if data[1].startswith("正常"):
                flag = '-T'
            temp['data_desc'] = data_desc + flag
            id += 2
            self.logger.debug(temp)
            sj_table = Email_GZ(self.logger, **temp) # 3
            sj_table.insert(cursor,db)
            self.logger.warning('data_id:{}--->成功'.format(temp['data_id']))
        mysql_conn.close()

    @staticmethod
    def percent_2_float(str):
        if '%' in str:
            return float(str.strip("%")) / 100
        else:
            return float(str)


if __name__ == "__main__":
    yhzc = GenerateDatas()
    yhzc.yhzc_2_database()

