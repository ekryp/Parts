<template>
  <div>
    <headernav/>
    <side-nav/>
    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <div class="custom-container" style="paddingTop:7.57%">
      <div>
        <div class="myBreadCrumb">
          <p>
            <span style="font-size: 14px;">{{analysisDashboardConstant.breadcrumb}}</span>
          </p>
        </div>
      </div>

      <div class="float-right" style="marginTop:1%" v-if="createAnalysisFlag === 'true' ">
        <button
          type="button"
          class="btn btn-success"
          @click="createAnalysis"
          v-tooltip.top.hover.focus="'Click to Create'"
        >{{analysisDashboardConstant.createAnalysisButton}}</button>
      </div>
      <!-- <div class="float-left" style="marginTop:1%">
        <button
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Download'"
        >
          <DownloadExcel
            :data="partsAnalysisRequestDownload"
            type="csv"
            name="AnalysisList.csv"
            :columnHeaders="partsAnalysisRequestListTitle"
          >
            <i class="fas fa-file-excel"></i>
            &nbsp;
            {{analysisDashboardConstant.exportButton}}
          </DownloadExcel>
        </button>
      </div>-->
      <br>
      <br>
      <br>
      <table id="example" class="table table-bordered">
        <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Lab Needed</th>
            <th scope="col">Start Time</th>
            <th scope="col">End Time</th>
            <th scope="col">Request Type</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Support Meeting</td>
            <td>Lab 1</td>
            <td>12/02/2019 10.00.00 AM</td>
            <td>12/02/2019 12.00.00 PM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Traffic Problem</td>
            <td>Lab 3</td>
            <td>22/02/2019 10.00.00 AM</td>
            <td>22/02/2019 10.30.00 AM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Part Unavailable</td>
            <td>Lab 2</td>
            <td>01/02/2019 9.00.00 AM</td>
            <td>01/02/2019 10.00.00 AM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Support Meeting</td>
            <td>Lab 1</td>
            <td>12/02/2019 10.00.00 AM</td>
            <td>12/02/2019 12.00.00 PM</td>
            <td>Read Only</td>
          </tr>
          <tr>
            <td>Traffic Problem</td>
            <td>Lab 3</td>
            <td>22/02/2019 10.00.00 AM</td>
            <td>22/02/2019 10.30.00 AM</td>
            <td>Read Only</td>
          </tr>
          <tr>
            <td>Part Unavailable</td>
            <td>Lab 2</td>
            <td>01/02/2019 9.00.00 AM</td>
            <td>01/02/2019 10.00.00 AM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Support Meeting</td>
            <td>Lab 1</td>
            <td>12/02/2019 10.00.00 AM</td>
            <td>12/02/2019 12.00.00 PM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Traffic Problem</td>
            <td>Lab 3</td>
            <td>22/02/2019 10.00.00 AM</td>
            <td>22/02/2019 10.30.00 AM</td>
            <td>Full Admin</td>
          </tr>
          <tr>
            <td>Part Unavailable</td>
            <td>Lab 2</td>
            <td>01/02/2019 9.00.00 AM</td>
            <td>01/02/2019 10.00.00 AM</td>
            <td>Read Only</td>
          </tr>
        </tbody>
      </table>

      <!-- new Table -->
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
import DownloadExcel from "@/components/DownloadExcel/JsonExcel";
import headernav from "@/components/header/header";
import footernav from "@/components/footer/footer";
import SideNav from "@/components/sidenav/sidenav";
import Multiselect from "vue-multiselect";
import { mapState, mapActions, mapGetters } from "vuex";
import Vue from "vue";
import JsonExcel from "vue-json-excel";
import * as constant from "../constant/constant";
import { AgGridVue } from "ag-grid-vue";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

Vue.component("downloadExcel", JsonExcel);

export default {
  name: "PartsAnalysisList",
  components: {
    SideNav,
    Multiselect,
    headernav,
    AgGridVue,
    DownloadExcel,
    Loading
  },

  created() {
    console.log("beforeMount -- get_all_request_analysis", this.$store);
    // this.get_all_request_analysis();
    clearInterval(window.intervalObj);
    this.createAnalysisFlag = localStorage.getItem("createAnalysisFlag");
    console.log("this.createAnalysisFlag", this.createAnalysisFlag);
    //this.get_dashboard_request_count();
    //  this.createColumnDefs();
  },
  // Vuex Configure Its not updating the Value once State Changed
  computed: {},
  data() {
    console.log("Parts-AnalysisReqestList", this.$store.state);
    return {
      isLoading: false,
      fullPage: true,
      analysisDashboardConstant: constant.ListLabScreen,

      options: [
        { name: "Total Analysis Request" },
        { name: "Completed Request" },
        { name: "Completed Request with Error" },
        { name: "Completed Request Successfully" },
        { name: "Requests In Progress" },
        { name: "Requests To Be Submitted" }
      ],
      partsAnalysisRequestListTitle: [
        "Analysis Name",
        "Analysis Type",
        "Customer Name",
        "Status",
        "Created Date"
      ],
      partsAnalysisRequestList: [],
      partsAnalysisRequestDownload: [],
      dashboard_request_count: "",
      current: "Analysis",
      createAnalysisFlag: false,
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
      router.push("/create_event");
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
      this.isLoading = true;
      console.log("working successfully");
      fetch(constant.APIURL + "api/v1/get_steps_all_users", {
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
            console.log("data -getallrequest--->", data);
            this.partsAnalysisRequestList = data;

            for (let i = 0; i < this.partsAnalysisRequestList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.rowData.push({
                analysis_name: this.partsAnalysisRequestList[i].analysis_name,
                analysis_type: this.partsAnalysisRequestList[i].analysis_type,
                customer_name: this.partsAnalysisRequestList[i].customer_name,
                requestStatus: this.partsAnalysisRequestList[i].requestStatus,
                createdDate: new Date(
                  this.partsAnalysisRequestList[i].created_at
                ),
                completedFlag: this.partsAnalysisRequestList[i]
                  .analysis_request_id
              });
              this.partsAnalysisRequestDownload.push({
                analysis_name: this.partsAnalysisRequestList[i].analysis_name,
                analysis_type: this.partsAnalysisRequestList[i].analysis_type,
                customer_name: this.partsAnalysisRequestList[i].customer_name,
                requestStatus: this.partsAnalysisRequestList[i].requestStatus,
                createdDate: new Date(
                  this.partsAnalysisRequestList[i].created_at
                )
                  .toDateString()
                  .substring(4)
              });
            }
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    get_dashboard_request_count() {
      this.isLoading = true;
      fetch(constant.APIURL + "api/v1/get_dashboard_request_count", {
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
            this.isLoading = false;
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
          filter: "date",
          cellRenderer: dateCellRenderer
        },
        {
          headerName: "Action",
          field: "completedFlag",
          width: 250,
          cellRenderer: actionCellRenderer
        }
      ];
    },
    onCellClicked(event) {
      console.dir(event);
      let requestId = event.value;
      if (Number.isInteger(requestId)) {
        router.push({
          path: "/parts/analysis/view",
          query: { id: requestId }
        });
      }
    },
    onReady(event) {
      var gridWidth = document.getElementById("agbox").offsetWidth;

      // keep track of which columns to hide/show
      var columnsToShow = [];
      var columnsToHide = [];

      // iterate over all columns (visible or not) and work out
      // now many columns can fit (based on their minWidth)
      var totalColsWidth = 0;
      var allColumns = event.columnApi.getAllColumns();
      for (var i = 0; i < allColumns.length; i++) {
        let column = allColumns[i];
        totalColsWidth += column.getMinWidth();
        if (totalColsWidth > gridWidth) {
          columnsToHide.push(column.colId);
        } else {
          columnsToShow.push(column.colId);
        }
      }

      // show/hide columns based on current grid width
      event.columnApi.setColumnsVisible(columnsToShow, true);
      event.columnApi.setColumnsVisible(columnsToHide, false);

      // fill out any available space to ensure there are no gaps
      event.api.sizeColumnsToFit();
    }
  }
};
function dateCellRenderer(params) {
  var options = { year: "numeric", month: "long", day: "numeric" };
  let dateVal = params.value.toLocaleDateString("en-US", options);
  return dateVal;
}

function actionCellRenderer(params) {
  let skills = [];

  skills.push('<i style="cursor:pointer" class="far fa-eye"></i>');

  return skills.join(" ");
}
</script>
<style>
.text-top {
  font-size: 1.15vw;
  font-weight: 500;
}
.count {
  font-size: 2.5em;
  font-weight: 600;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.vue-tooltip {
  background-color: white;
  color: #71869e;
}
</style>
