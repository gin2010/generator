# -*- coding: utf-8 -*-
# @Date : 2020-01-14
# @Author : water
# @Version  : v1.0
# @Desc  :

import os,configparser
from logSetClass import Log
import xlrd,copy,json

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # data_generator路径
class GenerateDatas(object):

    def __init__(self):

        log_name = "data_generator.log"
        log_file = os.path.join(PATH, 'log', log_name)
        config_file = os.path.join(PATH,'config','data_generator.ini')
        # 加载配置文件
        config = configparser.RawConfigParser()
        config.read(config_file,encoding="utf-8")
        # 加载配置文件--日志配置
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        # 加载配置文件--excel路径
        self.data_excel = os.path.join(PATH,'data',config.get("excel_name","data_excel"))
        # 加载配置文件--step
        self.step = config.get("excel_name","step")
        # 加载配置文件--模板temp
        temp_file = config.get("template","temp")
        temp_path = os.path.join(PATH,'config',temp_file)
        with open(temp_path,'r') as f:
            self.template = json.load(f)
            print(self.template)
            print(type(self.template))

    def _read_excel(self):
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
        ws = wb.sheet_by_name("yhzc_gz")
        max_row = ws.nrows
        for row in range(1,max_row):
            yield ws.row_values(row)


    def yhzc_2_database(self):
        datas = self._read_excel()
        id = int(self.step)
        for data in datas:
            temp = copy.deepcopy(self.template)
            data_desc = data[1]
            temp['data_sort'] = "发票优惠政策规则校验"
            temp['mx_yhzcbs'] = data[2]
            temp['mx_lslbz'] =data[3]
            temp['mx_zzstsgl'] = data[1]
            temp['mx_hsbz'] = 0
            temp['mx_kce'] = None
            temp['mx_spbm'] = "1010101070000000000"
            slv_list = data[4].replace('，',',').split(",")
            for slv in slv_list:
                flag = '-F'
                if slv in data[4]:
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
                print(temp)

    @staticmethod
    def percent_2_float(str):
        if '%' in str:
            return float(str.strip("%"))/100
        else:
            return float(str)

def main():
    yhzc = GenerateDatas()
    yhzc.yhzc_2_database()

if __name__ == "__main__":
    main()