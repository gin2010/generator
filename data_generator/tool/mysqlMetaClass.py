# -*- coding: utf-8 -*-
# @Date : 2020-01-09
# @Author : water
# @Version  : v1.0
# @Desc  :

import pymysql

class MysqlMetaClass(type):
    '''
    定义数据库元类
    将变量全部封装在__attrs__里
    将表名封装在__table__里（默认类名为数据库表名）
    '''
    def __new__(cls, name,p_class,attrs):
        all_attrs = dict()
        for k,v in attrs.items():
            if not k.startswith("__"):
                all_attrs[k] = v
        print("all_attrs---->",all_attrs)
        for k in all_attrs.keys():
            attrs.pop(k)
        attrs['__attrs__'] = all_attrs
        attrs['__table__'] = name.lower()
        print("attrs---->",attrs)
        return super().__new__(cls,name,p_class,attrs)


class Model(metaclass=MysqlMetaClass):
    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v) # 初始化实例对象中的变量

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def query(self):
        pass


class Step_Data(Model):
    # djange里面用的类来实现下面数据库表的列
    case_id = ("case_id","int(11)")
    step = ("step","int(11)")
    test_desc = ("test_desc","varchar(2000)")
    step_refer = ("step_reference","varchar(100)")
    http_method = ("http_method","varchar(10)")
    headers = ("headers","varchar(3000)")
    url = ("url_sql","varchar(3000)")
    temp = ("request_sql_param","text")
    out_put = ("out_put","longtext")
    request_name = ("request_name","varchar(100)")
    aoto = ("aoto_replace","int(11)")
    my_expect = ("expected_modify","longtext")
    auto_expect = ("expected_result","longtext")


def main():
    case = {
        "case_id": 24230004,
        "step": 1000,
        "test_desc": "测试orm实现",
        "http_method": "post",
        "url_sql": "/saveinvoice",
        "temp": {"fphm":24190001,"fhdm":241900010001},
        "out_put": "",
        "request_name": "测试"
    }
    t = Step_Data(**case)
    print(t.test_desc)
    t.insert()

if __name__ == "__main__":
    main()
