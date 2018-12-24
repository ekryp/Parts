<template>
    <div>
    <headernav msg="Analysis Dashboard"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div>
        <div class="myBreadCrumb"  style="margin-bottom:1px">
          <p>
          <span  style="font-size: 14px;">{{current}}</span>
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-2 text-center">
          
          <span class="text-top">Total Analysis Request</span>
          <br>
        </div>
        <div class="col-lg-2 text-center">
          <span class="text-top">Completed Request</span>
          <br>
        </div>
        <div class="col-lg-2 text-center">
          <span class="text-top">Completed Request with Error</span>
          <br>
        </div>
        <div class="col-lg-2 text-center">
          <span class="text-top">Completed Request Successfully</span>
          <br>
        </div>
        <div class="col-lg-2 text-center">
          <span class="text-top">Requests In Progress</span>
          <br>
        </div>
        <div class="col-lg-2 text-center">
          <span class="text-top">Requests To Be Submitted</span>
          <br>
        </div>
      </div>
      <div class="row" style="marginTop:0%" v-if="dashboard_request_count !== undefined">
        <div class="col-lg-2 text-center">
          <span class="count">{{dashboard_request_count.total_request}}</span>
        </div>
        <div class="col-lg-2 text-center">
          <span class="count">{{dashboard_request_count.complete_request}}</span>
        </div>
        <div class="col-lg-2 text-center">
          <span
            class="count"
            v-if="dashboard_request_count.failed_request > 0"
            style="color:red"
          >{{dashboard_request_count.failed_request}}</span>
          <span
            class="count"
            v-if="dashboard_request_count.failed_request === 0"
          >{{dashboard_request_count.failed_request}}</span>
        </div>
        <div class="col-lg-2 text-center" style="color:green">
          <span class="count">{{dashboard_request_count.complete_request_succesfully}}</span>
        </div>
        <div class="col-lg-2 text-center">
          <span class="count">{{dashboard_request_count.incomplete_request}}</span>
        </div>
        <div class="col-lg-2 text-center">
          <span class="count">{{dashboard_request_count.saved_request}}</span>
        </div>
      </div>
      <div class="float-right" style="marginTop:1%">
        <button type="button" class="btn btn-success" @click="createAnalysis">Create Analysis</button>
      </div>
      <div class="float-left" style="marginTop:1%">
        <button type="button" class="btn btn-success">
          <download-excel :data="partsAnalysisRequestList" type="csv">
            <i class="fas fa-file-excel"></i>
            &nbsp;
            Export
          </download-excel>
        </button>
      </div>

      <div class="shadow-lg p-3 mb-5 bg-white rounded" style="marginTop:7%">
        <div style="marginTop:0%">
          <div >
            <ag-grid-vue style="width: 1600px; height: 500px;"
                        class="ag-theme-balham"
                        :columnDefs="columnDefs"
                        :rowData="rowData"
                        :enableSorting="true"
                        :enableFilter="true"
                        :pagination= "true"
                        :paginationAutoPageSize="true"
                        >
            </ag-grid-vue>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router/";
import headernav from "@/components/header/header";
import SideNav from "@/components/sidenav/sidenav";
import Multiselect from "vue-multiselect";
import { mapState, mapActions, mapGetters } from "vuex";
import Vue from "vue";
import JsonExcel from "vue-json-excel";
import * as constant from "../constant/constant";
import {AgGridVue} from "ag-grid-vue";

Vue.component("downloadExcel", JsonExcel);

export default {
  name: "PartsAnalysisList",
  components: {
    SideNav,
    Multiselect,
    headernav,
    AgGridVue
  },

  created() {
   
    clearInterval(window.intervalObj);
    console.log("beforeMount -- get_all_request_analysis", this.$store);
    this.get_all_request_analysis();
    this.get_dashboard_request_count();
    this.columnDefs = [
      {headerName: 'Analysis Name', field: 'analysis_name',width: 325},
      {headerName: 'Analysis Type', field: 'analysis_type',width: 325},
      {headerName: 'Customer Name', field: 'customer_name',width: 325},
      {headerName: 'Status', field: 'requestStatus',width: 325},
      {headerName: 'Action', field: 'requestStatus',width: 325}
        ];
        

  },
  // Vuex Configure Its not updating the Value once State Changed
  computed: {},
  data() {
    console.log("Parts-AnalysisReqestList", this.$store.state);
    return {
      options: [
        { name: "Total Analysis Request" },
        { name: "Completed Request" },
        { name: "Completed Request with Error" },
        { name: "Completed Request Successfully" },
        { name: "Requests In Progress" },
        { name: "Requests To Be Submitted" }
      ],
      partsAnalysisRequestList: [],
      dashboard_request_count: "",
      current:'Analysis',
      columnDefs: null,
      rowData: null
      
    };
  },
  methods: {
    createAnalysis() {
      router.push("/parts/analysis/create");
    },
    update(data) {
      console.log("dasta ----->", data.analysis_request_id);
      router.push({
        path: "/parts/analysis/create",
        query: { id: data.analysis_request_id }
      });
    },
    summaryResult(data) {
      router.push({
        path: "/parts/analysis",
        query: { id: data.analysis_request_id }
      });
    },

    exportCSV(data) {
      console.log("data");
    },

    // API Calls
    get_all_request_analysis() {
      console.log("working successfully");
      fetch(constant.APIURL + "api/v1/get_steps_all_users", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.rowData = data;
            this.exportCSV(data);
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_dashboard_request_count() {
      fetch(constant.APIURL + "api/v1/get_dashboard_request_count", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_dashboard_request_count-->", data);
            this.dashboard_request_count = data;
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
.text-top {
  font-size: 1.15vw;
  font-weight: 500;
}
.count {
  font-size: 40px;
  font-weight: 600;
}
.myBreadCrumb
{
 margin-top:-2%;
 margin-bottom: 2%;  
}
</style>
