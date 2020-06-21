<template>
<div class="box" >
  <el-table :data="tableData" :default-sort="{prop: 'id', order: 'ascending'}">
    <el-table-column prop="id" label="学生id" sortable width="120"></el-table-column>
    <el-table-column prop="name" label="姓名" width="100"></el-table-column>
    <el-table-column prop="gender" label="性别" width="100"></el-table-column>
    <el-table-column prop="age" label="年龄" width="100"></el-table-column>
    <el-table-column prop="identity" label="身份" width="100"></el-table-column>
    <el-table-column prop="phone" label="电话" width="180"></el-table-column>
    <el-table-column prop="mail" label="邮箱" width="180"></el-table-column>
  </el-table>
</div>
</template>

<script>
export default {
  data() {
    const generateTableData = _ => {
      const tableData = [];
      const students = this.global.user.students;

      students.forEach(student => {
        tableData.push({
          id: student.username,
          name: student.extra.name,
          gender: student.extra.gender,
          age: student.extra.age,
          identity: student.extra.identity,
          phone: student.extra.phonenum,
          mail: student.email
        });
      });
      return tableData;
    };
    return {
      tableData: generateTableData()
    };
  },
  methods: {
    formatter(row, column) {
      return row.address;
    }
  }
};
</script>

<style scoped>
.box {
  width: 880px;
  border: 1px solid #dcdfe6;
  height: 60%;
  margin-left: 10%;
  margin-top: 50px;
}
</style>