<template>
  <div class="infoBox">
    <ul>
      <h2 class="setTitle">个人信息</h2>
      <li v-for="item in list" class="setList">{{item.title + ":" + item.value}}</li>
    </ul>
    <el-button @click="dialogVisible = true" class="setButton">修改信息</el-button>
    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <el-form :model="list"  ref="list" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model.trim="list.name.value"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="list.gender.value">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model.trim="list.age.value"></el-input>
        </el-form-item>
        <el-form-item label="身份">
          <el-select v-model="list.identity.value" placeholder="请选择性别">
            <el-option label="老师" value="老师"></el-option>
            <el-option label="学生" value="学生"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model.trim="list.phone.value"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="list.mail.value"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('list')" class="setButton">提交修改</el-button>
          <el-button @click="dialogVisible = false" class="setButton">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 等待补充
      dialogVisible: false,
      list: {
        name: {
          title: "姓名",
          value: this.global.user.userInfo.extra.name
        },
        gender: {
          title: "性别",
          value: this.global.user.userInfo.extra.gender
        },
        age: {
          title: "年龄",
          value: this.global.user.userInfo.extra.age
        },
        identity: {
          title: "身份",
          value: this.global.user.userInfo.extra.identity
        },
        phone: {
          title: "电话",
          value: this.global.user.userInfo.extra.phonenum
        },
        mail: {
          title: "邮箱",
          value: this.global.user.userInfo.email
        }
      }
    };
  },
  methods: {
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .put(
              this.global.baseURL +
                "users/" +
                this.global.user.userInfo.id +
                "/",
              {
                username: this.global.user.userInfo.username,
                password: this.global.user.userInfo.password,
                email: this.list.mail.value,
                extra: {
                  age: this.list.age.value,
                  name: this.list.name.value,
                  gender: this.list.gender.value,
                  identity: this.list.identity.value,
                  phonenum: this.list.phone.value
                }
              }
            )
            .then(
              response => {
                // success callback
                console.log("提交"); // 等待补充
                alert("submit!"); // 刷新？
                this.global.user.userInfo = response.body;
                this.dialogVisible = false;
              },
              response => {
                // error callback
                alert("error!");
              }
            );
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    }
  }
};
</script>

<style scoped>
.infoBox {
  width: 65%;
  margin-left: 10%;
  border: 2px solid #dcdfe6;
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB,
    Microsoft YaHei, SimSun, sans-serif;
}
.setTitle {
  border-bottom: 1px solid #cccccc;
  margin-top: 20px;
  padding-bottom: 10px;
}
.setList {
  border-bottom: 1px dashed #cccccc;
  margin-top: 20px;
  padding-bottom: 20px;
  padding-left: 0px;
  list-style: none;
}
.setButton {
  margin: 30px;
}
</style>
