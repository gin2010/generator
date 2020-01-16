# -*- coding: utf-8 -*-
# @Date : 2020-01-09
# @Author : water
# @Version  : v1.0
# @Desc  :111
import configparser,os,logging


PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ModelMetaclass(type):
    def __new__(cls, name,bases,attrs):
        mappings = dict()
        # print("--attrs--",attrs)
        for k,v in attrs.items():
            if isinstance(v,tuple):
                mappings[k] = v
        # print("mappings---->",mappings)
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name.lower()
        # print("attrs---->",attrs)
        return super().__new__(cls,name,bases,attrs)


class Model(metaclass=ModelMetaclass):

    def __init__(self,logger,**kwargs):
        # 初始化实例对象中的变量
        # self.kwargs = kwargs
        for k,v in kwargs.items():
            setattr(self,k,v)

        # 加载data_generator.ini配置文件
        config_file = os.path.join(PATH, "config", "data_generator.ini")
        config = configparser.RawConfigParser()
        config.read(config_file, encoding="utf-8")  # 读取文件
        log_level = config.get('logging','level')
        # 日志配置
        if logger != None:
            self.logger = logger
        else:
            logging.basicConfig(level=int(log_level), format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)

        # logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        # self.logger = logging.getLogger(__name__)


    def insert(self,cursor,db):
        '''
        __mappings__:{'data_id': ('data_id', 'int(11)'),...} Yhzc_GZ类中变量与值组成的字段
        getattr(self,k,None)：实例对象中传入的字段在self.__dict__里可以查看，或self.kwargs
        :return:
        '''
        fields = list() # 元组里的实现数据库里字段
        args = list()  # Yhzc_GZ类对象中变量名
        self.logger.debug(self.__mappings__)
        for k,v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self,k,None))  # 从k里取出对应变量实际的值
        args_temp = list()
        for temp in args:
            if isinstance(temp,str):
                args_temp.append('"%s"' % temp)
            else:
                args_temp.append(str(temp))
        args_temp = [x.replace('None','Null') for x in args_temp] # 将none替换为Null
        sql = 'insert into %s (%s) values (%s)'% (self.__table__,','.join(fields),','.join(args_temp))
        self.logger.debug(sql)
        cursor.execute(sql)
        db.commit()
        self.logger.info('--数据插入成功--')

    def query(self,cursor,db):
        pass

    def updata(self,cursor,db):
        pass

    def remove(self,cursor,db):
        pass

    def interface_dict(self):
        fields = dict()  # 元组里的实现数据库里字段
        self.logger.warning(self.__mappings__)
        for k, v in self.__mappings__.items():
            fields[v[0]] = getattr(self, k, None) # 从k里取出对应变量实际的值
        return fields


class Yhzc_GZ(Model):
    # djange里面用的类来实现下面数据库表的列
    data_id = ("data_id", "int(11)")
    data_sort = ("data_sort", "varchar(255)")
    data_desc = ("data_desc", "varchar(255)")
    jshj = ("jshj", "double(20,2)")
    hjje = ("hjje", "double(20,2)")
    hjse = ("hjse", "double(20,2)")
    mx_xmdj = ("mx_xmdj", "double(24,8)")
    mx_xmje = ("mx_xmje", "double(20,2)")
    mx_se = ("mx_se", "double(24,8)")
    mx_slv = ("mx_slv", "double(24,8)")
    mx_hsbz = ("mx_hsbz", "char(1)")
    mx_yhzcbs = ("mx_yhzcbs", "char(1)")
    mx_lslbs = ("mx_lslbs", "char(1)")
    mx_zzstsgl = ("mx_zzstsgl", "varchar(255)")
    mx_kce = ("mx_kce", "double(20,2)")
    mx_spbm = ("mx_spbm", "varchar(255)")


class SJ_GZ(Model):
    data_id = ("data_id", "int")
    data_sort = ("data_sort", "varchar(255)")
    data_desc = ("data_desc", "varchar(255)")
    data_key =  ("sj",'varchar(255)')


class FPQZ(Model):
    # datas_fp数据库字段名=接口字段名
    sj = ("gmf_sj", "none")
    nsrsbh = ("gmf_nsrsbh","none")
    nsrsbh = ("xsf_nsrsbh","none")


if __name__ == "__main__":
    # data = {
    #     'jshj': 10150.0,
    #     'hjje': 10000,
    #     'hjse': 150.0,
    #     'mx_xmsl': 1,
    #     'mx_xmdj': 10000,
    #     'mx_xmje': 10000,
    #     'mx_slv': 0.015,
    #     'mx_se': 150.0,
    #     'mx_hsbz': 0,
    #     'mx_fphxz': '0',
    #     'mx_spbm': '1010101070000000000',
    #     'mx_yhzcbs': 1,
    #     'mx_lslbs': '',
    #     'mx_zzstsgl': '普通零税',
    #     'mx_kce': None,
    #     'data_sort': '发票优惠政策规则校验',
    #     'mx_lslbz': 3.0,
    #     'data_id': 1311,
    #     'data_desc': '普通零税-税率为1.5%-T'
    # }
    # yhzc = Yhzc_GZ(None,**data)
    # yhzc.insert()
    data = {"sj":"1558868411",'nsrsbh':"913702008636074111"}
    fpqz = FPQZ(None,**data)
    print(fpqz.interface_dict())