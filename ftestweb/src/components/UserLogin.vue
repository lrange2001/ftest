<template>
<div id="building">
  <div class="logindv">
      <p style="font-weight: bold; color: #555555; text-align: center">DevOps管理系统</p>
      <hr>
       <el-input class="input_border" v-model="form.username"  placeholder="请输入用户名" />
       <el-input class="input_border" v-model="form.password" type="password" show-password placeholder="请输入密码"/>
      <div class="loginbutton">
        <ButtOn buttonmsg="登录" @click="loginclick"/>
      </div>
  </div>
</div>
</template>


<script>
import ButtOn from "@/components/ButtOn";
console.log(process.env.VUE_APP_BASE_URL);
    export default {
        name: "UserLogin",
        data() {
          return {
            form: {
              username: "",
              password: ""

            }
          }
        },
        components: {
            ButtOn
        },
      methods: {
          loginclick(){
              window.sessionStorage.clear();
              this.$axios.post(
                  '/server/login/',
                  this.form
              ).then(res => {
                  if(res.data.code == 200){
                      //登录成功后将token存储至session当中 用于判断
                      window.sessionStorage.setItem('token',res.data.token);
                      window.sessionStorage.setItem('username',this.form.username);
                      window.location.href='/'
                  }else{
                      this.$message.error(res.data.message)
                  }
              })
          }
      }
    }
</script>

<style scoped>

  .logindv {
    width: 500px;
    height: 230px;
    border: 1px solid gray;
    box-shadow: 0 5px 20px 0 #e8e8e8;
    border-radius: 8px;
    position: absolute;
    left: 35%;
    bottom: 50%;

  }
  .input_border{
      padding-top: 15px;
  }
#building{
  background:url("../img/background.jpg");
  width:100%;
  height:100%;
  position:fixed;
  background-size:100% 100%;
}
</style>