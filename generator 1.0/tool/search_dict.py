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
            "KPLX": "2",
            "KPHJJE": "1199.00",
            "HJBHSJE": "1024.79",
            "KPHJSE": "174.21",
            "KPXM": "宇宙飞船",
            "GMF_NSRSBH": "110101009791112",
            "GMF_NSRMC": "柯南公司",
            "GMF_YH": "12310",
            "GMF_YHZH": "123",
            "GMF_DZ": "北京宇宙区",
            "GMF_DH": "15588888884",
            "GMF_SF": "1239",
            "GMF_EMAIL": "81924573@qq.com",
            "GMF_SJ": "15588888884",
            "YFPHM": "1237",
            "YFPDM": "1238",
            "JQBH": "661505060904",
            "KPY": "开票员",
            "SKY": "收款员",
            "FHR": "复核人",
            "SWJG_DM": "111019201",
            "SPHSL": "1",
            "FP_ZLDM": "2",
            "VERSION": "1",
            "XSF_DZ": "北京市宇宙区外星人1号",
            "XSF_DH": "123123123",
            "XSF_YH": "1236",
            "XSF_YHZH": "招商银行",
            "FJH": "9",
            "DSPTBM": "11110101",
            "DKBZ": "0",
            "PDFPATH": "/home/gin/",
            "TSCHBZ": "1",
            "CHYY": "冲红原因",
            "XHQD": "销货清单",
            "XHQDBZ": "0",
            "BMB_BBH": "1233",
            "QD_BZ": "0",
            "DDH": "11111111117",
            "DSF_PTBM": "11111111",
            "SGBZ": "1",
            "QDXMMC": "1232",
            "SKM": "12323354657677",
            "EWM": "Qk1+BgAAAAAAAD4AAAAoAAAAZAAAAGQAAAABAAEAAAAAAEAGAAAAAAAAAAAAAAAAAAACAAAAAAAA///////////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAP////////////////AAAAD////////////////wAAAA////////////////8AAAAAADPAAAzPPzwD////AAAAAAAzwAAMzz88A////wAAAAP/P8P8/DM//A////8AAAAD/z/D/PwzP/wP////AAAAAwM8D/DzPMM/D////wAAAAMDPA/w8zzDPw////8AAAADAzw888P8Dz/P////AAAAAwM8PPPD/A8/z////wAAAAMDM8/PDzAwAw////8AAAADAzPPzw8wMAMP////AAAAA/8/DMAPAwPwD////wAAAAP/PwzADwMD8A////8AAAAAADDzAPPD8zAP////AAAAAAAw8wDzw/MwD////wAAAA//8DDP8APD88////8AAAAP//Awz/ADw/PP////AAAAD8MAD/Aw/zAAD////wAAAA/DAA/wMP8wAA////8AAAAAw8PwAAAP8MwD////AAAAAMPD8AAAD/DMA////wAAAAAAAzPMDMMA/A////8AAAAAAAMzzAzDAPwP////AAAADPPwPz8MM8zDD////wAAAAzz8D8/DDPMww////8AAAAM8AwP8/P/MzwD////AAAADPAMD/Pz/zM8A////wAAAAPz8MPDwM8M/D////8AAAAD8/DDw8DPDPw/////AAAAD/AMMA88D8zPD////wAAAA/wDDAPPA/Mzw////8AAAAPz8PwzPPADMPP////AAAAD8/D8MzzwAzDz////wAAAA//M8PADM8zPDP///8AAAAP/zPDwAzPMzwz////AAAADPDMMDw8MwzMD////wAAAAzwzDA8PDMMzA////8AAAAPDA/88PM/wMwP////AAAADwwP/PDzP8DMD////wAAAA8w8wwzw/zMw8////8AAAAPMPMMM8P8zMPP////AAAADPMM8P8/MzM8A////wAAAAzzDPD/PzMzPAP///8AAAAD888PwD8P/PwD////AAAAA/PPD8A/D/z8A////wAAAAwwMADM/88PwA////8AAAAMMDAAzP/PD8AP////AAAAAz/Azw/wAMzAD////wAAAAM/wM8P8ADMwA////8AAAAMwA8DPDD/Mzwz////AAAADMAPAzww/zM8M////wAAAAwD8PDAwA8z8D////8AAAAMA/DwwMAPM/A/////AAAADA8Dz8zMAwD/D////wAAAAwPA8/MzAMA/w////8AAAAPwMPM/w8wzMP/////AAAAD8DDzP8PMMzD/////wAAAAPzAADD8/8wAPP///8AAAAD8wAAw/P/MADz////AAAAD//w8//wz8P//////wAAAA//8PP/8M/D//////8AAAAAADMzMzMzMwAD////AAAAAAAzMzMzMzMAA////wAAAAP/MD88w/A/P/P///8AAAAD/zA/PMPwPz/z////AAAAAwMz//zzAM8wM////wAAAAMDM//88wDPMDP///8AAAADAzAAD/MwzzAz////AAAAAwMwAA/zMM8wM////wAAAAMDPDDA/DM/MDP///8AAAADAzwwwPwzPzAz////AAAAA/888/APwDM/8////wAAAAP/PPPwD8AzP/P///8AAAAAADPDM8P8zwAD////AAAAAAAzwzPD/M8AA////wAAAA",
            "BZ": "1",
            "FP_MW": "6134*3>950+75<8/1208-85*</*14>-65-142/+7390*24855672678136749+92184+/8*553-9-8-+5*</*1/670433467<<3<0*24<4*6",
            "DDSJ": "2019-08-01 14:15:11",
            "JYM": "65560891271390877510",
			"ISCOVER":"1"
        },
        "FP_KJ_MX": [
            {
                "SPHXH": "01",
                "SPMC": "华为手机",
                "SPSL": "1.00000000",
                "SPJE": "1024.79",
                "SPDJ": "1024.78632479",
                "DW": "1231",
                "GGXH": "12",
                "HSJBZ": "0",
                "KCE": "2",
                "SE": "174.21",
                "SL": "17%",
                "SPBM": "123",
                "ZXBM": "1234",
                "YHZCBS": "1",
                "LSLBS": "0",
                "ZZSTSGL": "1235",
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
    for k in temp:
        if k == target_key:
            temp[k] = target_value
            # print(f"if 中 {k}")
            break
        elif isinstance(temp[k], dict):
            search_dict_key(temp[k],target_key,target_value)
        elif isinstance(temp[k],list):
            for l in temp[k]:
                search_dict_key(l, target_key, target_value)
    return temp


if __name__ == "__main__":
    new_temp = search_dict_key(TEMPLATE,"ZFFS",'-----aaaaa-----')
    print(new_temp)