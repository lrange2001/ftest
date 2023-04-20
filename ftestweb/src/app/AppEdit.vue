<template>
     <el-drawer
    :model-value="visible"
    :title=title
    direction="rtl"
    size="50%"
    @close="dialogClose"
    @open="dialogOpen"
  >
<div>
    <el-card class="box-card" style="margin: 5px">
      <template #header>
        <div class="card-header">
          <span>APP详细信息</span>
        </div>
      </template>
      <p><el-tag type="info">应用APP名称</el-tag>: <el-tag>{{appeditdata.app_name}}</el-tag></p>
  <!--    <p>{{appeditdata.app_script}}</p>-->
      <p><el-tag type="info">应用部署指令</el-tag>: <el-tag> {{appeditdata.app_deploy}}</el-tag></p>
      <p><el-tag type="info">应用运行指令</el-tag>: <el-tag>{{appeditdata.app_start}}</el-tag></p>
      <p><el-tag type="info">应用停止指令</el-tag>: <el-tag>{{appeditdata.app_stop}}</el-tag></p>
      <p><el-tag type="info">应用创建时间</el-tag>: <el-tag>{{appeditdata.create_time}}</el-tag></p>
      <p><el-tag type="info">配置更新时间</el-tag>: <el-tag>{{appeditdata.update_time}}</el-tag></p>

      <div align="right">
          <el-button type="danger" plain @click="deleteApp">删除APP</el-button>
      </div>
    </el-card>


    <el-card class="box-card" style="margin: 5px">
      <template #header>
        <div class="card-header">
          <span>部署服务器选择</span>
        </div>
      </template>

      <div>
          <el-select v-model="selectValue" placeholder="请选择部署服的服务器">
            <el-option
              v-for="item in serverData"
              :key="item.id"
              :label="item.hostname"
              :value="item.hostname"
            >
            </el-option>
          </el-select>
      </div>
        <div  align="right">
          <el-button type="primary" plain @click="deployBtn">自动部署</el-button>
        </div>
    </el-card>




    <el-card class="box-card" style="margin: 5px">
      <template #header>
        <div class="card-header">
          <span>部署材料配置</span>
        </div>
      </template>

        <div>
            <el-input v-model="form.id" disabled  style="display: none"></el-input>
            <p>应用APP名称: <el-input v-model="form.app_name" disabled style="width: 50%"/></p>
            <p>应用部署指令: <el-input v-model="form.app_deploy" style="width: 50%"/></p>
            <p>应用运行指令: <el-input v-model="form.app_start" style="width: 50%" /></p>
            <p>应用停止指令: <el-input v-model="form.app_stop"  style="width: 50%"/></p>

          <el-upload
                v-model:file-list="form.fileList"
                class="upload-demo"
                :action="uploadUrl"
                multiple
                :on-preview="handlePreview"
                :on-remove="handleRemove"
                :before-remove="beforeRemove"
                :before-upload="beforeAvatarUpload"
                :limit="100"
                :on-exceed="handleExceed"
              >
<!--                <el-button>上传部署脚本</el-button>-->
                  <el-button type="primary" >上传安装脚本以及安装软件<el-icon class="el-icon--right"><Upload /></el-icon></el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    支持任何文件,大小无上限，最多支持100个文件数量，需要考虑服务器宽带,如果是内网请忽略
                  </div>
                </template>
          </el-upload>
        </div>
        <div  align="right">
            <el-button @click="UpdateData" :loading="isloading" type="primary" plain>同步部署配置</el-button>
        </div>
    </el-card>






    <el-card class="box-card" style="margin: 5px">
      <template #header>
        <div class="card-header">
          <span>已运行的服务器</span>
        </div>
      </template>
      <el-table :data="serverData2" border style="width: 100%" prop>
<!--        <el-table-column label="ID" prop="id" />-->
        <el-table-column label="主机名" prop="hostname">
            <template #default="scope">
                <tr>
                    <td><el-tag class="ml-2" type="success">{{scope.row.app_hostname}}</el-tag></td>
                </tr>
            </template>
        </el-table-column>

        <el-table-column label="公网IP" prop="public_ip">
            <template #default="scope">
            <tr>
                <td><el-tag class="m1-2" type="info">{{scope.row.public_ip}}</el-tag></td>
            </tr>
            </template>
        </el-table-column>

        <el-table-column label="内网IP" prop="private_ip" >
            <template #default="scope">
            <tr>
                <td><el-tag class="m1-2" type="info">{{scope.row.private_ip}}</el-tag></td>
            </tr>
            </template>
        </el-table-column>
        <el-table-column label="操作" width="500px" >

          <template #default="scope">
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">卸载应用
            </el-button>

            <el-button
              size="small"
              type="success"
              @click="handleDelete(scope.$index, scope.row)">重启应用
            </el-button>

            <el-button
              size="small"
              type="success"
              @click="handleDelete(scope.$index, scope.row)">运行应用
            </el-button>

            <el-button
              size="small"
              type="info"
              @click="handleDelete(scope.$index, scope.row)">停止应用
            </el-button>

            <el-button
              size="small"
              @click="handleDelete(scope.$index, scope.row)">查询日志
            </el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-card>


    </div>

  </el-drawer>

</template>

<script>
    export default {
        name: "AppEdit",
        props: {
            visible: Boolean,
            AppEditData: Number
        },
        data() {
            return {
                appeditdata: '',
                title: '应用配置',
                serverData: '',
                serverData2: '',
                isloading: false,
                uploadUrl: '',
                selectValue: '',
                form: {
                    id: '',
                    app_name: '',
                    app_deploy: '',
                    app_start: '',
                    app_stop: '',
                    fileList: ''

                }
            }
        },
        mounted() {
            this.getUploadUrl();
            this.getServerData();

        },
        methods: {
            getUploadUrl(){
              const baseurl = process.env.VUE_APP_BASE_URL;
              this.uploadUrl = String(baseurl + '/appdeploy/app/')
            },
            dialogClose() {
                this.$emit('update:visible', false);
                this.selectValue = '';
            },
            getAppEditData() {
                this.$axios.get('/appdeploy/api/app/' + this.AppEditData + '/').then(res => {
                    this.appeditdata = res.data;
                    this.form.id = res.data.id;
                    this.form.app_name = res.data.app_name;
                    this.form.app_deploy = res.data.app_deploy;
                    this.form.app_start = res.data.app_start;
                    this.form.app_stop = res.data.app_stop;
                })
            },
            dialogOpen() {
                this.getAppEditData();
                this.getServerData2();
            },
            getServerData() {
                this.$axios.get('/server/api/serverdetais/').then(res => {
                    if (res.data.code == 200) {
                        this.serverData = res.data.data;
                    } else {
                        //请求不到后的代码 后端需要改 无message
                    }
                })
            },
            getServerData2(){
              this.$axios.get('/appdeploy/apprun/' + this.AppEditData +'/' ).then(res => {
                  this.serverData2 = res.data.data;
              })
            },
            UpdateData() {
                this.isloading = true;
                this.$axios.put('/appdeploy/app/' + this.form.id + '/', {
                    "app_name": this.form.app_name,
                    "app_start": this.form.app_start,
                    "app_deploy": this.form.app_deploy,
                    "app_stop": this.form.app_stop,
                    "fileList": this.form.fileList
                }).then(res => {
                    if (res.data.code == 200) {
                        this.$message.success('同步数据已完成');
                        setTimeout(() =>
                            location.reload(), 1000
                        );
                    } else {
                        this.$message.error(res.data.message);
                        this.isloading = false;
                    }
                })

            },
            deleteApp(){
                this.$axios.delete('/appdeploy/app/'+this.form.id+'/').then(res =>{
                    if(res.data.code == 200) {
                        this.$message.success('删除成功')
                    }else{
                        this.$message.error(res.data.message);
                    }
                })
            },
            deployBtn(){
                const deploydata = {"app_id":this.AppEditData,"hostname":this.selectValue};
                this.$axios.post('/appdeploy/apprun/',deploydata).then(res =>{
                    this.$message.success(res.data.message);
                    setTimeout(() =>
                        location.reload(), 1000
                    );
                })
            },
            handleDelete(){
                this.$message.warning('暂未开发')
            }
        }
    }
</script>

<style scoped>
</style>