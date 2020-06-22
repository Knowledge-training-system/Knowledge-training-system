<template>
  <div class="container">
    <el-container class="container-layout">
      <el-header class="header">
        <el-row>
          <el-col :span="6">
            <div class="appname">New Star</div>
          </el-col>
          <el-col :span="6">
            <span class="item">{{page}}</span>
          </el-col>
          <el-col :span="6" :offset="6">
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link menu">
                {{username}}
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="账号管理">账号管理</el-dropdown-item>
                <el-dropdown-item command="退出空间">退出空间</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="200px" class="aside">
          <div class="headPicBox">
            <div class="headPic">
              <el-avatar :size="100" :src="circleUrl"></el-avatar>
              <p class="user-name">{{username}}</p>
            </div>
          </div>
          <el-divider></el-divider>
          <div class="aside-nav">
            <el-menu
              default-active="/teacher/info"
              router
              mode="horizontal"
              class="el-menu-vertical-demo"
              @select="handleSelect"
            >
              <el-menu-item index="/teacher/info" :key="1">
                <i class="el-icon-user-solid"></i>
                <span slot="title">个人信息</span>
              </el-menu-item>
              <el-menu-item index="/teacher/students" :key="2">
                <i class="el-icon-menu"></i>
                <span slot="title">学生管理</span>
              </el-menu-item>
              <el-menu-item index="/teacher/paper" :key="3">
                <i class="el-icon-document"></i>
                <span slot="title">发布试卷</span>
              </el-menu-item>
              <el-menu-item index="/teacher/manage" :key="4">
                <i class="el-icon-setting"></i>
                <span slot="title">管理试卷</span>
              </el-menu-item>
            </el-menu>
          </div>
        </el-aside>
        <el-main class="main">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      circleUrl:
        "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
      username: this.global.user.userInfo.extra.name,
      page: "个人信息"
    };
  },
  methods: {
    handleCommand(command) {
      if (command == "账号管理") {
        this.page = "账号管理";
        this.$router.push({ path: "/teacher/account", replace: true });
        //重定向路由
      } else {
        this.$router.push({ path: "/login", replace: true });
        //重定向路由到登录界面，同时清空所有全局用户数据
      }
    },
    handleSelect(index) {
      if (index == "/teacher/info") {
        this.page = "个人信息";
      } else if (index == "/teacher/students") {
        this.$http
          .get(
            this.global.baseURL +
              "users/teacher/学生/"
          )
          .then(
            response => {
              // success callback
              this.global.user.students = response.body;
              console.log(this.global.user.students);
            },
            response => {
              // error callback
              alert("error!");
            }
          );
        this.page = "学生管理";
      } else if (index == "/teacher/paper") {
        this.page = "发布试卷";
      } else if (index == "/teacher/manage") {
        this.page = "管理试卷";
      }
    }
  }
};
</script>

<style scoped>
.container {
  height: 100%;
}
.container-layout {
  height: 100%;
}
.header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
}
.appname {
  height: 60px;
  font-size: 30px;
  color: #1989fa;
  display: inline-block;
  height: 100%;
  line-height: 56px;
  box-sizing: border-box;
  text-align: center;
}
.item {
  display: inline-block;
  height: 100%;
  line-height: 60px;
  font-size: 20px;
  color: #1989fa;
  border-bottom: 3px solid #1989fa;
  box-sizing: border-box;
  text-align: center;
  font-weight: lighter;
}
.menu {
  display: inline-block;
  height: 100%;
  line-height: 60px;
  font-size: 20px;
  color: #1989fa;
  box-sizing: border-box;
  text-align: center;
  font-weight: lighter;
}
.el-menu-item {
  width: 200px;
}
.aside {
  background-color: #ffffff;
  height: 100%;
  border: 1px solid #dcdfe6;
}
.headPicBox {
  height: 180px;
  text-align: center;
}
.headPic {
  position: absolute;
  left: 40px;
  top: 90px;
}
.aside {
}
.main {
  background-color: #fff;
  height: 100%;
  box-sizing: border-box;
  border: 1px solid #dcdfe6;
}
</style>