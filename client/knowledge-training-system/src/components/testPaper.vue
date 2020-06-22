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
      <div v-for="item in testpaper.questions" class="text item">
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
        <br/>
        <div
          v-for="(question,index) in item.value"
          style="margin-right:30px"
        >
          {{index +1}}{{"、" + question.question}}
          <br />
          <div style="margin-left:30px" v-if="item.title == 'single' || item.title == 'multiple'">
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
              <div style="margin-left:30px">
                答案:
                <el-input placeholder="请输入答案" size="mini"></el-input>
              </div>
            </el-col>
          </el-row>
          <br/>
        </div>
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
      testpaper: {
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
      },
      allStudents: generateStudents(),
      testStudents: [],
      filterMethod(query, item) {
        return item.name.indexOf(query) > -1;
      },
      options: [
        {
          value: 4,
          label: "简单"
        },
        {
          value: 5,
          label: "一般"
        },
        {
          value: 6,
          label: "难"
        },
        {
          value: 7,
          label: "超难"
        },
        {
          value: 8,
          label: "巨难"
        }
      ],
      difficulty: 0,

      form: {
        teacherName: this.global.user.userInfo.extra.name,
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
    onSubmit() {
      const studentIds = [];
      const testStudents = this.testStudents;
      console.log("你好");
      console.log(this.allStudents);
      console.log(testStudents);
      testStudents.forEach((student, index) => {
        studentIds.push(this.allStudents[index].id);
      });
      console.log(studentIds);

      this.$http
        .post(this.global.baseURL + "AllQuestions/releaseExamination", {
          releaseTeacherId: this.global.user.userInfo.username,
          knowledgePointList: this.form.checkList,
          questionNumber0: this.form.single,
          questionNumber1: this.form.multiple,
          questionNumber2: this.form.completion,
          questionNumber3: this.form.judge,
          averageDifficulty: this.difficulty,
          studentIdList: studentIds,
          submitStartTime: this.datetime[0],
          submitEndTime: this.datetime[1]
        })
        .then(
          response => {
            // success callback
            alert("submit!");
            this.global.user.testpaper = response.body;
            this.testpaper.questions.single.value = [];
            this.testpaper.questions.multiple.value = [];
            this.testpaper.questions.completion.value = [];
            this.testpaper.questions.judge.value = [];
            this.global.user.testpaper.questions.forEach(question => {
              console.log(question);
              //console.log(question.question.indexOf("[单选题]"));
              if (question.question.indexOf("[单选题]") == 0) {
                console.log(question.question.indexOf("[单选题]"));
                this.testpaper.questions.single.value.push(question);
              } else if (question.question.indexOf("[多选题]") == 0) {
                this.testpaper.questions.multiple.value.push(question);
              } else if (question.question.indexOf("[填空题]") == 0) {
                this.testpaper.questions.completion.value.push(question);
              } else if (question.question.indexOf("[判断题]") == 0) {
                this.testpaper.questions.judge.value.push(question);
              }
            });
            /*this.testpaper.paper = this.global.user.testpaper;
            var scores = 0;
            const questions = this.testpaper.paper.questions;
            questions.forEach(question => {
              scores = scores + question.score;
            });
            this.scores = scores;  */
            console.log(this.testpaper.questions);
            console.log(response);
          },
          response => {
            // error callback
            alert("error!");
          }
        );
    }
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