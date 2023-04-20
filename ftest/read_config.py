import configparser


'''
获取ftest.conf当中的配置

'''
config = configparser.ConfigParser()

config.read("ftest.conf",encoding='utf-8')

result = {}
def main(section):
    for section in config.sections():
        options = config.options(section)
        for key in options:
            result[key] = config.get(section,key)
    return result

