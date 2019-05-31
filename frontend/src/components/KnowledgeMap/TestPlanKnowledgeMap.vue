<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4>{{testPlanConstants.PopUpHeaders[0]}}</h4>
      </div>
      <div class="content">
        <div class="form-group text-left">
          <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>
          <div v-if="viewFlag">
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{testPlanConstants.popUpFields[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{testPlanContent.file_name}}</span>
              </div>
            </div>
            <br>
            <label class="labelweight">{{testPlanConstants.popUpFields[4]}}</label>
            <br>
            <span class="textOverlay">{{testPlanContent.setup}}</span>
            <br>
            <label class="labelweight">{{testPlanConstants.popUpFields[1]}}</label>
            <br>
            <span class="textOverlay">{{testPlanContent.Objective}}</span>
            <br>
            <div>
              <label class="labelweight">{{testPlanConstants.popUpFields[2]}}</label>
              <br>
              <span class="textOverlay">{{testPlanContent.Procedure}}</span>
              
            </div>
            <br>
            <label class="labelweight">{{testPlanConstants.popUpFields[3]}}</label>
            <br>
            <span class="textOverlay">{{testPlanContent.expectedResult}}</span>
            <br>
          </div>
          <div v-if="addFlag || editFlag">
            <div class="row">
              <div class="col-lg-5">
                <label style="{text-align}">File Name :</label>
              </div>
              <div class="col-lg-6">
                <input
                  type="text"
                  class="form-control"
                  v-model="testPlan.file_name"
                  :placeholder="testPlanPlaceHolders.fileNamePlaceHolder"
                >
              </div>
            </div>
            <br>
             <div class="row">
              <div class="col-lg-5">
                <label style="{text-align}">Setup :</label>
              </div>
              <div class="col-lg-6">
                <textarea
                  type="text"
                  class="form-control"
                  col=3 
                  v-model="testPlan.setup"
                  :placeholder="testPlanPlaceHolders.setupPlaceHolder"
                ></textarea>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label style="{text-align}">Objective :</label>
              </div>
              <div class="col-lg-6">
                <input
                  type="text"
                  class="form-control"
                  v-model="testPlan.Objective"
                  :placeholder="testPlanPlaceHolders.objectivePlaceHolder"
                >
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label style="{text-align}">Procedure :</label>
              </div>
              <div class="col-lg-6">
                <!-- <input
                  type="text"
                  class="form-control"
                  v-model="testPlan.procedure"
                  :placeholder="testPlan.procedurePlaceHolder"
                >-->
                <b-form-textarea
                  id="textarea"
                  class="textOverlay"
                  v-model="testPlan.Procedure"
                  :placeholder="testPlanPlaceHolders.procedurePlaceHolder"
                  rows="3"
                  max-rows="10"
                ></b-form-textarea>
              </div>
            </div>
           
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label style="{text-align}">Expected result :</label>
              </div>
              <div class="col-lg-6">
                <!-- <input
                  type="text"
                  class="form-control"
                  v-model="testPlan.procedure"
                  :placeholder="testPlan.procedurePlaceHolder"
                >-->
                <b-form-textarea
                  id="textarea"
                  class="textOverlay"
                  v-model="testPlan.expectedResult"
                  :placeholder="testPlanPlaceHolders.expectedResultPlaceHolder"
                  rows="3"
                  max-rows="6"
                ></b-form-textarea>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="actions">
        <button
          v-if="addFlag"
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Create'"
          @click="addTestPlan()"
        >Create</button>

         <button
          v-if="editFlag"
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Create'"
          @click="updateTestPlan()"
        >Update</button>
        <button v-if="viewFlag" type="button" class="btn btn-success" @click="hideEntry()">Ok</button>

        <button
          v-if="addFlag || editFlag"
          type="button"
          class="btn btn-danger"
          @click="hideEntry()"
          v-tooltip.top.hover.focus="'Cancel the option'"
        >Cancel</button>
      </div>
    </vudal>

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
              <data-tables :data="allTestPlan" style="width: 100%">
                <el-table-column
                 :min-width="120"
                  v-for="title in titles"
                  :prop="title.prop"
                  :label="title.label"
                  :key="title.prop"
                  sortable="custom"
                ></el-table-column :min-width="20">
                <el-table-column align="right">
                  <template slot-scope="scope">
                      <el-button size="mini" type="info" @click="showEditRole(scope.row)">Edit</el-button>
                    <el-button size="mini" type="primary" @click="showViewRole(scope.row)">View</el-button>
                     
                    <el-button size="mini" type="danger" @click="deleteRole(scope.row)">Delete</el-button>
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
  name: "TestPlanKnowledgeMap",
  components: {
    SideNav,
    headernav,
    Vudal,
    Multiselect,
    Loading
  },
  created() {
    clearInterval(window.intervalObj);
    this.getTestPlan();
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
      viewFlag:false,
      testPlan: {
        file_name: "",
        Objective: "",
        Procedure: "",
        expectedResult:"",
        setup:""

      },
      testPlanPlaceHolders: {
        fileNamePlaceHolder: "Enter the File Name Here",
        objectivePlaceHolder: "Enter the Objective Here",
        procedurePlaceHolder: "Enter the Procedure",
        setupPlaceHolder:"Enter the Setup ",
        expectedResultPlaceHolder:"Enter the Expected Result"
      },
      titles: [
        {
          prop: "Objective",
          label: "Objective"
        }
      ]
    };
  },
  methods: {
    hideEntry() {
      this.testPlan.file_name="";
      this.testPlan.Objective="";
      this.testPlan.Procedure="";
      this.testPlan.expectedResult="";
      this.testPlan.setup="";
      this.$modals.myModal.$hide();
    },
    showAddRole() {
       this.testPlan.file_name="";
      this.testPlan.Objective="";
      this.testPlan.Procedure="";
      this.testPlan.expectedResult="";
      this.testPlan.setup="";
      this.viewFlag = false;
      this.editFlag = false;
      this.addFlag = true;
      this.$modals.myModal.$show();
    },
    showViewRole(user) {
      this.viewFlag = true;
      this.addFlag = false;
      this.editFlag = false;
      this.testPlanContent = user;
      this.$modals.myModal.$show();
    },
    showEditRole(user) {
      this.viewFlag = false;
      this.addFlag = false;
      this.editFlag = true;
      this.testPlanContent = user;
      this.testPlan.file_name = user.file_name;
      this.testPlan.Objective = user.Objective;
      this.testPlan.Procedure = user.Procedure;
      this.testPlan.expectedResult = user.expectedResult;
      this.testPlan.setup = user.setup
      this.$modals.myModal.$show();
    },
    getTestPlan() {
      this.isLoading = true;
      this.allTestPlan = [];
      fetch(
          constant.ELKURL + "api/get_all_test_plan?search_param=" + this.filterParam,
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

             let tempJson={ Objective: data.data.test_plan[i].Objective,
                Procedure: data.data.test_plan[i].Procedure,
                file_name: data.data.test_plan[i].file_name,
                 key:data.data.test_plan[i].key}

              if (typeof data.data.test_plan[i].setup !== 'undefined'){
                tempJson['setup']=data.data.test_plan[i].setup
              }
              if (typeof data.data.test_plan[i].expectedResult !== 'undefined'){
                tempJson['expectedResult']=data.data.test_plan[i].expectedResult
              }

              this.allTestPlan.push(tempJson);
              tempJson={}
            }
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },

    updateTestPlan()
    {
let formData = new FormData();
console.log('Test Plan Dat',this.testPlanContent.key);
      formData.append("data", JSON.stringify({
          file_name: this.testPlan.file_name,
          Objective: this.testPlan.Objective,
          Procedure: this.testPlan.Procedure,
          setup:this.testPlan.setup,
          key:this.testPlanContent.key,
          expectedResult:this.testPlan.expectedResult
        }));
      fetch(constant.ELKURL + "api/get_test_plan", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
               this.isLoading = false;
              this.filterParam = "";
              this.$modals.myModal.$hide();
               swal({
                    title: "Success",
                    text: "Test Plan Details Updated",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getTestPlan();
                    }
                  });
            }
            
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    addTestPlan() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append(
        "data",
        JSON.stringify({
          file_name: this.testPlan.file_name,
          Objective: this.testPlan.Objective,
          Procedure: this.testPlan.Procedure,
          setup:this.testPlan.setup,
          expectedResult:this.testPlan.expectedResult
        })
      );
      fetch(constant.ELKURL + "api/get_test_plan", {
        method: "POST",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            
            if (data.http_status_code === 200) {
              this.isLoading = false;
              this.filterParam = "";
              this.$modals.myModal.$hide();
               swal({
                    title: "Success",
                    text: "Test Plan Details Added",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getTestPlan();
                    }
                  });
                
              
            }
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
.textOverlay {
  word-break: break-all;
  white-space: pre-wrap;
}

</style>
