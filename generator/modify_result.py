# -*- coding: utf-8 -*-
# @Date : 2019-12-23
# @Author : water
# @Version  : v1.0
# @Desc  : 修改数据库中的expected_result，只获取想要比对的结果

import logging,json
from tool.operateMysqlClass import OperateMysql

#配置日志
logging.basicConfig(level=30, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update(step,data):
    mysql = OperateMysql(logger)
    expect = dict()
    target_key = "expected_modify"
    expect[target_key] = data
    mysql.update_sql(step,target_key,expect)
    mysql.close()


def query():
    mysql = OperateMysql(logger)
    # target_key = "expected_modify" # 用于封闭查询的字段，暂未修改
    datas = mysql.query_sql()
    mysql.close()
    return datas


def result_modify(data):
    # 获取需要比对的字段
    data = json.loads(data)
    require_list = ['code', 'fp_dm', 'fp_hm', 'hjje', 'hjse', 'msg']
    expects = dict()
    for i in data.keys():
        for j in require_list:
            if j in i:
                expects[i] = data[i]
    return json.dumps(expects,ensure_ascii=False)


def main():
    datas = query()
    for data in datas:
        step,result = data
        expect_modify = result_modify(result)
        # print(expect_modify)
        update(step,expect_modify)


if __name__ == "__main__":
    # query()
    # update(1,'','')
    # result_modify("")
    main()
