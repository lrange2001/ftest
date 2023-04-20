from server.models import Serverdetails
import json
from log.logserver import outputLog
def get_serverdetails(data):
    try:
        result = json.loads(data)
    except:
        return {"message":"采集格式出现问题","code": 500}
    hostname = result['hostname']
    if Serverdetails.objects.filter(hostname=hostname).exists():
        try:
            Serverdetails.objects.filter(hostname=hostname).update(**result)
            resp = {
                "message": "更新数据完成",
                "code": 200
            }
            outputLog(logger_name='register_serverinfoTodb').info(resp)
            return resp

        except Exception as f:
            outputLog(logger_name='register_serverinfoTodb').error(f)
            resp = {"message": "更新数据失败:%s"%f,"code": 502}
            return  resp
    else:
        try:
            Serverdetails.objects.create(**result).save()
            resp = {
                "message": "同步数据完成",
                "code": 200
            }
            outputLog(logger_name='register_serverinfoTodb').info(resp)
            return resp
        except Exception as f:
            outputLog(logger_name='register_serverinfoTodb').error(f)
            print(f)
            resp = {"message": "创建数据失败:%s"%f,"code": 502}
            return  resp
