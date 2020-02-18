# -*- coding: utf-8 -*-
# @Date : 2019/09/19
# @Author : water
# @Desc  :对于多层字典，查找里面的key，并替换掉对应的value。字典内部可能还嵌套列表+字典结构
# @Version  : v1.0

TEMPLATE = {
    "FPXX": {
        "FP_KJ": {
            "FPQQLSH": "10780194078",
            "XSF_NSRMC": "赤井公司",
            "XSF_NSRSBH": "110101N1KRX0F08",
            "FPDM": "241909000240",
            "FPHM": "19081601",
            "KPRQ": "2019-08-11 14:17:39",
            "DDH": "11111111117",
            "DSF_PTBM": "11111111",
            "SGBZ": "1",
            "QDXMMC": "1232",
            "SKM": "12323354657677",
        },
        "FP_KJ_MX": [
            {
                "SPHXH": "01",
                "SPMC": "华为手机",
                "SPSL": "1.00000000",
                "SPJE": "1024.79",
                "SPDJ": "1024.78632479",
                "DW": "1231",
                "FPHXZ": "1"
            }
        ],
        "FP_WLXX": [
            {
                "CYGS": "承运公司",
                "WLDH": "123123123",
                "SHDZ": "测试送货地址",
                "SHSJ": "2019-08-01 14:17:11"
            }
        ],
        "FP_ZFXX": {
            "ZFFS": "测试支付方式",
            "ZFPT": "测试支付平台",
            "ZFLSH": "12312312367"
        }
    }
}


def search_dict_key(temp,target_key,target_value):
    # target_key两边空格可能会影响字典相应值的查询
    for k in temp:
        if k == target_key.strip():
            temp[k] = target_value
            # print(f"if 中 {k}")
            break
        elif isinstance(temp[k], dict):
            search_dict_key(temp[k],target_key.strip(),target_value)
        elif isinstance(temp[k],list):
            for l in temp[k]:
                search_dict_key(l, target_key.strip(), target_value)
    return temp

# 20191227 增加可以直接传入字典
def search_dict(temp, **kwargs):
    for key in kwargs.keys():
        temp = search_dict_key(temp, key, kwargs[key])
    return temp

# 20191230 增加可以直接删除某个值
def del_dict_key(temp,target_key):
    # target_key两边空格可能会影响字典相应值的查询
    for k in temp:
        if k == target_key.strip():
            del temp[k]
            # print(f"if 中 {k}")
            break
        elif isinstance(temp[k], dict):
            del_dict_key(temp[k],target_key.strip())
        elif isinstance(temp[k],list):
            for l in temp[k]:
                del_dict_key(l, target_key.strip())
    return temp


if __name__ == "__main__":
    # new_temp = search_dict_key(TEMPLATE, "ZFLSH", '-----aaaaa-----')
    # print(new_temp)
    new_temp = del_dict_key(TEMPLATE, "FP_KJ")
    print(new_temp)