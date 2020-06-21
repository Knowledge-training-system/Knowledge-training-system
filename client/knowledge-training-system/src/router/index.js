import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import student from '@/components/student'
import userInfo from '@/components/userInfo'
import testPaper from '@/components/testPaper'
import manageStudents from '@/components/manageStudents'
import manageTestpaper from '@/components/manageTestpaper'
import Teacher from '@/components/Teacher'
import account from '@/components/account'
import studentTests from '@/components/studentTests'
import VueResource from 'vue-resource'


Vue.use(VueResource)
Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [{
            path: '/',
            redirect: '/login',
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/student',
            name: 'student',
            component: student,
            children: [{
                    path: '',
                    component: userInfo
                },
                {
                    path: 'info',
                    name: 'userInfo',
                    component: userInfo
                },
                {
                    path: 'tests',
                    name: 'studentTests',
                    component: studentTests
                },
                {
                    path: 'account',
                    name: 'account',
                    component: account
                }
            ]
        },
        {
            path: '/teacher',
            name: 'teacher',
            component: Teacher,
            children: [{
                    path: '',
                    component: userInfo
                },
                {
                    path: 'info',
                    name: 'userInfo',
                    component: userInfo
                },
                {
                    path: 'students',
                    name: 'manageStudents',
                    component: manageStudents
                },
                {
                    path: 'paper',
                    name: 'testPaper',
                    component: testPaper
                },
                {
                    path: 'manage',
                    name: 'manageTestpaper',
                    component: manageTestpaper
                },
                {
                    path: 'account',
                    name: 'account',
                    component: account
                }
            ]

        },


    ]
})