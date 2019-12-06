# -*- coding: utf-8 -*-
# @Date : 2019/09/19
# @Author : water
# @Version  : v1.0
# @Desc  :读取casedata、checkdata、testcase中的数据

import os
import logging
from bs4 import BeautifulSoup

# 程序运行日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
CHECKPOINT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"DZCheckData_基础数据.xml")
CASEDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hztestcase.xml")


def read_xml_return_listdict(xml_path,main_tag,keys):
    with open(xml_path,'r') as f:
        bs = BeautifulSoup(f,'lxml')
    # print(bs.checkpoint) #取checkpoint节点及所有后代
    # print(bs.checkpoint.name) #取checkpoint节点名字
    # print(bs.checkpoint.code.string) #取节点的内容必须是末级节点，否则返回NONE
    # print(bs.checkpoint.code.contents)
    print(type(bs))
    xml_datas = list()
    for child in bs.find_all("checkpoint"):
        print("---------start----------")
        d = dict()
        if not child.databh is None:
            d[child.databh.name] = child.databh.string
        if not child.code is None:
            d[child.code.name] = child.code.string
        if not child.msg is None:
            d[child.msg.name] = child.msg.string
        xml_datas.append(d)
        print("----------over-----------")
    logger.info(xml_datas)

    logger.info("xml finish")
    return xml_datas


def read_xml_return_listdict_all(xml_path):
    with open(xml_path,'r') as f:
        bs = BeautifulSoup(f,'lxml')
    # print(bs.checkpoint) #取checkpoint节点及所有后代
    # print(bs.checkpoint.name) #取checkpoint节点名字
    # print(bs.checkpoint.code.string) #取节点的内容必须是末级节点，否则返回NONE
    # print(bs.checkpoint.code.contents)
    xml_datas = list()
    for child in bs.find_all("testcase"):
        print("---------start----------")
        print(child)
        d = dict()
        l_key= ['Bh','CaseName']
        l_value = list()
        l_key = deep_search(child,l_key)
        print(l_value,l_value)
        # xml_datas.append(d)
        print("----------over-----------")
    logger.info(xml_datas)

    logger.info("xml finish")
    return xml_datas


def deep_search(child,l):
    for gchild in child.children:
        if not gchild.name is None:
            l.append(gchild.name)
            if has_child(gchild):
                deep_search(gchild,l)
    return l


def has_child(tag):
    l = list()
    for child in tag.children:
        if not child.name is None:
            l.append(child.name)
    if len(l) == 0:
        return False
    else:
        return True


if __name__ == "__main__":
    # xml_datas = read_xml_return_listdict(CHECKPOINT_PATH,"checkpoint",['databh','code','msg'])
    read_xml_return_listdict_all(CASEDATA_PATH)
    # print(xml_datas)
    # print(type(xml_datas))