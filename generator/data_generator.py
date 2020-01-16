# -*- coding: utf-8 -*-
# @Date : 2020-01-14
# @Author : water
# @Version  : v1.0
# @Desc  : 发票测试数据自动生成

from tool.generateDatas import GenerateDatas


def main():
    # yhzc = GenerateDatas()
    # yhzc.yhzc_2_database()
    sj = GenerateDatas()
    sj.single_2_database()
    print("-------------end----------------")


if __name__ == "__main__":
    main()

