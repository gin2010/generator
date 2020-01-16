# -*- coding: utf-8 -*-
# @Date : 2019-12-31
# @Author : water
# @Version  : v1.0
# @Desc  :read_excel导出用例为xls格式，过滤出expected_result中的code、msg
#         result_2_excel从mysql数据库中读取用例及结果，过滤出expected_result中的code、msg

import xlrd,xlwt,json,pymysql,os,time

need_keys = ['code','msg','returnMessage','returnCode',]
path = "./123456.xls"
PATH = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(PATH,"result","fpqz_result20200109.xls")

def read_excel(path,):
    wb = xlrd.open_workbook(path,)
    ws = wb.sheet_by_name("question")
    max_row = ws.nrows
    wb_new = xlwt.Workbook(encoding='utf-8')
    sheet = wb_new.add_sheet("result", cell_overwrite_ok=True)
    sheet.write(0, 0, ws.cell(0,0).value)  # 写入标题
    sheet.write(0, 1, ws.cell(0,1).value)  # 写入标题
    sheet.write(0, 2, ws.cell(0,2).value)  # 写入标题
    for i in range(1,max_row):
        result = dict()
        result = ws.cell(i,2).value
        result = filter(result,need_keys)
        sheet.write(i, 0, ws.cell(i,0).value)
        sheet.write(i, 1, ws.cell(i,1).value)
        sheet.write(i, 2, result)
    wb_new.save(output_file)


def read_from_mysql(case_id,*args):
    mysql = pymysql.connect(
        host="192.168.2.19",
        port=3306,
        user="devtest",
        password="Sa!@#$%^",
        database="51fppt_test"
    )
    # 使用cursor()方法创建一个游标对象
    cursor = mysql.cursor()
    print("connect mysql successful!!")
    sql = "SELECT {} FROM `step_data` where case_id={};".format(",".join(args),case_id)
    # sql = "SELECT case_id,step,expected_result FROM `step_data` where case_id=24000007;"
    print(sql)
    cursor.execute(sql)
    # data = cursor.fetchmany(3) # 查询三条记录
    # data = cursor.fetchone()  # 查询单条
    data = cursor.fetchall()  # 查询全部
    # mysql.commit() # 查询的不用commit
    cursor.close()
    mysql.close()
    return data  # 二维元组

def result_2_excel():
    keys = ["step","test_desc","expected_result"]
    case_id = "24000007"
    wb_new = xlwt.Workbook(encoding='utf-8')
    sheet = wb_new.add_sheet("result", cell_overwrite_ok=True)
    length = len(keys)
    # 写入标题
    for c in range(length):
        sheet.write(0,c,keys[c])
    datas = read_from_mysql(case_id,*keys)
    for r in range(len(datas)):
        # print(datas[r])
        sheet.write(r+1,0,datas[r][0])
        sheet.write(r+1,1,datas[r][1])
        if datas[r][2] != "":
            sheet.write(r+1,2,filter(datas[r][2],need_keys))
    wb_new.save(output_file)
    print("------------finish----------------")

def filter(result,need_keys):
    result_dict = json.loads(result)
    # print(result_dict)
    result = dict()
    for key in result_dict.keys():
        for k in need_keys:
            if k in key:
                result[key] = result_dict[key]
                # print(result)
                break
    return json.dumps(result,ensure_ascii=False)

def update_expected_modify():
    '''修改expected_result，然后写入到expected_modify中'''
    keys = ["step" , "expected_result"]
    remain_keys = ["code",'msg']
    delete_keys = ["[datagram][file]","[access_token]"]
    case_id = "24000008"
    mysql = pymysql.connect(
        host="192.168.2.19",
        port=3306,
        user="devtest",
        password="Sa!@#$%^",
        database="51fppt_test"
    )
    # 使用cursor()方法创建一个游标对象
    cursor = mysql.cursor()
    print("mysql connect successfully")
    datas = read_from_mysql(case_id,*keys)
    for data in datas:
        data_list = list()
        data_list.append(data[0])
        # print(data)
    # 只保留remain_keys里的值
        data_list.append(filter(data[1],remain_keys).replace("'","\\'"))
        # print(data_list)
        sql = "update `step_data` set expected_modify = '{}' where case_id ={} and step = {};".format(data_list[1], case_id,data_list[0])
        print(sql)
        cursor.execute(sql)
    mysql.commit()
    print("修改expect成功！！！")
    cursor.close()
    mysql.close()


def main():
    # read_excel(path)
    # result_2_excel()
    update_expected_modify()

if __name__ == "__main__":
    main()
