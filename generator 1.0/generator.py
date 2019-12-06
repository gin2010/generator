# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.2
# @Desc  :每次改写update_temp_single方法，更改最终传入到request_sql_param中内层报文的内容，由于不同的接口内层报文不一致，
#         因此将此方法针对不同的接口报文类型**重写**，不同的接口通过修改配置文件中模板文件temp与模板类型
#         发票采集模板使用：
#         1修改发票号码、发票代码；
#         2将内层报文参数inner_param的值修改为inner_param_value并返回
#         :param temp:内层报文（从模板文件中读取的）
#         :param step:测试用例step（从excel模板common中读取的step）
#         :param fphm:发票号码（从excel模板common中读取的起始发票号码）
#         :param inner_key:内层报文中需要更新的key（从excel模板case中读取的每一行request_param的值），相当于每次修改的字段
#         :param inner_value:内层报文中需要更新的key对应的value（GetString返回的字段值，一次传入一个）
#         :return temp: 转换为json格式的内层报文，写入到数据库request_sql_param的内容


import json,sys,os,time,random,copy,xlrd
from tool.operateMysqlClass import OperateMysql
# 添加tool工具包到系统变量中
tool = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool")
sys.path.append(tool)
from tool.generatorCase import Generator
from tool.search_dict import search_dict_key


class Generator_tjcx_kpcx(Generator):

    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        temp[inner_key] = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_tjcx_kpts(Generator):

    # 修改父类的模板
    # 统计查询接口--发票推送
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        try:
            temp = int(inner_value)
        except Exception:
            temp = inner_value
        return json.dumps(temp, ensure_ascii=False)


class Generator_fs(Generator):
    #
    # 修改父类的模板
    # 统计查询接口--开票查询
    def __init__(self):
        super().__init__()  # 初始化父类


    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        temp = copy.deepcopy(temp)
        # 非税接口item只有“0006”与“0007”，zdyxmxx只有“0008”，head和jfxx都有
        temp["head"]["djbm"] = random.choice(("0006", "0007", "0008"))
        # temp["head"]["djbm"] = random.choice(("0006", "0007"))
        # temp["head"]["djbm"] = "0008"
        if temp["head"]["djbm"] == "0006":
            # 住院票据开立
            temp["head"]["mbdm"] = "0006"
            temp.pop("zdyxmxx",False)
        elif temp["head"]["djbm"] == "0007":
            # 门诊票据开立
            temp["head"]["mbdm"] = "0007"
            temp.pop("zdyxmxx", False)
        else:
            # 财政票据开立
            temp["head"]["mbdm"] = "0009"
            temp.pop("item", False)
        temp["head"]["pjdm"] = "24" + time.strftime("%y%m") + "000241"
        if inner_key == "pjhm":
            temp = search_dict_key(temp, inner_key, inner_value)
        else:
            # head等外层用
            temp = search_dict_key(temp, inner_key, inner_value)
            # zdyxmxx里的zdyitems层使用
            # temp["zdyxmxx"]["zdyitems"][0] = search_dict_key(temp["zdyxmxx"]["zdyitems"][0], inner_key, inner_value)
            # zdyxmxx里的xmbt层使用
            # temp["zdyxmxx"]["xmbt"] = search_dict_key(temp["zdyxmxx"]["xmbt"], inner_key, inner_value)
            temp["head"]["pjhm"] = int(fphm) + step
        return json.dumps(temp, ensure_ascii=False)


class Generator_ys_xxcx(Generator):

    # 修改父类的模板
    # 51云税--客户信息查询与商品信息查询
    def __init__(self):
        super().__init__()  # 初始化父类

    # 修改父类的update_temp_single方法
    def update_temp_single(self,temp,step,fphm,inner_key,inner_value):
        temp1 = copy.deepcopy(temp)
        try:
            temp1 = search_dict_key(temp1, inner_key, inner_value)
        except Exception:
            os.exit(0)
            self.logger.error("inner_key:{} not found".format(inner_value))
        return json.dumps(temp1, ensure_ascii=False)

    # 修改父类的update_temp_multiple方法
    def update_temp_multiple(self,temp,step,fphm,inner_keys,inner_values):
        temp1 = copy.deepcopy(temp)
        for i in range(len(inner_keys)):
            temp1 = search_dict_key(temp1, inner_keys[i], inner_values[i])
        return json.dumps(temp1, ensure_ascii=False)


class Generator_ys_xxsc(Generator):

    # 修改父类的模板
    # 51云税--客户信息删除与商品信息删除
    def __init__(self):
        super().__init__()  # 初始化父类

    # 修改父类的update_temp_single方法
    def update_temp_single(self, temp, step, fphm, inner_key, inner_value):
        temp1 = copy.deepcopy(temp)
        step = int(step)
        try:
            if inner_key != "bm":
                temp1 = search_dict_key(temp1, inner_key, inner_value)
                temp1["datagram"]["bm"] = str(step-40000)
            else:
                temp1 = search_dict_key(temp1, inner_key, inner_value)
        except Exception:
            os.exit(0)
            self.logger.error("inner_key:{} not found".format(inner_value))
        return json.dumps(temp1, ensure_ascii=False)

    # 修改父类的update_temp_multiple方法
    def update_temp_multiple(self, temp, step, fphm, inner_keys, inner_values):
        temp1 = copy.deepcopy(temp)
        for i in range(len(inner_keys)):
            temp1 = search_dict_key(temp1, inner_keys[i], inner_values[i])
        return json.dumps(temp1, ensure_ascii=False)


class Generator_ys_xxxz(Generator):

    # 修改父类的模板
    # 51云税--客户信息新增、修改与商品信息新增、修改
    # 新增的需要把下面的“每次生成新的编号”注释关闭
    # 修改的如果不想变化编号，则把“每次生成新的编号”注释
    def __init__(self):
        super().__init__()  # 初始化父类

    # 修改父类的update_temp_single方法
    def update_temp_single(self, temp, step, fphm, inner_key, inner_value):
        temp1 = copy.deepcopy(temp)
        step = int(step)
        try:
            if inner_key != "bm":
                temp1 = search_dict_key(temp1, inner_key, inner_value)
                # 每次生成新的编号
                # temp1["datagram"]["bm"] = str(step)
            else:
                temp1 = search_dict_key(temp1, inner_key, inner_value)
        except Exception:
            os.exit(0)
            self.logger.error("inner_key:{} not found".format(inner_value))
        return json.dumps(temp1, ensure_ascii=False)

    # 修改父类的update_temp_multiple方法
    def update_temp_multiple(self, temp, step, fphm, inner_keys, inner_values):
        temp1 = copy.deepcopy(temp)
        temp1["datagram"][inner_keys[0]] = inner_values[0]
        temp1["datagram"]["bm"] = str(step)
        return json.dumps(temp1, ensure_ascii=False)



class Generator_ys_xxxz_pd(Generator):

    # 修改父类的模板
    # 51云税--客户信息新增与商品信息新增 铺底数据
    # 需要修改“名称”字段
    def __init__(self):
        super().__init__()  # 初始化父类

    # 修改父类的update_temp_single方法
    def generate_single_case(self):
        single_case_path = os.path.join(self.generate_path, "data", self.single_case_excel)
        case_datas, common_datas = self._read_single_excel(single_case_path)
        self.logger.debug([case_datas, common_datas])
        step = int(common_datas["step"])
        length = int(common_datas["fphm_start"])
        ghfmc = str(copy.deepcopy(self.temp['datagram']['xmmc']))
        # 连接mysql数据库
        opsql = OperateMysql(self.logger)
        for l in range(1,length+1):
            step += 1
            common_datas["step"] = step
            common_datas["request_name"] = common_datas["test_desc"] + "--" + str(l)
            self.temp['datagram']['bm'] = str(step)
            self.temp['datagram']['xmmc'] = ghfmc + str(step)
            common_datas["request_sql_param"] = json.dumps(self.temp, ensure_ascii=False)
            opsql.insert_sql(common_datas)
        opsql.close()


class Generator_ys_xxsc_pd(Generator):

    # 修改父类的模板
    # 51云税--客户信息删除与商品信息删除 铺底数据
    def __init__(self):
        super().__init__()  # 初始化父类

    # 修改父类的update_temp_single方法
    def generate_single_case(self):
        single_case_path = os.path.join(self.generate_path, "data", self.single_case_excel)
        case_datas, common_datas = self._read_single_excel(single_case_path)
        self.logger.debug([case_datas, common_datas])
        step = int(common_datas["step"])
        length = int(common_datas["fphm_start"])
        # 连接mysql数据库
        opsql = OperateMysql(self.logger)
        for l in range(1,length+1):
            step += 1
            common_datas["step"] = step
            common_datas["request_name"] = common_datas["test_desc"] + "--" + str(l)
            self.temp['datagram']['bm'] = str(step -1000).zfill(5)
            common_datas["request_sql_param"] = json.dumps(self.temp, ensure_ascii=False)
            opsql.insert_sql(common_datas)
        opsql.close()


class Generator_ys_xxsc_pd_id(Generator):

    # 修改父类的模板
    # 51云税--客户信息与商品信息删除固定ID
    # 新增的需要把下面的“每次生成新的编号”注释关闭
    # 修改的如果不想变化编号，则把“每次生成新的编号”注释
    def __init__(self):
        super().__init__()  # 初始化父类


    def generate_single_case(self):
        single_case_path = os.path.join(self.generate_path, "data", self.single_case_excel)
        case_datas, common_datas = self._read_single_excel(single_case_path)
        self.logger.debug([case_datas, common_datas])
        step = int(common_datas["step"])
        wb = xlrd.open_workbook("./data/id.xls")
        ws = wb.sheet_by_index(0)
        max_row = ws.nrows
        # 连接mysql数据库
        opsql = OperateMysql(self.logger)
        for l in range(max_row):
            step += 1
            common_datas["step"] = step
            bm = ws.cell(l,0).value
            common_datas["request_name"] = common_datas["test_desc"] + "-bm-" + str(bm)
            if isinstance(bm,float):
                self.temp['datagram']['bm'] = str(int(bm))
            else:
                self.temp['datagram']['bm'] = str(bm)
            common_datas["request_sql_param"] = json.dumps(self.temp, ensure_ascii=False)
            opsql.insert_sql(common_datas)
        opsql.close()


class Generator_ys_xxxz_pd_id(Generator):

    # 修改父类的模板
    # 51云税--客户信息与商品信息新增与删除固定ID
    # 新增的需要把下面的“每次生成新的编号”注释关闭
    # 修改的如果不想变化编号，则把“每次生成新的编号”注释
    def __init__(self):
        super().__init__()  # 初始化父类


    def generate_single_case(self):
        single_case_path = os.path.join(self.generate_path, "data", self.single_case_excel)
        case_datas, common_datas = self._read_single_excel(single_case_path)
        self.logger.debug([case_datas, common_datas])
        step = int(common_datas["step"])
        max_row = 1009
        # 连接mysql数据库
        opsql = OperateMysql(self.logger)
        for l in range(max_row):
            step += 1
            common_datas["step"] = step
            common_datas["request_name"] = common_datas["test_desc"] + "-bm-" + str(l)
            self.temp['datagram']['bm'] = str(l+1000)
            common_datas["request_sql_param"] = json.dumps(self.temp, ensure_ascii=False)
            opsql.insert_sql(common_datas)
        opsql.close()


if __name__ == "__main__":
    # 统计查询接口--开票查询
    # generate = Generator_tjcx_kpcx()
    # generate.generate_single_case()

    # 统计查询接口--发票推送
    # generate = Generator_tjcx_kpts()
    # generate.generate_single_case()

    # 统一查询接口--发票号码查询
    generate = Generator_tjcx_kpts()
    generate.generate_single_case()

    # 非税接口
    # generate = Generator_fs()
    # generate.generate_single_case()  # 生成单个字段的用例
    # generate.generate_multiple_case()  # 生成多字段用例

    # 51云税 客户信息查询/商品信息查询
    # generate = Generator_ys_xxcx()
    # generate.generate_single_case()  # 生成单个字段的用例

    # 51云税 客户信息删除/商品信息删除
    # generate = Generator_ys_xxsc()
    # generate.generate_single_case()

    # 51云税 客户信息新增、修改/商品信息新增、修改
    # generate = Generator_ys_xxxz()
    # generate.generate_single_case()
    # generate.generate_multiple_case()

    # 51云税 客户信息新增/商品信息新增（铺底数据）
    # generate = Generator_ys_xxxz_pd()
    # generate.generate_single_case()

    # 51云税 客户信息删除/商品信息删除（铺底数据）
    # generate = Generator_ys_xxsc_pd()
    # generate.generate_single_case()

    # 51云税 客户信息删除/商品信息删除（铺底数据传入固定的bm）
    # generate = Generator_ys_xxsc_pd_id()
    # generate.generate_single_case()

    # 51云税 客户信息删除/商品信息新增（铺底数据用于测试查询）
    # generate = Generator_ys_xxxz_pd_id()
    # generate.generate_single_case()

