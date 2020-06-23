<template>
  <div class="box">
    <el-table :data="oneStudentpapers" style="width: 100%; size:medium" ref="filterTable">
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
                  <div v-if="question.submittedAnswer != null">
                    <el-col :span="4">
                      <div style="margin-left:30px">输入答案:{{question.submittedAnswer}}</div>
                    </el-col>
                    <el-col :span="4" :offset="3">
                      <div style="margin-left:30px">正确答案:{{question.trueAnswer}}</div>
                    </el-col>
                  </div>
                  <div v-else-if="question.submittedAnswer == null">
                    <el-col :span="4">
                      <div style="margin-left:30px">
                        答案:
                        <el-input
                          placeholder="请输入答案"
                          size="mini"
                          v-model="question.submittedAnswer"
                        ></el-input>
                      </div>
                    </el-col>
                  </div>
                </el-row>
              </div>
            </div>
            <div>
              <el-row>
                <el-col :span="4">
                  <div style="margin-left:30px">
                    <el-input placeholder="请输入试卷ID号" size="mini" v-model="submitPaperId"></el-input>
                  </div>
                </el-col>
                <el-col :span="4" :offset="3">
                  <el-button type="primary" @click="submitForm">提交</el-button>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </template>
      </el-table-column>
      <el-table-column label="试卷ID" prop="paperId" width="100"></el-table-column>
      <el-table-column label="出题老师" prop="teacherName" width="100"></el-table-column>
      <el-table-column label="教职工号" prop="username" width="120"></el-table-column>
      <el-table-column label="试卷分数" prop="maxScore" width="100"></el-table-column>
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
      const allPapers = this.global.user.oneStudentPapers;
      console.log(this.global.user.oneStudentPapers);
      var submitOrNot = "未提交";
      var SCORE = "无";

      allPapers.forEach(paper => {
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
        };
        
        submitOrNot = "未提交";
        SCORE = "无";

        if (paper.score != null) {
          SCORE = paper.score;
        }
        if (paper.submitTime != null) {
          submitOrNot = paper.submitTime;
        }
        this.$http
          .get(this.global.baseURL + "Student/PaperDetail/" + paper.paperId)
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
              console.log(testpaper.questions);
              console.log(response);
            },
            response => {
              // error callback
              alert("error!");
            }
          );

        studentPapers.push({
          paperId: paper.paperId,
          teacherName: "徐文政",
          username: "12345678",
          maxScore: paper.maxScore,
         // questionNum: paper.questionTotalNumber,
          startTime: paper.submitStartTime,
          endTime: paper.submitEndTime,
          isSubmit: submitOrNot,
          score: SCORE,
          testpaper: testpaper
        });
      });
      return studentPapers;
    };
    return {
      oneStudentpapers: generateStudentPapers(),
      submitPaperId: ""
    };
  },
  methods: {
    submitForm() {
      const submitAnswerList = [];
      const allPapers = this.oneStudentpapers;
      console.log(this.submitPaperId);
      console.log(allPapers);

      allPapers.forEach(paper => {
        if (paper.paperId == this.submitPaperId) {
          console.log(paper.testpaper.questions);
          paper.testpaper.questions.single.value.forEach(question => {
            submitAnswerList.push(question.submittedAnswer);
          });
          paper.testpaper.questions.multiple.value.forEach(question => {
            submitAnswerList.push(question.submittedAnswer);
          });
          paper.testpaper.questions.completion.value.forEach(question => {
            submitAnswerList.push(question.submittedAnswer);
          });
          paper.testpaper.questions.judge.value.forEach(question => {
            submitAnswerList.push(question.submittedAnswer);
          });
        }
      });

      this.$http
        .post(
          this.global.baseURL +
            "Student/submitPaperAnswer/" +
            this.submitPaperId,
            {
                submitAnswerList:submitAnswerList,
            }
        )
        .then(
          response => {
            // success callback
            this.global.user.submitOutcome = response.body;
            console.log("学生试卷");
            console.log(this.global.user.submitOutcome);
          },
          response => {
            // error callback
            alert("error!");
          }
        );
    },
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

