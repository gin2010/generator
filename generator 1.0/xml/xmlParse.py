# -*- coding: utf-8 -*-
# @Date : 2019/09/26
# @Author : water
# @Version  : v1.0
# @Desc  : 读取xml文件夹，将里面的xml用例文件的bh、caseName提取出来，并保存到excel表格里

from bs4 import BeautifulSoup
import logging,json,os
from xml2dict import encoder
import xlwt


XML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hztestcase.xml")
DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"invoicecancel")
RESULT_XLS = os.path.join(os.path.dirname(os.path.abspath(__file__)),"invoicecancel.xls")

# 程序运行日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_xml_get_bh(filepath):
    """
    :param filepath: xml文件地址
    :return: 返回testcase.xml中的Bh与casename
    """
    with open(filepath,'r')  as f:
        bh_casename= list()
        xml = encoder.XML2Dict()
        datas = xml.parse(f.read())
        for data in datas["Data"]["TestCase"]:
            if isinstance(data["Bh"],bytes):
                bh_casename.append([data["Bh"].decode("utf-8"),data['CaseName'].decode("utf-8")])
        return bh_casename

def get_dir_file(dirpath):
    """
    :param dirname: 输入testcase目录，获取里面全部xml名并组成filepath列表返回
    :return: 全部xml的路径列表
    """
    files = list()
    for dir,_,file in os.walk(dirpath):
        if len(file)>0:
            for i in file:
                each_file = os.path.join(dir,i)
                files.append(each_file)
        else:
            continue
    return files


def write_data_to_excel(datas,path,sheet_name="data"):
    """
    将datas列表中的内容写入到xls里面
    :param datas: 需要写入的数据
    :param sheet_name: 写入的sheet名，默认为data
    :return: none
    """
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet(sheet_name)
    # 写入excel
    # 参数对应 行, 列, 值
    worksheet.write(0,0,label="BH")
    worksheet.write(0,1,label="CaseName")
    for i in range(len(datas)):
        worksheet.write(i+1, 0, label=datas[i][0])
        worksheet.write(i+1, 1, label=datas[i][1])
    # 保存
    workbook.save(path)

if __name__ == "__main__":
    bh_casenames = list()
    for each in get_dir_file(DIR_PATH):
        bh_casenames.extend(load_xml_get_bh(each))
    write_data_to_excel(bh_casenames,RESULT_XLS)
