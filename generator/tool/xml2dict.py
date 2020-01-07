# -*- coding: utf-8 -*-
# @Date : 2019-12-31
# @Author : water
# @Version  : v1.0
# @Desc  :


import xmltodict,json
#定义xml转json的函数
def xmltojson(xmlstr):
    #parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    #json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    #dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse,indent=1)
    print(type(jsonstr))
    return jsonstr



#json转xml函数
def jsontoxml(jsonstr):
    #xmltodict库的unparse()json转xml
    xmlstr = xmltodict.unparse(jsonstr,full_document=True)
    print(xmlstr)


def main():
    xml_temp ="""
    <student>
        <stid>10213</stid>
        <info>
            <name>name</name>
            <sex>male</sex>
        </info>
        <course>
            <name>math</name>
            <score>90</score>
        </course>
    </student>
    """
    datas = xmltojson(xml_temp)  #调用转换函数
    print(datas)
    print(xml_temp)
    jsontoxml(json.loads(datas))


if __name__ == "__main__":
    main()
