<template>
  <div>
    <headernav msg="Analysis Dashboard"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="paddingTop:7.57%">
      <div>
        <div class="myBreadCrumb" >
          <p>
            <span style="font-size: 14px;">{{current}}</span>
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
          <div v-if="partsAnalysisRequestList.length !== 0">
          <table id="AnalysisTable" class="table table-borderless table-hover" style="width:100%">
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
                  <td v-if="item.requestStatus ==='Failed'" style="color:red">{{item.requestStatus}}</td>
                  <td style="cursor:pointer">
                    <i class="far fa-eye" @click="update(item)"></i>
                    <i
                      v-if="item.requestStatus ==='Completed'"
                      class="fas fa-poll"
                      @click="summaryResult(item)"
                    ></i>
                    <i
                      v-if="item.requestStatus ==='Failed'"
                      class="fas fa-poll"
                      @click="errorResult(item)"
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
import { AgGridVue } from "ag-grid-vue";

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
    console.log("beforeMount -- get_all_request_analysis", this.$store);
    this.get_all_request_analysis();
    clearInterval(window.intervalObj);
    this.get_dashboard_request_count();
    this.createColumnDefs();
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
      current: "Analysis",
      columnDefs: null,
      rowData: [],
      gridOptions: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        },
        columnStyle: {
          color: "#72879d"
          // fontSize: "11.05px"
        }
      }
    };
  },
  methods: {
    createAnalysis() {
      router.push("/parts/analysis/create");
    },
    update(data) {
      console.log("dasta ----->");
      router.push({
        path: "/parts/analysis/view",
        query: { id: data.analysis_request_id }
      });
    },
    summaryResult(data) {
      router.push({
        path: "/parts/analysis",
        query: { id: data.analysis_request_id }
      });
    },
    errorResult(data) {
      router.push({
        path: "/parts/analysis/error",
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
            $(document).ready(function() {
              $("#AnalysisTable").DataTable();
            });
            for (let i = 0; i < this.partsAnalysisRequestList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.rowData.push({
                analysis_name: this.partsAnalysisRequestList[i].analysis_name,
                analysis_type: this.partsAnalysisRequestList[i].analysis_type,
                customer_name: this.partsAnalysisRequestList[i].customer_name,
                requestStatus: this.partsAnalysisRequestList[i].requestStatus,
                createdDate: new Date(
                  this.partsAnalysisRequestList[i].created_at
                )
                  .toDateString()
                  .substring(4),
                completedFlag:
                  this.partsAnalysisRequestList[i].analysis_request_id +
                  "," +
                  this.partsAnalysisRequestList[i].requestStatus
              });
            }
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
    },
    createColumnDefs() {
      this.columnDefs = [
        {
          headerName: "Analysis Name",
          field: "analysis_name",
          width: 250
        },
        {
          headerName: "Analysis Type",
          field: "analysis_type",
          width: 150
        },
        {
          headerName: "Customer Name",
          field: "customer_name",
          width: 150
        },
        {
          headerName: "Status",
          field: "requestStatus",
          width: 150
        },
        {
          headerName: "Created Date",
          field: "createdDate",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Action",
          field: "completedFlag",
          width: 250,
          cellRenderer: actionCellRenderer
        }
      ];
    }
  }
};

function actionCellRenderer(params) {
  let value = params.value;
  let actionParams = value.split(",");
  let skills = [];
  let analysisId = 55;
  skills.push(
    '<a  style=" background: lightgray;" href="/parts/analysis/create?id=' +
      actionParams[0] +
      '"><i class="far fa-eye"></i></a>'
  );
  if (actionParams[1] === "Completed") {
    skills.push(
      '<a style=" background: lightgray;" href="/parts/analysis?id=' +
        actionParams[0] +
        '"><i  class="fas fa-poll"></i></a>'
    );
  } else if (actionParams[1] === "Failed") {
    skills.push(
      '<a style=" background: lightgray;" href="/parts/analysis/error?id=' +
        actionParams[0] +
        '"><i  class="fas fa-poll"></i></a>'
    );
  }
  return skills.join(" ");
}
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
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
</style>
