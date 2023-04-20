<template>
    <div style="float: right">
      <el-button @click="HeadrButton01" :loading="HeadrButton01Button">一键同步</el-button>
      <el-button @click="HeadrButton02 = true">创建服务器</el-button>

  </div>
  <div class="mt-4" style="width: 500px; margin-bottom: 15px; float: left">
    <el-input
      v-model="searchData"
      placeholder="请输入要搜索的主机名"
      class="input-with-select"
    >
      <template #prepend>
        <el-button icon="Search" @click="searchHostname"/>
<!--        <el-icon><Search/></el-icon>-->
      </template>
    </el-input>
  </div>
    <div>
      <el-table :data="tableData" border style="width: 100%" prop>
<!--        <el-table-column label="ID" prop="id" />-->
        <el-table-column label="主机名" prop="hostname">
            <template #default="scope">
                <tr>
                    <td><el-tag class="ml-2" type="success">{{scope.row.hostname}}</el-tag></td>
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

        <el-table-column label="操作系统版本" prop="os_version" /> >

        <el-table-column label="磁盘" prop="disk" />
        <el-table-column label="内存" prop="memory" >
            <template #default="scope">
            <tr>
                <td><el-tag class="m1-2" type="info">{{scope.row.memory}}</el-tag></td>
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
        <el-table-column label="类型" prop="machine_type">
          <template #default="scope">
            <tr>
              <td><el-tag>{{ scope.row.machine_type}}</el-tag></td>
            </tr>
          </template>
        </el-table-column>
        <el-table-column label="CPU数量" prop="cpu_num" >
            <template #default="scope">
            <tr>
                <td><el-tag class="m1-2" type="info">{{scope.row.cpu_num}}</el-tag></td>
            </tr>
            </template>
        </el-table-column>
        <el-table-column label="CPU参数" prop="cpu_model" />
        <el-table-column label="运行日期" prop="put_shelves_date"  />
        <el-table-column label="操作" width="400px" >

          <template #default="scope">
            <el-button size="small" :key="scope.$index"  @click="handleGetData(scope.$index, scope.row)">同步数据</el-button>
            <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除</el-button>

            <el-button size="small"  type="primary" @click="handleWebssh(scope.$index, scope.row)">WebSSH</el-button>

          </template>
        </el-table-column>

      </el-table>

      <SSHChannel v-model:visible="sshDialogVisible" :row="ssh_channel_hostname" style="border-radius: 16px;"></SSHChannel>
      <ServerCreate v-model:visible="HeadrButton02"></ServerCreate>
        <ServerEdit v-model:visible="EditVisible" :editdata="EditData"></ServerEdit>
    </div>


</template>


<script>
  import SSHChannel from "./SSHChannel";
  import IndexLayout from "../server/IndexLayout";
  import ServerCreate from "./ServerCreate";
  import ServerEdit from "./ServerEdit";
// 一定要在Vue.use之前执行此函数
// fixElTableErr(Table)
    export default {
      name: "Serverdetails",
      data() {
        return {
          currentPage: 1, //默认开始页面
          pageSize: 10, //默认每一页的条数
          total: 100, //总条数
          tableData: '',
          ssh_channel_hostname: '',
          sshDialogVisible: false,
          searchData:'',
          HeadrButton01Button: false,
          HeadrButton02: false,
          EditData: '',
          EditVisible: false,
        }
      },
      components: {
        ServerCreate,
        SSHChannel,
        IndexLayout,
        ServerEdit
      },
      mounted() {
          //页面加载 获取数据
        this.$axios.get('/server/api/serverdetais/').then(res =>{
          if(res.data.code == 200){
            this.tableData = res.data.data;
          }else{
            //请求不到后的代码 后端需要改 无message
          }
        })
      },

     // beforeUpdate(){
     //  this.$nextTick(() => { //在数据加载完，重新渲染表格
     //    this.$refs['table'].doLayout();
     //  })
     //  },
      methods: {
          //删除接口
        handleDelete(index,row) {
            console.log(row.hostname);
          this.$axios.delete('/server/api/serverdetais/'+row.id + '/').then(res =>{
              this.$axios.post('/server/NodeHostname/',{"hostname": row.hostname}).then(res =>{
                  this.$message.success('删除成功');
                    setTimeout(() =>
                        location.reload(),1000
                    )
              })
          })
        },
        //编辑接口
        handleEdit(index,row){
          this.EditVisible = true;
          this.EditData = row;
        },
          //webssh接口
        handleWebssh(index,row){
          this.ssh_channel_hostname = row.hostname;
          this.sshDialogVisible = true
        },
          //同步数据接口
        handleGetData(index,row){
          this.$axios.post('/server/gather_node/',{'hostname':row.hostname}).then(res => {
              if(res.data.code == 200){
                this.$message.success('同步数据完成');
                //刷新
                setTimeout(() =>
                    location.reload(),1000
                )

              }else{
                  this.$message.error(res.data.message)
              }
          })
        },
          //搜索接口 必须主机名
        searchHostname(){
          this.$axios.get('/server/api/serverdetais/?search='+this.searchData).then(res =>{
            if(res.data.code == 200){
              this.tableData = res.data.data;
            }else{
              this.$message.warning(res.data.message);
              this.tableData = res.data.data;
            }
          })
        },
          //一键同步
        HeadrButton01(){
          this.HeadrButton01Button = true;
          this.$axios.get('/server/synchronization/').then(res =>{
            if(res.data.code == 200){
              this.HeadrButton01Button = false;
              this.$message.success(res.data.message);
              setTimeout(() =>
                    location.reload(),1000
                )
            }else{
              this.HeadrButton01Button = false;
              this.$message.error('部分机器同步失败,详情查看控制台');
              console.log(res.data.message);
              setTimeout(() =>
                    location.reload(),1000
                )
            }
          })
        },
      }
}

</script>

<style scoped>

</style>