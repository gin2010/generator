# -*- coding: utf-8 -*-
# @Date : 2020-01-14
# @Author : water
# @Version  : v1.0
# @Desc  : 主程序，直接运行此程序将数据导入到datas_fp表中

from tool.generateDatas import GenerateDatas


def main():
    # yhzc = GenerateDatas()
    # yhzc.yhzc_2_database()
    sj = GenerateDatas()
    sj.single_2_database()
    print("-------------end----------------")


if __name__ == "__main__":
    main()

