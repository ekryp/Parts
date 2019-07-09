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
              <label class="labelweight">Title :</label>
            </div>
            <div class="col-lg-7">
              <span>{{releaseNoteContent.file_name}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">Description :</label>
          <br>
          <span class="textOverlay">{{releaseNoteContent.description}}</span>
          <br>
          <div
            v-if="(releaseNoteContent.workaround !==' ') && (releaseNoteContent.workaround !=='') "
          >
            <label class="labelweight">Workaround :</label>
            <br>
            <span class="textOverlay">{{releaseNoteContent.workaround}}</span>
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
          <span style="font-size: 14px;">Knowledge Map > Release Notes</span>
        </p>
      </div>
      <div class="row">
        <div class="col" align="center">
          <h3>Release Notes</h3>
        </div>
      </div>
      <br>

      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">Release Notes Details</h5>
            <br>
            <div class="row">
              <div class="col-lg-12">
                <el-col :span="6" class="float-right">
                  <el-input placeholder="Search " v-model="filterParam" @change="getReleaseNotes()"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables :data="allReleaseNotes">
                <el-table-column
                  v-for="title in titles"
                  :prop="title.prop"
                  :label="title.label"
                  :key="title.prop"
                  sortable="custom"
                ></el-table-column>
                <el-table-column align="right">
                  <template slot-scope="scope">
                    <el-button size="mini" type="info" @click="showEditRole(scope.row)">View</el-button>
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
    this.getReleaseNotes();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      testPlanConstants: constant.testPlanScreen,
      filterParam: "",
      allReleaseNotes: [],
      releaseNoteContent: "",
      addFlag: false,
      editFlag: false,
      testPlanPlaceHolders: {
        fileNamePlaceHolder: "",
        objectivePlaceHolder: "",
        procedurePlaceHolder: ""
      },
      titles: [
        {
          prop: "issueId",
          label: "Issue ID"
        },

        {
          prop: "file_name",
          label: "File Name"
        },
        {
          prop: "severity",
          label: "Severity"
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
      this.releaseNoteContent = user;
      this.$modals.myModal.$show();
    },
    getReleaseNotes() {
      this.isLoading = true;
      this.allReleaseNotes = [];
      fetch(
        constant.ELKURL +
          "api/get_release_notes?search_param=" +
          this.filterParam,
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

            for (var j = 0; j < data.data.releaseNotes.length; j++) {
              this.allReleaseNotes.push({
                description: data.data.releaseNotes[j].description,
                index: j,
                file_name: data.data.releaseNotes[j].file_name,
                issueId: data.data.releaseNotes[j].issueId,
                probability: data.data.releaseNotes[j].probability,
                severity: data.data.releaseNotes[j].severity,
                workaround: data.data.releaseNotes[j].workaround,
                key: data.data.releaseNotes[j].key
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
