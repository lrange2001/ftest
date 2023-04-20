<template>
  <el-dialog
      :model-value="visible"
      title="添加服务器"
      width="30%"
      @close="dialogClose"
      :close-on-click-modal="false"
  >
        <el-form :model="form" label-width="120px" ref="formRef" :rules="formRules">
            <el-form-item label="主机名称" prop="hostname">
                 <el-input   v-model="form.hostname"  />
            </el-form-item>

            <el-form-item label="SSH地址" prop="ipaddress">
          <el-input v-model="form.ipaddress"   />
            </el-form-item>

            <el-form-item label="端口" prop="port">
          <el-input v-model="form.port"   />
            </el-form-item>

            <el-form-item label="用户名" prop="username">
          <el-input  v-model="form.username"  />
            </el-form-item>

            <el-form-item label="认证方式" prop="auth_choice">
            <el-radio-group v-model="form.auth_choice" class="ml-4" style="float: left"  >
              <el-radio label="1" size="large">密码认证</el-radio>
              <el-radio label="2" size="large">密钥认证</el-radio>
            </el-radio-group>
            </el-form-item>

             <el-form-item label="请输入密码"  v-if="this.form.auth_choice == 1" prop="auth_password">
                <el-input   v-model="form.auth_password"   show-password   ></el-input>
              </el-form-item>

            <el-form-item label="请添加密钥" v-else-if="this.form.auth_choice == 2"  prop="auth_key">
              <el-input    v-model="form.auth_key"  ></el-input>
            </el-form-item>
        </el-form>


    <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogClose">取消</el-button>
          <el-button type="primary" @click="submit" :loading="submiting">确定</el-button>
        </span>
      </template>
 </el-dialog>

</template>

<script>
    export default {
        name: "ServerCreate",
        data() {
          return {
              submiting: false,
              form: {
                  hostname: '',
                  ipaddress: '',
                  username: '',
                  auth_choice: '',
                  auth_password: '',
                  auth_key: '',
                  port: 22
              },
              formRules: {
                  hostname: [
                      {required: true, message: "主机名称必须真实",trigger: "blur" }
                  ],
                  ipaddress: [
                      {required: true, message: "请填写SSH地址",trigger: "blur"}
                  ],
                  username: [
                      {required: true, message: "请输入用户名", trigger: 'blur'}
                  ],
                  auth_choice: [
                      {required: true, message: '请选择认证方式',trigger: 'blur'}
                  ],
                  auth_password: [
                      {required: true, message:'请输入密码',trigger:'blur'}
                  ],
                  auth_key: [
                      {required: true, message:'请上传密钥文件',trigger:'blur'}
                  ],
                  port: [
                      {required: true, message: '请输入SSH端口', trigger: 'blur'}
                      // {min: 2, message: 'SSH端口长度不小于2个数字', trigger: 'blur'},
                  ],
              },
          }
        },
        props: {
            visible: Boolean
        },
        methods: {
          clearform(){
            this.form.hostname = '',
            this.form.ipaddress = '',
            this.form.username = '',
            this.form.auth_choice = '',
            this.form.auth_password = '',
            this.form.auth_key = ''
          },
          dialogClose() {
            this.$emit('update:visible', false)  // 父组件必须使用v-model
            this.clearform(); //清理所有数据
          },
            submit(){
              this.$refs.formRef.validate((valid) =>{
                  this.submiting = true;
                  if(valid){
                    // this.dialogClose();
                      this.$axios.post('/server/api/server/',this.form).then(res =>{
                          if(res.data.code == 200){
                              this.$axios.post('/server/gather_node/',{'hostname':this.form.hostname}).then(rsync =>{
                                  if(rsync.data.code == 200){
                                      this.$message.success('创建完成,并且同步成功');
                                      this.submiting = false;
                                      this.dialogClose();
                                  }else{
                                      this.$message.warning('创建完成,但同步失败,详情查看控制台')
                                      console.log(rsync.data.message);
                                      this.submiting = false;
                                      this.dialogClose();
                                  }
                              })
                          }else{
                              this.$message.error('创建失败,详情查看控制台');
                              this.submiting = false;
                              console.log(res.data.message);
                          }
                      })

                  }else{
                      this.$message.error('格式错误');
                  }
              })

            }
        }
    }
</script>

<style scoped>
</style>