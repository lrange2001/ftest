<template>
  <el-row :gutter="12">
    <div v-for="row in appdata" style="padding: 20px">
      <el-card shadow="hover" @click="AppdesBtn(row.id)" :key="row.id" style="text-align: center">
          <el-text tag="b" type="info" size="large">{{ row.app_name }}</el-text>
      </el-card>
    </div>
  </el-row>
  <AppCreate v-model:visible="AppCreateBorder" ></AppCreate>
    <AppEdit v-model:visible="AppEditBorder" :AppEditData="AppEditData"></AppEdit>
  <div align="right">
      <el-button @click="AppCreateBorder = true"  size="large" class="createbtn">创建APP</el-button>
  </div>
</template>

<script>
  import AppCreate from "./AppCreate";
  import AppEdit from "./AppEdit";
    export default {
        name: "AppDescribe",
      data(){
          return{
            AppCreateBorder: false,
              AppEditBorder: false,
              AppEditData: '',
            appdata: '',
          }
      },
      mounted() {
          this.$axios.get('/appdeploy/api/app/').then(res =>{
            this.appdata = res.data.data;
          })
      },
      methods: {
          AppdesBtn(index){
            //获取到id 传入子组件 子组件进行配置 删除、编辑、部署等操作
              this.AppEditBorder = true,
              this.AppEditData = index;
          }

      },
      components: {
          AppCreate,
          AppEdit
      }
    }
</script>

<style scoped>
</style>