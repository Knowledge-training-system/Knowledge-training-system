<template>
  <div class="box">
    <el-table :data="studentpapers" style="width: 100%; size:medium" ref="filterTable">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-card class="box-card">
            <div slot="header" style="text-align:center" class="clearfix">
              <span style="font-size:20px">试卷</span>
            </div>
            <div v-for="item in props.row.testpaper.questions" class="text item">
              <div v-if="item.title == 'single' && item.value.length  > 0">一、单选题</div>
              <div
                v-else-if=" item.title == 'multiple' &&  item.value.length  > 0&& testpaper.questions.single.value.length == 0"
              >一、多选题</div>
              <div v-else-if=" item.title == 'multiple' &&  item.value.length">二、多选题</div>
              <div
                v-else-if=" item.title == 'completion' &&  item.value.length  > 0 && testpaper.questions.single.value.length == 0 && testpaper.questions.multiple.value.length == 0"
              >一、填空题</div>
              <div
                v-else-if=" item.title == 'completion' &&  item.value.length  > 0 && (testpaper.questions.single.value.length == 0 || testpaper.questions.multiple.value.length == 0)"
              >二、填空题</div>
              <div v-else-if=" item.title == 'completion' &&  item.value.length  > 0">三、填空题</div>
              <div
                v-else-if=" item.title == 'judge' &&  item.value.length  > 0 && testpaper.questions.single.value.length == 0 && testpaper.questions.multiple.value.length == 0 && testpaper.questions.completion.value.length == 0"
              >一、判断题</div>
              <div
                v-else-if=" item.title == 'judge' &&  item.value.length  > 0 && testpaper.questions.single.value.length != 0 && testpaper.questions.multiple.value.length == 0 && testpaper.questions.completion.value.length == 0"
              >二、判断题</div>
              <div
                v-else-if=" item.title == 'judge' &&  item.value.length > 0 && testpaper.questions.single.value.length == 0 && testpaper.questions.multiple.value.length != 0 && testpaper.questions.completion.value.length == 0"
              >二、判断题</div>
              <div
                v-else-if=" item.title == 'judge' &&  item.value.length > 0 && testpaper.questions.single.value.length == 0 && testpaper.questions.multiple.value.length == 0 && testpaper.questions.completion.value.length != 0"
              >二、判断题</div>
              <div
                v-else-if=" item.title == 'judge' &&  item.value.length > 0 && testpaper.questions.single.value.length != 0 && testpaper.questions.multiple.value.length != 0 && testpaper.questions.completion.value.length != 0"
              >四、判断题</div>
              <div v-else-if=" item.title == 'judge' &&  item.value.length > 0">三、判断题</div>
              <br />
              <div v-for="(question,index) in item.value" style="margin-right:30px">
                {{index +1}}{{"、" + question.question}}
                <br />
                <div
                  style="margin-left:30px"
                  v-if="item.title == 'single' || item.title == 'multiple'"
                >
                  {{question.options[0]}}
                  <br />
                  {{question.options[1]}}
                  <br />
                  {{question.options[2]}}
                  <br />
                  {{question.options[3]}}
                </div>
                <br />
                <el-row>
                  <el-col :span="4">
                    <div style="margin-left:30px" >输入答案:{{question.submittedAnswer}}</div>
                  </el-col>
                  <el-col :span="4" :offset="3">
                    <div style="margin-left:30px">正确答案:{{question.trueAnswer}}</div>
                  </el-col>
                </el-row>
                <br />
              </div>
            </div>
          </el-card>
        </template>
      </el-table-column>
      <el-table-column label="试卷ID" prop="paperId" width="100"></el-table-column>
      <el-table-column label="测试学生" prop="stuName" width="100"></el-table-column>
      <el-table-column label="学号" prop="username" width="120"></el-table-column>
      <el-table-column label="试卷分数" prop="maxScore" width="100"></el-table-column>
      <el-table-column label="题目数量" prop="question.Num" width="100"></el-table-column>
      <el-table-column
        label="开始时间"
        prop="startTime"
        width="200"
        sortable
        column-key="date"
        :filters="[{text: '2020-06-22', value: '2020-06-22T16:00:00Z'}, {text: '2016-05-02', value: '2016-05-02'}]"
        :filter-method="filterHandler"
      ></el-table-column>
      <el-table-column label="截止时间" prop="endTime" width="200"></el-table-column>
      <el-table-column label="提交时间" prop="isSubmit" width="150" sortable></el-table-column>
      <el-table-column label="得分" prop="score" width="100" sortable></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    const generateStudentPapers = _ => {
      const studentPapers = [];
      const students = this.global.user.students;
      const allStudentPapers = this.global.user.studentPapers;
      var submitOrNot = "未提交";
      var SCORE = "无";

      allStudentPapers.forEach(studentPaper => {
        const testpaper = {
          questions: {
            single: {
              title: "single",
              value: []
            },
            multiple: {
              title: "multiple",
              value: []
            },
            completion: {
              title: "completion",
              value: []
            },
            judge: {
              title: "judge",
              value: []
            }
          }
          //paper: [],
          //scores: 0,
          //count: 1
        };

        submitOrNot = "未提交";
        SCORE = "无";
        
        if (studentPaper.score != null) {
          SCORE = studentPaper.score;
        }
        if (studentPaper.submitTime != null) {
          submitOrNot = studentPaper.submitTime;
        }
        this.$http
          .get(
            this.global.baseURL + "Student/PaperDetail/" + studentPaper.paperId
          )
          .then(
            response => {
              // success callback
              this.global.user.aPaper = response.body;
              testpaper.questions.single.value = [];
              testpaper.questions.multiple.value = [];
              testpaper.questions.completion.value = [];
              testpaper.questions.judge.value = [];
              console.log(this.global.user.aPaper);
              console.log("一张试卷");

              this.global.user.aPaper.questions.forEach(question => {
                console.log(question);
                if (question.question.indexOf("[单选题]") == 0) {
                  testpaper.questions.single.value.push(question);
                } else if (question.question.indexOf("[多选题]") == 0) {
                  testpaper.questions.multiple.value.push(question);
                } else if (question.question.indexOf("[填空题]") == 0) {
                  testpaper.questions.completion.value.push(question);
                } else if (question.question.indexOf("[判断题]") == 0) {
                  testpaper.questions.judge.value.push(question);
                }
              });
              console.log("testpaper.questions");
              console.log(testpaper.questions);
              console.log(response);
            },
            response => {
              // error callback
              alert("error!");
            }
          );
        students.forEach(student => {
          if (studentPaper.studentId == student.id) {
            studentPapers.push({
              paperId: studentPaper.paperId,
              stuName: student.extra.name,
              username: student.username,
              maxScore: studentPaper.maxScore,
              questionNum: studentPaper.questionTotalNumber,
              startTime: studentPaper.submitStartTime,
              endTime: studentPaper.submitEndTime,
              isSubmit: submitOrNot,
              score: SCORE,
              testpaper: testpaper
            });
          }
        });
      });
      return studentPapers;
    };
    return {
      studentpapers: generateStudentPapers()
    };
  },
  methods: {
    resetDateFilter() {
      this.$refs.filterTable.clearFilter("date");
    },
    filterHandler(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    }
  }
};
</script>

<style>
.box {
  border: 1px solid #dcdfe6;
  width: 1220px;
  margin-left: 5%;
  margin-top: 40px;
}
.demo-table-expand {
  font-size: 20px;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
  font-size: 15px;
}

.box-card {
  width: 900px;
  margin-left: 10%;
}
</style>

