import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login/Login'
import Callback from '@/components/Login/Callback'
import Dashboard from '@/components/Dashboard/Dashboard'
import PartsAnalysis from '@/components/Parts/Analysis'
import PartsAnalysisList from '@/components/Parts/AnalysisList'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }, {
      path: '/callback',
      name: 'callback',
      component: Callback
    }, {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    }, {
      path: '/parts/analysis',
      name: 'PartsAnalysis',
      component: PartsAnalysis
    }, {
      path: '/parts/analysis-list',
      name: 'PartsAnalysisList',
      component: PartsAnalysisList
    }
  ]
})
