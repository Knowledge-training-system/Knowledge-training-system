<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>密码管理</span>
      <el-button style="float: right" size="medium" type="primary" @click="changePw()">修改</el-button>
    </div>
    <div>
      <div class="text item">旧密码</div>
      <el-input placeholder="请输入原密码" v-model="oldPw" show-password class="el- item"></el-input>
      <div class="text item">
        新密码
        <span class="text item" style="color:red">(*密码由8-16位字母和数字(两者都要包括）组成!)</span>
      </div>
      <el-input placeholder="请输入新密码" v-model="newPw" show-password class="el- item"></el-input>
      <div class="text item">确认密码</div>
      <el-input placeholder="请再次输入新密码" v-model="repeat" show-password class="el- item"></el-input>
    </div>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      oldPw: "",
      newPw: "",
      repeat: ""
    };
  },
  methods: {
    changePw() {
      var checkEnter = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$/;
      if (this.oldPw !== this.global.user.userInfo.password) {
        alert("原密码错误！");
      } else if (!checkEnter.test(this.newPw)) {
        alert("新密码不合规范！");
      } else if (this.newPw !== this.repeat) {
        alert("两次新密码输入不一致！");
      } else {
        console.log(this.repeat); // 等待补充
        this.$http
          .put(
            this.global.baseURL + "users/" + this.global.user.userInfo.id + "/",
            {
              username: this.global.user.userInfo.username,
              password: this.repeat,
              email: this.global.user.userInfo.email,
              extra: {
                age: this.global.user.userInfo.extra.age,
                name: this.global.user.userInfo.extra.name,
                gender: this.global.user.userInfo.extra.gender,
                identity: this.global.user.userInfo.extra.identity,
                phonenum: this.global.user.userInfo.extra.phonenum
              }
            }
          )
          .then(
            response => {
              // success callback
              console.log("提交"); // 等待补充
              alert("修改成功！");
              this.global.user.userInfo = response.body;
              this.dialogVisible = false;
            },
            response => {
              // error callback
              alert("error!");
            }
          );
      }
    }
  }
};
</script>

<style scoped>
.text {
  font-size: 14px;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}

.item {
  margin-bottom: 18px;
}

.el- {
  width: 300px;
}

.tips {
  padding-left: 60px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

.box-card {
  width: 720px;
  margin: 50px;
  margin-left: 15%;
}
</style>
