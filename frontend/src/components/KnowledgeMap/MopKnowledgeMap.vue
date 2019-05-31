<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <vudal name="myModal">
      <div class="header">
        <div class="row">
          <div class="col-lg-11">
            <h4>Patches :</h4>
          </div>
          <div class="col-lg-1 in-progress" @click="hideEntry()">
            <i class="fa fa-times fa-md pull-right" aria-hidden="true"></i>
          </div>
        </div>
      </div>
      <div class="content contentwidth" style="text-align: left">
        <div>
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">File Name :</label>
            </div>
            <div class="col-lg-7">
              <span>{{mopContent.file_name}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">Title :</label>
          <br>
          <span class="textOverlay">{{mopContent.title}}</span>
          <br>

          <div>
            <label class="labelweight">Introduction :</label>

            <span class="textOverlay">{{mopContent.introduction}}</span>
          </div>
        </div>
      </div>
      <div class="actions">
        <button type="button" class="btn btn-success" @click="hideEntry()">OK</button>
      </div>
    </vudal>

    <div class="custom-container" style="paddingTop: 6%">
      <div class="myBreadCrumb">
        <p>
          <span style="font-size: 14px;">Knowledge Map > MOP</span>
        </p>
      </div>
      <div class="row">
        <div class="col" align="center">
          <h3>MOP</h3>
        </div>
      </div>
      <br>

      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">MOP Details</h5>
            <br>
            <div class="row">
              <div class="col-lg-12">
                <el-col :span="6" class="float-right">
                  <el-input placeholder="Search " v-model="filterParam" @change="getMop()"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables :data="allMop">
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
    this.getMop();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      testPlanConstants: constant.testPlanScreen,
      filterParam: "",
      allMop: [],
      mopContent: "",
      addFlag: false,
      editFlag: false,
      testPlanPlaceHolders: {
        fileNamePlaceHolder: "",
        objectivePlaceHolder: "",
        procedurePlaceHolder: ""
      },
      titles: [
        {
          prop: "file_name",
          label: "File Name"
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
      this.mopContent = user;
      this.$modals.myModal.$show();
    },
    getMop() {
      this.isLoading = true;
      this.allMop = [];
      fetch(
        constant.ELKURL + "api/get_all_mop?search_param=" + this.filterParam,
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

            for (let i = 0; i < data.data.mop.length; i++) {
              let tempJson = {
                introduction: data.data.mop[i].introduction,
                index: i,
                title: data.data.mop[i].title,
                file_name: data.data.mop[i].file_name,
                probability: data.data.mop[i].probability,
                key: data.data.mop[i].key
              };
              this.allMop.push(tempJson);
              tempJson = {};
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
  text-align: left !important;
  width: 950px !important;
}
.labelweight {
  font-weight: 600;
  text-align: left;
}
.align {
  padding: 6px;
}
</style>
