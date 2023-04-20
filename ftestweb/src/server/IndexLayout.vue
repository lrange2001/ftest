<template>
    <div class="tac el-container container">
  <!--      侧边栏-->
      <div  class="left">
        <div style="padding: 10%;color: #e8e8e8; text-align: center">
          DevOps
        </div>
          <el-menu
            :uniqueOpened="true"
            default-active="2"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
            router
            :collapse-transition="false"
          >
<!--                          style="height: 100vh"-->
              <template v-for="menu in this.$router.options.routes" :key="menu" >
                  <el-menu-item v-if="menu.path == '/' " :index="menu.path">
                      <el-icon><component :is="menu.icon"></component></el-icon>
                      <span>{{ menu.name }}</span>
                  </el-menu-item>
                  <el-menu-item v-else-if="menu.path == '/login'" style="display: none"></el-menu-item>

                  <el-menu-item v-else-if="!menu.children " :index="menu.path">
                      <span>{{ menu.name }}</span>
                  </el-menu-item>

                  <el-sub-menu   v-else-if="menu.children" :index="menu.path">
                    <template #title>
                        <el-icon><component :is="menu.icon"></component></el-icon>
                        <span>{{ menu.name }}</span>
                    </template>
                      <el-menu-item v-for="child in menu.children" :key="child" :index="child.path">
                          <el-icon><location /></el-icon>
                          <span>{{ child.name }}</span>
                      </el-menu-item>
                  </el-sub-menu>
              </template>

          </el-menu>
        </div>


<!--      导航栏-->
      <div class="right">
        <el-menu
          default-active="1"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          style="width: 100%; height: 4%"
        >

          <el-sub-menu index="2" style="position: absolute; right: 0">

            <template #title>
              <el-avatar>{{ username }}</el-avatar>
            </template>
            <el-menu-item @click="Logout">退出</el-menu-item>
            <el-menu-item @click="UpdatePassword">修改密码</el-menu-item>
          </el-sub-menu>


<!--          <el-menu-item index="3" disabled>消息中心</el-menu-item>-->
<!--          <el-menu-item index="4">订单管理</el-menu-item>-->
        </el-menu>


  <el-card class="box-card">
    <template #header>
      <div class="card-header">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item v-for="mbx in this.$route.matched">
<!--                <a :href="mbx.path">{{ mbx.name}}</a>-->
                <p>{{mbx.name}}</p>
            </el-breadcrumb-item>
          </el-breadcrumb>
      </div>
    </template>
            <router-view></router-view>
  </el-card>

        <span style="position: absolute; right: 0;bottom: 0"><el-tag type="info">{{ nowDateTime }}</el-tag></span>
      </div>
</div>
</template>

<script>
  import Serverdetails from "../components/Serverdetails";
  import AppDescribe from "../app/AppDescribe";



    export default {
        name: "IndexLayout",
        mounted() {
          this.getUsername();
        },
        components: {
            Serverdetails,
            AppDescribe
        },
        created() {
            this.currentTime();
        },
        data() {
            return {
                backgroud_color: 'red',
                nowDateTime: '', //当前日期
                username: '',
            }
        },
        methods: {
            Logout() {
                window.sessionStorage.clear();
                window.location.href = '/login'
            },
            getTime() {
                let yy = new Date().getFullYear();
                let mm = new Date().getMonth() + 1;
                let dd = new Date().getDate();
                let hh = new Date().getHours();
                let mf = new Date().getMinutes() < 10 ? '0' + new Date().getMinutes() : new Date().getMinutes();
                let ss = new Date().getSeconds() < 10 ? '0' + new Date().getSeconds() : new Date().getSeconds();
                this.nowDateTime = yy + '年 ' + mm + '月' + dd + '日 ' + hh + ':' + mf + ':' + ss;
            },
            currentTime() {
                setInterval(this.getTime, 500)
            },
            getUsername() {
                this.username = window.sessionStorage.getItem('username')
            }
            }
    }

</script>

<style scoped>
.el_layout {
  background-color: #545c64;
}
.el-container,el_layout {
        height: 100%;
    }
.container{
    display: flex;
    height: 100%;

}
.left {
    width: 200px;
    height: 100%;
    background-color: #545c64;
}
.right{
    width: 100%;
    height: 100%;
}
</style>