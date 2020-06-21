<template>
  <div box>
    <el-card class="box-card">
      <div slot="header" style="text-align:center" class="clearfix">
        <span style="font-size:20px">生成试卷</span>
      </div>
      <div>
        <el-form ref="form" :model="form" label-width="100px">
          <el-row>
            <el-col :span="10" :offset="2">
              <el-form-item label="发布人" class="teacherName">
                <el-input v-model="form.teacherName"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="18" :offset="2">
              <el-form-item label="知识点">
                <el-checkbox-group v-model="form.checkList">
                  <el-checkbox label="毛泽东思想"></el-checkbox>
                  <el-checkbox label="新民主主义革命理论"></el-checkbox>
                  <el-checkbox label="社会主义改造理论"></el-checkbox>
                  <el-checkbox label="邓小平理论"></el-checkbox>
                  <el-checkbox label="社会主义建设道路初步探索理论成果"></el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
            <el-col :span="8" :offset="2">
              <el-form-item label="单选题数目">
                <el-input-number v-model="form.single" controls-position="right" :min="0"></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="8" :offset="2">
              <el-form-item label="多选题数目">
                <el-input-number v-model="form.multiple" controls-position="right" :min="0"></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="8" :offset="2">
              <el-form-item label="判断题数目">
                <el-input-number v-model="form.judge" controls-position="right" :min="0"></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="8" :offset="2">
              <el-form-item label="填空题数目">
                <el-input-number v-model="form.completion" controls-position="right" :min="0"></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="16" :offset="2">
              <el-form-item label="难度">
                <el-select v-model="difficulty" placeholder="请选择">
                  <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="20" :offset="2">
              <el-form-item label="测试学生">
                <el-transfer
                  filterable
                  :filter-method="filterMethod"
                  filter-placeholder="请输入学生名称"
                  v-model="testStudents"
                  :data="allStudents"
                  :titles="['所有学生', '测试学生']"
                ></el-transfer>
              </el-form-item>
            </el-col>
            <el-col :span="16" :offset="2">
              <el-form-item label="开放时间">
                <el-date-picker
                  v-model="datetime"
                  type="datetimerange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                ></el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="16" :offset="2">
              <el-form-item>
                <el-button type="primary" @click="onSubmit">立即创建</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </el-card>
    <br />
    <br />
    <br />
    <el-card class="box-card">
      <div slot="header" style="text-align:center" class="clearfix">
        <span style="font-size:20px">试卷(100分)</span>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    const generateStudents = _ => {
      const allStudents = [];
      const students = this.global.user.students;

      students.forEach((student, index) => {
        allStudents.push({
          key: index,
          label: student.extra.name,
          name: student.extra.name,
          id: student.id
        });
      });
      return allStudents;
    };
    return {
      allStudents: generateStudents(),
      testStudents: [],
      filterMethod(query, item) {
        return item.name.indexOf(query) > -1;
      },
      options: [
        {
          value: "4",
          label: "简单"
        },
        {
          value: "5",
          label: "一般"
        },
        {
          value: "6",
          label: "难"
        },
        {
          value: "7",
          label: "超难"
        },
        {
          value: "8",
          label: "巨难"
        }
      ],
      difficulty: "",

      form: {
        teacherName: "",
        checkList: [],
        single: "",
        multiple: "",
        judge: "",
        completion: ""
      },
      datetime: ""
    };
  },
  methods: {
    omSubmit() {
      const studentIds = [];
      const testStudents = this.testStudents;
      testStudents.forEach((student, index) => {
        studentIds.push(student.id);
      });

      this.$http
        .post(
          this.global.baseURL +
            "AllQuestions/releaseExamination/",
            {
                releaseTeacherId:this.global.user.userInfo.id,
                knowledgePointList:this.form.checkList,
                questionTypeList:[1,2,3,4],
                questionNumber0:this.form.single,
                questionNumber1:this.form.multiple,
                questionNumber2:this.form.completion,
                questionNumber3:this.form.judge,
                averageDifficulty:this.difficulty,
                studentIdList:studentIds,
                submitStartTime:this.datetime,
                submitEndTime:this.datetime,
            }
        )
        .then(
          response => {
            // success callback
            alert("submit!");
            this.global.user.testpaper = response.body;
            console.log(this.global.user.testpaper);
            console.log(response);
          },
          response => {
            // error callback
            alert("error!");
          }
        );
    },
  }
};
</script>

<style>
.text {
  font-size: 14px;
}
.teacherName {
  width: ;
  margin-left: ;
}
.item {
  margin-bottom: 18px;
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
  width: 60%;
  margin-left: 15%;
}
</style>