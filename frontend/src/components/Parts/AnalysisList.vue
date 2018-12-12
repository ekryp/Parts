<template>
  <div>
    <headernav msg="Analysis Dashboard"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
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
          <download-excel :data="partsAnalysisRequestList">
            <i class="fas fa-file-excel"></i>
            &nbsp;
            Export
          </download-excel>
        </button>
      </div>

      <div class="shadow-lg p-3 mb-5 bg-white rounded" style="marginTop:7%">
        <div style="marginTop:0%">
          <div v-if="partsAnalysisRequestList.length !== 0">
            <table id="example" class="table table-borderless table-hover" style="width:100%">
              <thead>
                <tr>
                  <th scope="col">Analysis Name</th>
                  <th scope="col">Analysis Type</th>
                  <th scope="col">Customer Name</th>
                  <th scope="col">Status</th>
                  <th scope="col">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in partsAnalysisRequestList"
                  :key="item.analysis_request_id"
                  style="cursor:pointer"
                >
                  <td>{{item.analysis_name}}</td>
                  <td>{{item.analysis_type}}</td>
                  <td>{{item.customer_name}}</td>
                  <td
                    v-if="item.requestStatus ==='Completed'"
                    style="color:#86B21D"
                  >{{item.requestStatus}}</td>
                  <td
                    v-if="item.requestStatus ==='Processing'"
                    style="color:#2699FB"
                  >{{item.requestStatus}}</td>
                  <td v-if="item.requestStatus ==='failed'" style="color:red">{{item.requestStatus}}</td>
                  <td style="cursor:pointer">
                    <i class="far fa-eye" @click="update(item)"></i>
                    <i
                      v-if="item.requestStatus ==='Completed'"
                      class="fas fa-poll"
                      @click="summaryResult(item)"
                    ></i>
                  </td>
                </tr>
              </tbody>
            </table>
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

Vue.component("downloadExcel", JsonExcel);

export default {
  name: "PartsAnalysisList",
  components: {
    SideNav,
    Multiselect,
    headernav
  },

  created() {
    console.log("beforeMount -- get_all_request_analysis", this.$store);
    this.get_all_request_analysis();
    this.get_dashboard_request_count();
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
      dashboard_request_count: ""
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
            this.partsAnalysisRequestList = data;
            this.exportCSV(data);
            $(document).ready(function() {
              $("#example").DataTable();
            });
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
</style>
