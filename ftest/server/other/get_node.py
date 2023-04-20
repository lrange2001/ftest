import paramiko
import os

class to_node:
    def __init__(self,username,port,host,auth_type,password=None,key=None):
        self.username = username
        self.port = port
        self.host = host
        self.auth_type = auth_type
        self.password = password
        self.key = key
    def to_command_node(self,command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.auth_type == 1:
            client.connect(
                hostname=self.host,
                username=self.username,
                port=self.port,
                password=self.password
            )
        else:
            private_key = paramiko.RSAKey.from_private_key_file(self.key)
            client.connect(
                hostname=self.host,
                username=self.username,
                port=self.port,
                pkey=private_key
            )
        stdin, stdout, stderr = client.exec_command(command)
        result = {
            "stdout": stdout.read(),
            "stderr": stderr.read()
        }
        return result
    def transport_object_upload(self,local_path,remote_path):
        transport = paramiko.Transport((self.host, self.port))
        if self.auth_type == 1:
            transport.connect(username=self.username, password=self.password)
        else:
            transport.connect(username=self.username,pkey=self.key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_path,remote_path)
        sftp.close()


    def transport_object_download(self,local_path,remote_path):
        transport = paramiko.Transport((self.host, self.port))
        if self.auth_type == 1:
            transport.connect(username=self.username, password=self.password)
        else:
            transport.connect(username=self.username,pkey=self.key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_path,local_path)
        sftp.close()


