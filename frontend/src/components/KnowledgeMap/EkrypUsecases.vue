<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4>{{useCaseConstants.PopUpHeaders[0]}}</h4>
      </div>
      <div class="content" style="text-align: left">
        <div class="form-group text-left">
          <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>
          <div v-if="viewFlag">
          <br>
          <div class="row"  >
              <div class="col-lg-5">
                <label class="labelweight">{{useCaseConstants.popUpFields[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{useCaseContent.usecase}}</span>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{useCaseConstants.popUpFields[1]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{useCaseContent.briefDescription}}</span>
              </div>
            </div>
            <br>
            
            <div>
              <label class="labelweight">{{useCaseConstants.popUpFields[2]}}</label>
              <br>
              <span class="textOverlay">{{useCaseContent.description}}</span>
              
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
                  v-model="usecase.usecase"
                  :placeholder="useCasePlaceHolders.useCasePlaceHolder"
                ></textarea>
              </div>
            </div>
            <br>
            <div class="row">
              <div class="col-lg-4">
                <label style="{text-align}">Brief Description :</label>
              </div>
              <div class="col-lg-7">
               
                  <b-form-textarea
                  id="textarea"
                  class="textOverlay"
                  v-model="usecase.briefDescription"
                  :placeholder="useCasePlaceHolders.briefDescriptionPlaceHolder"
                  rows="3"
                  max-rows="10"
                ></b-form-textarea>
              </div>
            </div>
            <br>
             <div class="row">
              <div class="col-lg-4">
                <label style="{text-align}">Description :</label>
              </div>
              <div class="col-lg-7">
                <textarea
                  type="text"
                  class="form-control"
                  col=3 
                  v-model="usecase.description"
                  :placeholder="useCasePlaceHolders.descriptionPlaceHolder"
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
          @click="addUseCase()"
        >Create</button>

         <button
          v-if="editFlag"
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Create'"
          @click="updateUseCase()"
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
          <span style="font-size: 14px;">{{useCaseConstants.breadcrumbs[0]}}</span>
        </p>
      </div>
      <div class="row">
        <div class="col" align="center">
          <h3>{{useCaseConstants.tableName}}</h3>
        </div>
      </div>
      <br>

      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">{{useCaseConstants.tableName}}</h5>
            <br>
            <div class="row">
              <div class="col-lg-6">
                <button
                  class="btn btn-sm btn-success"
                  style="margin-bottom: 2%;marginLeft:1%"
                  @click="showUseCase()"
                >{{useCaseConstants.addButton}}</button>
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
                   <el-button size="mini" type="info" @click="showViewUseCase(scope.row)">View</el-button>
                    <el-button size="mini" type="primary" @click="showEditUseCase(scope.row)">Edit</el-button>
                    <el-button size="mini" type="danger" @click="deleteUseCase(scope.row)">Delete</el-button>
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
    this.getUseCase();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      useCaseConstants: constant.UseCaseScreen,
      filterParam: "",
      allUseCase: [],
      useCaseContent: "",
      addFlag: false,
      editFlag: false,
      viewFlag:false,
      usecase: {
        usecase: "",
        description: "",
        briefDescription: ""
      },
      useCasePlaceHolders: {
        useCasePlaceHolder: "Enter the UseCase Here",
        descriptionPlaceHolder:"Enter the Description Here",
        briefDescriptionPlaceHolder: "Enter the Brief Description Here"
       
      },
      filters: [
        {
          prop: ['usecase'],
          value: ''
        }
      ],
      titles: [
        {
          prop: "usecase",
          label: "UseCase Name"
        }
      ]
    };
  },
  methods: {
    hideEntry() {
      this.usecase.usecase="";
      this.usecase.description="";
      this.usecase.briefDescription="";
      
      this.$modals.myModal.$hide();
    },
    showUseCase() {
      this.usecase.usecase="";
      this.usecase.description="";
      this.usecase.briefDescription="";
      this.viewFlag = false;
      this.editFlag = false;
      this.addFlag = true;
      this.$modals.myModal.$show();
    },
    showViewUseCase(user) {
      this.viewFlag = true;
      this.addFlag = false;
      this.editFlag = false;
      this.useCaseContent = user;
      this.$modals.myModal.$show();
    },
    showEditUseCase(user) {
      this.viewFlag = false;
      this.addFlag = false;
      this.editFlag = true;
      this.useCaseContent = user;
      this.usecase.title = user.usecase;
      this.usecase.description=user.description;
      this.usecase.briefDescription = user.briefDescription;
      this.$modals.myModal.$show();
    },
    getUseCase() {
      this.isLoading = true;
      this.allUseCase = [];
      fetch(
          constant.APIURL + "api/v1/get_usecase" ,
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

             let tempJson={ usecase: data[i].usecase,
                description: data[i].description,
                briefDescription: data[i].briefDescription,
                ekryp_usecase_id:data[i].ekryp_usecase_id}
                


              this.allUseCase.push(tempJson);
              tempJson={}
            }
            console.log('This is ',this.allUseCase);
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },

    updateUseCase()
    {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('usecase',this.usecase.usecase);
      formData.append('description',this.usecase.description);
      formData.append('briefDescription',this.usecase.briefDescription);
      formData.append('ekryp_usecase_id',this.useCaseContent.ekryp_usecase_id);
        
      fetch(constant.APIURL + "api/v1/get_usecase", {
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
                    text: "Use Case  Details Updated",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getUseCase();
                    }
                  });
            }
            
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    deleteUseCase(usecase)
    {

       swal({
                    title: "Info",
                    text: "Do You Want to Delete the Data ?",
                    icon: "info"
                  }).then(ok => {
                    if (ok) {
                      this.isLoading = true;
                    
        let formData = new FormData();
     
      formData.append('faq_id',usecase.ekryp_usecase_id);
                 
      
     fetch(constant.APIURL + "api/v1/get_usecase", {
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
                    text: "Use Case Deleted Successfully",
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                       this.getUseCase();
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
    addUseCase() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('usecase',this.usecase.usecase);
      formData.append('description',this.usecase.description);
      formData.append('briefDescription',this.usecase.briefDescription);
        
      fetch(constant.APIURL + "api/v1/get_usecase", {
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
                    text: "Use Case Details Added",
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
