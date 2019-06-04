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
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{faqConstants.popUpFields[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{faqContent.title}}</span>
              </div>
            </div>
            <br>
            <!-- <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{faqConstants.popUpFields[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{faqContent.release_number}}</span>
              </div>
            </div>
            <br>-->

            <div>
              <label class="labelweight">{{faqConstants.popUpFields[2]}}</label>
              <br>
              <span class="textOverlay">{{faqContent.description}}</span>
            </div>
            <br>
          </div>
        </div>
      </div>
      <div class="actions">
        <button
          type="button"
          class="btn btn-success"
          @click="hideEntry()"
          v-tooltip.top.hover.focus="'Cancel the option'"
        >OK</button>
      </div>
    </vudal>

    <div class="custom-container" style="paddingTop: 6%">
      <div class="myBreadCrumb">
        <p>
          <span style="font-size: 14px;">{{faqConstants.breadcrumbs[0]}}</span>
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
              <div class="col-lg-12">
                <el-col :span="8" class="float-right">
                  <el-input placeholder="Search " v-model="filters[0].value"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables
                :data="allFaq"
                style="width: 100%"
                @row-click="showViewRole"
                :filters="filters"
              >
                <el-table-column
                  :min-width="20"
                  v-for="title in titles"
                  :prop="title.prop"
                  :label="title.label"
                  :key="title.prop"
                  sortable="custom"
                ></el-table-column>
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
  name: "Help",
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
      viewFlag: false,
      filters: [
        {
          prop: ["title"],
          value: ""
        }
      ],
      faq: {
        title: "",
        description: "",
        permission: ""
      },
      faqPlaceHolders: {
        titlePlaceHolder: "Enter the Title Here",
        descriptionPlaceHolder: "Enter the Description Here",
        permissionPlaceHolder: "Enter the Permission Here"
      },
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
      this.faq.title = "";
      this.faq.description = "";
      this.faq.permission = "";

      this.$modals.myModal.$hide();
    },
    showAddRole() {
      this.faq.title = "";
      this.faq.description = "";
      this.faq.permission = "";
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
      this.faqContent.title = user.title;
      this.faqContent.description = user.description;
      this.faqContent.permission = user.permission;

      this.$modals.myModal.$show();
    },
    getFAQ() {
      this.isLoading = true;
      this.allFaq = [];
      fetch(constant.APIURL + "api/v1/get_faq", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            let array = [];
            console.log("Dta", data);
            for (let i = 0; i < data.length; i++) {
              let tempJson = {
                title: data[i].title,
                description: data[i].description,
                permissions: data[i].permissions,
                faq_id: data[i].faq_id
              };

              this.allFaq.push(tempJson);
              tempJson = {};
            }
            console.log("This is ", this.allFaq);
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
