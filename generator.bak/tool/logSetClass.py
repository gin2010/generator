# -*- coding: utf-8 -*-
# @Date : 2019/10/12
# @Author : water
# @Version  : v1.0
# @Desc  : 配置的日志输出功能
           # 1.初始化传入日志输出文件地址（file）、日志级别（0、10、20、30、40、50）
           # 2.三个对外的方法：
           #    2.1 log_to_control：输入日志到控制台
           #    2.2 log_to_file：输入日志到文件
           #    2.3 control_and_file：输入日志到文件及控制台


import logging
from logging import handlers


class Log:

    def __init__(self,file,level):
        # 设置log文件地址
        self.log_file = file
        self.logger = logging.getLogger(self.log_file)
        # 设置日志格式
        fmt = '%(asctime)s -%(pathname)s[line:%(lineno)d] -%(levelname)s:%(message)s'
        self.format_str = logging.Formatter(fmt)  # 设置日志格式
        # 设置日志级别
        self.logger.setLevel(int(level))


    def _log_to_control(self):
        """
        设置日志输出到控制台
        :return:
        """
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(self.format_str)  # 设置屏幕上显示的格式
        self.logger.addHandler(sh)  # 把对象加到logger里


    def log_to_control(self):
        self._log_to_control()
        return self.logger


    def _log_to_file(self):
        """
        设置日志输出到文件中（默认的是追加模式）
        :return:
        """
        th = handlers.TimedRotatingFileHandler(filename=self.log_file, when='D', backupCount=0, encoding='utf-8')
        th.setFormatter(self.format_str)  # 设置文件里写入的格式
        self.logger.addHandler(th)


    def log_to_file(self):
        self._log_to_file()
        return self.logger


    def control_and_file(self):
        """
        日志输出到控制台和文件中
        :return:
        """
        # 日志输出到控制台
        self._log_to_control()
        # 日志输出到文件
        self._log_to_file()
        return self.logger


if __name__ == "__main__":
    lg = Log("logset.log",20)
    logg = lg.log_to_file()
    logg.debug("my debug")
    logg.info("my info")
    logg.warning("my warning")



