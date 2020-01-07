# -*- coding: utf-8 -*-
# File  : OperateMysqlClass.py
# Author: water
# Date  : 2019/9/11

import pymysql,configparser
import logging,os,json
#from logSetClass import Log


class OperateMysql:

    def __init__(self,logger=None):
        CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config","generator.ini")
        # 加载generator.ini
        config = configparser.RawConfigParser()
        config.read(CONFIG_FILE,encoding="utf-8")  # 读取文件

        # 日志配置
        if logger != None:
            self.logger = logger
        else:
            logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
        '''
        20191012单独在每个文件中配置一份，会出现重复打印的问题
        log_name = "generator.log"
        log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log', log_name)
        log_level = int(config.get("logging", "level"))
        log = Log(log_file,log_level)
        self.logger = log.control_and_file()
        '''
        """
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        """
        # 加载数据库地址
        host = config.get("mysql","host")
        port = int(config.get("mysql","port"))
        user = config.get("mysql","user")
        password = config.get("mysql","password")
        database = config.get("mysql","database")
        self.logger.debug([host,port,user,password,database])

        #连接数据库
        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        #使用cursor()方法创建一个游标对象
        self.cursor = self.db.cursor()
        self.logger.warning("connect mysql successful!!")


    #关闭游标和数据库的连接
    def close(self):
        self.cursor.close()
        self.db.close()
        self.logger.warning("mysql closed!!")


    def insert_sql(self,data):
        # 插入数据
        sql = '''INSERT INTO step_data (case_id, step,test_desc,http_method,url_sql,out_put,request_sql_param,request_name) VALUES ('{case_id}','{step}','{test_desc}','{http_method}','{url_sql}','{out_put}','{request_sql_param}','{request_name}')'''
        sql = sql.format(**data)
        self.logger.info(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.logger.warning(f"case_id:{data['case_id']}&step:{data['step']}&&{data['request_name']}-->插入成功")


    def update_sql(self,step,target_key,data):
        # 修改数据
        sql = '''update step_data set %s = '{expected_modify}' where case_id=1116008 and step = %s;'''%(target_key,step)
        sql = sql.format(**data)
        self.logger.info(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.logger.warning(f"step:{step} -->修改成功！")


    def query_sql(self,):
        sql = "SELECT step,expected_result FROM `step_data` where case_id=1116008;"
        self.logger.info(sql)
        self.cursor.execute(sql)
        # data = self.cursor.fetchmany(3) # 查询三条记录
        # data = self.cursor.fetchone()  # 查询单条
        data = self.cursor.fetchall()  # 查询全部
        self.db.commit()
        self.logger.warning(f"查询数据成功！")
        return data


if __name__ =="__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    opsql = OperateMysql(logger)
    case_id = 24230002
    step = 11
    test_desc = "测试数据库2"
    http_method = "post"
    url_sql = ""
    out_put = ""
    request_sql_param = json.dumps({
        "YFPDM": "1238",
        "JQBH": "661505060904",
        "KPY": "开票员",
        "SKY": None,
        # None值在插入数据库的时候会转成Null
        "FHR": "复核人",
        "SWJG_DM": "111019201",
        "SPHSL": "1",
        "FP_ZLDM": "2",
        "VERSION": "1",
        "XSF_DZ": "北京市海淀区春晖园2号楼",
        "XSF_DH": "123123123",
        "XSF_YH": "1236",
        "XSF_YHZH": "招商银行"},ensure_ascii=False)

    request_name = 0
    data = {
        "case_id": case_id,
        "step": step,
        "test_desc": test_desc,
        "http_method": http_method,
        "url_sql": url_sql,
        "request_sql_param": request_sql_param,
        "out_put": out_put,
        "request_name": request_name
    }
    opsql.insert_sql(data)
    opsql.close()