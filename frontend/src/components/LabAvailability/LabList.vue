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
      
      <div class id="agbox" style="marginTop:7%">
        <div style="marginTop:0%">
          <div v-if="requestList.length !== 0">
            <ag-grid-vue
              style="width: 100%; height: 500px;"
              class="ag-theme-balham"
              :columnDefs="columnDefs"
              :rowData="rowData"
              :gridOptions="gridOptions"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              :cellClicked="onCellClicked"
              :suppressRowClickSelection="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="15"
              :gridReady="onReady"
              :gridSizeChanged="onReady"
            ></ag-grid-vue>
          </div>
        </div>
      </div>

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
    this.get_lab_request();
    clearInterval(window.intervalObj);
    this.createAnalysisFlag = localStorage.getItem("createAnalysisFlag");
    console.log("this.createAnalysisFlag", this.createAnalysisFlag);
    //this.get_dashboard_request_count();
     this.createColumnDefs();
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
      requestList: [],
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
    get_lab_request() {
      this.isLoading = true;
      console.log("working successfully");
      fetch(constant.APIURL + "api/v1/lab/requests", {
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
            this.requestList = data.data;


            for (let i = 0; i < this.requestList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.rowData.push({
                end_time: this.requestList[i].end_time,
                lab_resource: this.requestList[i].lab_resource,
                requested_date: this.requestList[i].requested_date,
                start_time: this.requestList[i].start_time,
                type: this.requestList[i].type,
                title: this.requestList[i].title

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
          headerName: "Title",
          field: "title",
          width: 250
        },
        {
          headerName: "Lab Needed",
          field: "lab_resource",
          width: 150
        },
        {
          headerName: "Requested Date",
          field: "requested_date",
          width: 150
        },
        {
          headerName: "Start Time",
          field: "start_time",
          width: 150
        },
        {
          headerName: "End Time",
          field: "end_time",
          width: 150
        },
        {
          headerName: "Type",
          field: "type",
          width: 150
         
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
