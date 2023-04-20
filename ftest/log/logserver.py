import logging

class outputLog:
    def __init__(self, file_name='ftest.log', logger_name=None):
        self.file_name = file_name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.get_log()

    def get_log(self):
        # FileHandler: 将格式化的日志记录写入磁盘文件的处理程序类
        # 将格式化的日志记录写入磁盘文件的处理程序
        handler = logging.FileHandler(self.file_name)
        handler.setLevel(logging.DEBUG)
        formater = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formater)
        self.logger.addHandler(handler)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)