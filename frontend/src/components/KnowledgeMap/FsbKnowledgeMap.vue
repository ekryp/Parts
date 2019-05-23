<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <div class="custom-container" style="paddingTop: 6%">
      <div class="myBreadCrumb">
        <p>
          <span style="font-size: 14px;">{{testPlanConstants.breadcrumbs[0]}}</span>
        </p>
      </div>
      <div class="row">
        <div class="col" align="center">
          <h3>Test Plan</h3>
        </div>
      </div>
      <br>

      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">{{testPlanConstants.tableName}}</h5>
            <br>
            <div class="row">
              <div class="col-lg-6">
                <button
                  class="btn btn-sm btn-success"
                  style="margin-bottom: 2%;marginLeft:1%"
                  @click="showAddRole()"
                >{{testPlanConstants.addButton}}</button>
              </div>
              <div class="col-lg-6">
                <el-col :span="12" class="float-right">
                  <el-input placeholder="Search " v-model="filterParam" @change="getTestPlan()"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables :data="allTestPlan">
                <el-table-column
                  v-for="title in titles"
                  :prop="title.prop"
                  :label="title.label"
                  :key="title.prop"
                  sortable="custom"
                ></el-table-column>
                <el-table-column align="right">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="showEditRole(scope.row)">View</el-button>
                  </template>
                </el-table-column>
              </data-tables>
            </div>
          </div>
        </div>
      </div>
      <!-- </div> -->
    </div>
    <div>
      <!-- Footer -->
      <footer class="footer font-small blue">
        <!-- Copyright -->
        <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
        <!-- Copyright -->
      </footer>
      <!-- Footer -->
    </div>
  </div>
</template>
<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import Multiselect from "vue-multiselect";
import * as constant from "../constant/constant";
//import * as data from "../../utilies/tabledata.json";
import Vudal from "vudal";
import generator from "generate-password";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import { DataTables, DataTablesServer } from "vue-data-tables";
import Vue from "vue";
import lang from "element-ui/lib/locale/lang/en";
import locale from "element-ui/lib/locale";
import BootstrapVue from "bootstrap-vue";

Vue.use(BootstrapVue);
locale.use(lang);

Vue.use(DataTables);
Vue.use(DataTablesServer);
Vue.use(ElementUI);

export default {
  name: "FsbKnowledgeMap",
  components: {
    SideNav,
    headernav,
    Vudal,
    Multiselect,
    Loading
  },
  created() {
    clearInterval(window.intervalObj);
    this.getFSB();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      testPlanConstants: constant.testPlanScreen,
      filterParam: "",
      allTestPlan: [],
      testPlanContent: "",
      addFlag: false,
      editFlag: false,
      fsbData: [],
      testPlanPlaceHolders: {
        fileNamePlaceHolder: "",
        objectivePlaceHolder: "",
        procedurePlaceHolder: ""
      },
      titles: [
        {
          prop: "FSBNumber",
          label: "FSB Number"
        },
        {
          prop: "issueId",
          label: "Issue ID"
        },
        {
          prop: "file_name",
          label: "File Name"
        },
        {
          prop: "title",
          label: "Title"
        },
        {
          prop: "title",
          label: "Title"
        }
      ]
    };
  },
  methods: {
    hideEntry() {
      this.$modals.myModal.$hide();
    },

    showEditRole(user) {
      this.editFlag = true;
      this.addFlag = false;
      this.testPlanContent = user;
      this.$modals.myModal.$show();
    },
    getFSB() {
      this.isLoading = true;
      fetch(
        constant.ELKURL + "api/get_test_plan?search_param=" + this.filterParam,
        {
          method: "GET",
          headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            let array = [];
            for (let i = 0; i < data.data.test_plan.length; i++) {
              this.allTestPlan.push({
                Objective: data.data.test_plan[i].Objective,
                Procedure: data.data.test_plan[i].Procedure,
                file_name: data.data.test_plan[i].file_name
              });
            }
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    }
  }
};
</script>
<style>
/* @media all and (max-width: 720px) and (min-width: 600px) {
    body{
        font-size: 13px;
    }
} */
.vudal {
  width: 950px !important;
}
.labelweight {
  font-weight: 600;
}
.align {
  padding: 6px;
}
</style>
