<template>
  <div class="container">
    <div class="nav">
      <el-row>
        <el-col :span="3" :offset="5">
          <h1 class="appname">New Star</h1>
        </el-col>
        <el-col :span="6" :offset="7">
          <div style="height:80px">
            <ul class="top-nav">
              <li>
                <a class="scrollto" href="#">
                  <h2>主页</h2>
                </a>
              </li>
              <li>
                <a class="scrollto" href="#">
                  <h2>产品服务</h2>
                </a>
              </li>
              <li>
                <a class="scrollto" href="#">
                  <h2>关于</h2>
                </a>
              </li>
              <li>
                <a class="scrollto" href="#">
                  <h2>联系方式</h2>
                </a>
              </li>
            </ul>
            <!--//nav-->
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="loginbox">
      <h1 class="logintitle">LOGIN</h1>
      <el-form :model="loginForm" ref="loginForm" class="loginForm">
        <el-form-item
          prop="userId"
          :rules="[
      { required: true, message: '请输入用户名', trigger: 'blur' },
    ]"
          class="useId"
        >
          <el-input
            v-model="loginForm.userId"
            prefix-icon="iconfont icon-zhanghao"
            placeholder="userId"
            class="input"
          ></el-input>
        </el-form-item>
        <el-form-item
          prop="password"
          :rules="[
      { required: true, message: '请输密码', trigger: 'blur' },
    ]"
          class="password"
        >
          <el-input
            v-model="loginForm.password"
            prefix-icon="iconfont icon-mima"
            placeholder="Password"
            show-password
            class="input"
          ></el-input>
        </el-form-item>

        <el-form-item class="btns">
          <el-button type="primary" @click="submitForm('loginForm')">提交</el-button>
          <el-button @click="resetForm('loginForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        userId: "",
        password: ""
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // GET /someUrl
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
          ),
          
          this.$http
            .post(
              this.global.baseURL +
                "users/login/" +
                this.loginForm.userId +
                "/" +
                this.loginForm.password +
                "/"
            )
            .then(
              response => {
                // success callback
                alert("submit!");
                this.global.user.userInfo = response.body;
                console.log(this.global.user.userInfo);
                console.log(response);

                this.$http
                    .get(
                      this.global.baseURL +
                        "Teacher/" + this.global.user.userInfo.id +"/AllPaper"
                    )
                    .then(
                      response => {
                        // success callback
                        this.global.user.studentPapers = response.body;
                        console.log('学生试卷');
                        console.log(this.global.user.studentPapers);
                      },
                      response => {
                        // error callback
                        alert("error!");
                      }
                    );
                if (this.loginForm.userId[0] == '1'){
                  this.$router.push({ path: "/teacher", replace: true });
                }else if (this.loginForm.userId[0] == '0'){
                   this.$http
                    .get(
                      this.global.baseURL +
                        "Student/" + this.global.user.userInfo.id +"/AllPaper"
                    )
                    .then(
                      response => {
                        // success callback
                        this.global.user.oneStudentPapers = response.body;
                        console.log('学生试卷');
                        console.log(this.global.user.oneStudentPapers);
                      },
                      response => {
                        // error callback
                        alert("error!");
                      }
                    );
                  this.$router.push({ path: "/student", replace: true });
                }else{
                  console.log("用户ID错误。")
                }
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
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
};
</script>

<style scoped>
.container {
  background-image: url(..\assets\pics\login-bg.jpg);
  background-repeat: no-repeat;
  background-size: 100% 100%;
  height: 100%;
}
.appname {
  height: 80px;
  color: white;
}

ul,
li {
  margin: 0;
  padding: 0;
}
li {
  list-style: none;
}
.top-nav li {
  float: left;
  margin-left: 15px;
  margin-right: 15px;
}
h2 {
  font-weight: normal;
}
.loginbox {
  width: 450px;
  height: 300px;
  background-color: #ffffff50;
  text-align: center;
  border-radius: 3px;
  position: absolute;
  left: 60%;
  top: 50%;
  transform: translate(0, -50%);
}
.loginForm {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 0 20px;
  box-sizing: border-box;
}
.btns {
  display: flex;
  justify-content: flex-end;
}
.logintitle {
  color: #fffffff0;
  top: 10%;
  position: absolute;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>