<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4>{{faqConstants.PopUpHeaders[0]}}</h4>
      </div>
      <div class="content" style="text-align: left">
        <div class="form-group text-left">
          <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>
          <div v-if="viewFlag">
          <br>
          <div class="row"  >
              <div class="col-lg-5">
                <label class="labelweight">{{faqConstants.popUpFields[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{faqContent.title}}</span>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{faqConstants.popUpFields[1]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{faqContent.permissions}}</span>
              </div>
            </div>
            <br>
            
            <div>
              <label class="labelweight">{{faqConstants.popUpFields[2]}}</label>
              <br>
              <span class="textOverlay">{{faqContent.description}}</span>
              
            </div>
            <br>
            
          </div>
          <div v-if="addFlag || editFlag">
           <div class="row">
              <div class="col-lg-4">
                <label style="{text-align}">Title :</label>
              </div>
              <div class="col-lg-7">
                <textarea
                  type="text"
                  class="form-control"
                  col=3 
                  v-model="faq.title"
                  :placeholder="faqPlaceHolders.titlePlaceHolder"
                ></textarea>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-4">
                <label style="{text-align}">Description :</label>
              </div>
              <div class="col-lg-7">
                <!-- <input
                  type="text"
                  class="form-control"
                  v-model="faq.description"
                  :placeholder="faqPlaceHolders.descriptionPlaceHolder"
                > -->
                  <b-form-textarea
                  id="textarea"
                  class="textOverlay"
                  v-model="faq.description"
                  :placeholder="faqPlaceHolders.descriptionPlaceHolder"
                  rows="3"
                  max-rows="10"
                ></b-form-textarea>
              </div>
            </div>
            <br>
             <div class="row">
              <div class="col-lg-4">
                <label style="{text-align}">Permission :</label>
              </div>
              <div class="col-lg-7">
                <textarea
                  type="text"
                  class="form-control"
                  col=3 
                  v-model="faq.permissions"
                  :placeholder="faqPlaceHolders.permissionPlaceHolder"
                ></textarea>
              </div>
            </div>
            <br>
            <!-- <div class="row">
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
               
                <b-form-textarea
                  id="textarea"
                  class="textOverlay"
                  v-model="testPlan.expectedResult"
                  :placeholder="testPlanPlaceHolders.expectedResultPlaceHolder"
                  rows="3"
                  max-rows="6"
                ></b-form-textarea>
              </div>
            </div> -->


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
          <span style="font-size: 14px;">FAQ</span>
        </p>
      </div>
      <div class="row">
        <div class="col" align="center">
          <h3>FAQ</h3>
        </div>
      </div>
      <br>

      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">{{faqConstants.tableName}}</h5>
            <br>
            <div class="row">
              <div class="col-lg-6">
                <button
                  class="btn btn-sm btn-success"
                  style="margin-bottom: 2%;marginLeft:1%"
                  @click="showAddRole()"
                >{{faqConstants.addButton}}</button>
              </div>
              <div class="col-lg-6">
                <el-col :span="12" class="float-right">
                  <el-input placeholder="Search " v-model="filters[0].value"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables :data="allFaq" style="width: 100%" :filters="filters">
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
                   <el-button size="mini" type="info" @click="showViewRole(scope.row)">View</el-button>
                    <el-button size="mini" type="primary" @click="showEditRole(scope.row)">Edit</el-button>
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
    this.getFAQ();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      faqConstants: constant.FaqScreen,
      filterParam: "",
      allFaq: [],
      faqContent: "",
      addFlag: false,
      editFlag: false,
      viewFlag:false,
      faq: {
        title: "",
        description: "",
        permissions: ""
      },
      faqPlaceHolders: {
        titlePlaceHolder: "Enter the Title Here",
        descriptionPlaceHolder:"Enter the Description Here",
        permissionPlaceHolder: "Enter the Permission Here"
       
      },
      filters: [
        {
          prop: ['title'],
          value: ''
        }
      ],
      titles: [
        {
          prop: "title",
          label: "Title"
        }
      ]
    };
  },
  methods: {
    hideEntry() {
      this.faq.title="";
      this.faq.description="";
      this.faq.permission="";
      
      this.$modals.myModal.$hide();
    },
    showAddRole() {
      this.faq.title="";
      this.faq.description="";
      this.faq.permission="";
      this.viewFlag = false;
      this.editFlag = false;
      this.addFlag = true;
      this.$modals.myModal.$show();
    },
    showViewRole(user) {
      this.viewFlag = true;
      this.addFlag = false;
      this.editFlag = false;
      this.faqContent = user;
      this.$modals.myModal.$show();
    },
    showEditRole(user) {
      this.viewFlag = false;
      this.addFlag = false;
      this.editFlag = true;
      this.faqContent = user;
      this.faq.title = user.title;
      this.faq.description=user.description;
      this.faq.permission = user.permission;
      
      this.$modals.myModal.$show();
    },
    getFAQ() {
      this.isLoading = true;
      this.allFaq = [];
      fetch(
          constant.APIURL + "api/v1/get_faq" ,
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
            console.log('Dta',data);
            for (let i = 0; i < data.length; i++) {

             let tempJson={ title: data[i].title,
                description: data[i].description,
                permissions: data[i].permissions,
                faq_id:data[i].faq_id}
                


              this.allFaq.push(tempJson);
              tempJson={}
            }
            console.log('This is ',this.allFaq);
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },

    updateTestPlan()
    {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('title',this.faq.title);
      formData.append('description',this.faq.description);
      formData.append('permissions',this.faq.permissions);
      formData.append('faq_id',this.faqContent.faq_id);
        
      fetch(constant.APIURL + "api/v1/get_faq", {
        method: "PATCH",
        headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          },
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
                    text: "FAQ  Details Updated",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getFAQ();
                    }
                  });
            }
            
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    deleteRole(faq)
    {

       swal({
                    title: "Info",
                    text: "Do You Want to Delete the Data ?",
                    icon: "info"
                  }).then(ok => {
                    if (ok) {
                      this.isLoading = true;
                    
        let formData = new FormData();
     
      formData.append('faq_id',faq.faq_id);
                 
      // formData.append("data", JSON.stringify({
      //     release_number: this.testPlan.release_number,
      //     Objective: this.testPlan.Objective,
      //     Procedure: this.testPlan.Procedure,
      //     setup:this.testPlan.setup,
      //     key:this.testPlanContent.key,
      //     expectedResult:this.testPlan.expectedResult
      //   }));
     fetch(constant.APIURL + "api/v1/get_faq", {
        method: "DELETE",
        headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          },
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
              this.isLoading = false;
               swal({
                    title: "Success",
                    text: "FAQ Deleted Successfully",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getFAQ();
                    }
                  });
            }else{
              swal({
                    title: "Error",
                    text: "Something Went Wrong.Please Try Again",
                    icon: "error"
                  })
            }
            
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
           }
                  });
    },
    addTestPlan() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('title',this.faq.title);
      formData.append('description',this.faq.description);
      formData.append('permissions',this.faq.permissions);
        
      fetch(constant.APIURL + "api/v1/get_faq", {
        method: "PUT",
        headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          },
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
                       this.getFAQ();
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
  text-align: left !important;
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
