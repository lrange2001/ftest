<template>
      <el-dialog
      :model-value="visible"
      title="添加自定义应用"
      width="40%"
      @close="dialogClose"
      :close-on-click-modal="false"
  >
      <el-steps :active="active" finish-status="success" simple style="margin-bottom: 10%">
        <el-step title="创建APP" />
        <el-step title="上传部署材料" />
        <el-step title="运行以及关闭指令" />
      </el-steps>
        <el-form :model="form" label-width="120px" ref="formRef" :rules="formRules">
          <div v-show="active == 1">
          <el-form-item label="APP名称" prop="AppName">
              <el-input v-model="form.AppName"  style="height: 35px; width: 80%" />
          </el-form-item>
          </div>
          <div v-show="active == 2">
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
                  <el-button type="primary">上传安装脚本以及安装软件<el-icon class="el-icon--right"><Upload /></el-icon></el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    支持任何文件,大小无上限，最多支持100个文件数量，需要考虑服务器宽带,如果是内网请忽略
                  </div>
                </template>
              </el-upload>
          </div>
          <div v-show="active == 3" >
              <el-form-item label="APP安装指令" prop="AppDEPLOY">
                  <el-input v-model="form.AppDEPLOY" style="height: 35px; width: 80%" />
              </el-form-item>

              <el-form-item label="APP运行指令" prop="AppRUN">
                  <el-input v-model="form.AppRUN"  style="width: 80%" />
              </el-form-item>

              <el-form-item label="APP停止指令" prop="AppSTOP">
                  <el-input v-model="form.AppSTOP"  style="width: 80%" />
              </el-form-item>
          </div>
        </el-form>

          <template #footer>
            <span class="dialog-footer" style="">
              <el-button @click="dialogClose" v-if="active == 1">取消</el-button>
              <el-button  @click="dialogToggle('pre')" v-if="active > 1">上一步</el-button>
              <el-button  @click="dialogToggle('next')" v-if="active < 3">下一步</el-button>
              <el-button  @click="submit" v-if="active == 3">确定</el-button>
            </span>
          </template>

      </el-dialog>
</template>

<script>
    export default {
        name: "AppCreate",
        data(){
            return {
                submiting: false,
                active: 1,
                uploadUrl: '',
                form: {
                    AppName: '',
                    AppRUN: '',
                    AppSTOP: '',
                    AppDEPLOY: '',
                    fileList: '',
                },
              formRules: {
                  AppName: [
                      {required: true, message: "请填写APP名称", trigger: "blur"},
                      {min: 4, message: 'APP名称长度不小于4个字符', trigger: 'blur'}
                  ],
                  AppDEPLOY:[
                      {required: true, message: "请输入APP安装指令", trigger: "blur"},
                  ],
                  AppRUN: [
                      {required: true, message:'请输入APP运行指令',trigger: 'blur'},
                  ],
                  AppSTOP: [
                      {required: true, message:'请输入APP停止指令',trigger:'blur'},
                  ]

              },
            }
        },
        props: {
            visible: Boolean
        },
        mounted() {
            this.getUploadUrl();
            this.$axios.get('/appdeploy/app/').then(res =>{
                if(res.data.code == 200){
                    // console.log(res.data.message)
                }else{
                    this.$message.error(res.data.message)
                }
            });

        },
        methods: {
            getUploadUrl(){
              const baseurl = process.env.VUE_APP_BASE_URL;
              this.uploadUrl = String(baseurl + '/appdeploy/app/')
            },
            dialogClose(){
                // this.$emit('update:visible',false);
                this.$emit('update:visible', false);
                this.active=1;
            },
            dialogToggle(action) {
                if (action == 'pre') {
                    if (this.active-- < 2) {
                      this.active = 1;

                    }
                } else if (action == 'next') {
                    if (this.active++ > 3) {
                      this.active = 1;
                    }
                }
            },
            submit(){
                // this.$refs.formRef.validate((valid)
                this.$refs.formRef.validate((valid) =>{
                    if(valid){
                        this.$axios.post('/appdeploy/app/',this.form).then(res =>{
                            if(res.data.code == 200){
                                this.$message.success(res.data.message);
                                this.dialogClose();
                                setTimeout(() =>
                                    location.reload(),1000
                                )

                            }else{
                                this.$message.error(res.data.message)
                            }
                        })
                    }else{
                        this.$message.error('请填写完整的信息！')
                    }
                })
            },
        }
    }
</script>

<style scoped>
   div {
       text-align: center;
   }
</style>