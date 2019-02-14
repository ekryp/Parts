// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './vuex/store'
import VTooltip from 'v-tooltip'
import JsonExcel from "vue-json-excel";
import "../node_modules/ag-grid-community/dist/styles/ag-grid.css";
import "../node_modules/ag-grid-community/dist/styles/ag-theme-balham.css";
import ToggleButton from 'vue-js-toggle-button'
import { VudalPlugin } from 'vudal';

Vue.use(VudalPlugin);
Vue.use(ToggleButton)
Vue.component("downloadExcel", JsonExcel);


Vue.use(VTooltip)
Vue.config.productionTip = false


// router.beforeEach((to, from, next) => {
//   next()
//   console.log(to.path);
  
//   if(localStorage.getItem("auth0_access_token"))
//   {
//     var authorization=localStorage.getItem("authorization");
//   var groups=localStorage.getItem("groups");
//   var permissions=authorization.split(',');
//   var flag=true;
//   for(var i=0;i<permissions.length;i++)
//   {
//     if(permissions[i] === to.meta.permission)
//    {
//      flag=false;
//      next()
//    }
//   }
//   if(flag)
//   {
//     next('/')
//   }
// }
//   next()
// })

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
