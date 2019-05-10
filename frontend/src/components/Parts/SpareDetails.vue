<template>
  <div>
    <headernav msg="Spare Details"/>
    <side-nav menu="analysis"/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <div class="custom-container" style="padding:3%; paddingTop:7.57%;marginLeft:4%">
      <div>
        <div class="myBreadCrumb" style="margin-bottom:1px">
          <p>
            <span
              class="in-progress"
              @click="redirectToAnalysis()"
            >{{spareDetailsConstant.breadcrumbs[0]}}</span>
            <span style="font-size: 14px;">{{spareDetailsConstant.breadcrumbs[1]}}</span>
          </p>
        </div>

        <div class="row">
          <div class="col-3 text-center">
            <span class="text-top">{{spareDetailsConstant.analysisDetails[0]}}</span>
            <br>

            <span class="count">{{analysisDashboardCount.total_depot}}</span>
          </div>

          <div class="col-3 text-center">
            <span class="text-top">{{spareDetailsConstant.analysisDetails[1]}}</span>
            <br>
            <span class="count" style="color:red">{{analysisDashboardCount.critical_depot}}</span>
          </div>
          <div class="col-3 text-center">
            <span class="text-top">{{spareDetailsConstant.analysisDetails[2]}}</span>
            <br>

            <span class="count">{{analysisDashboardCount.total_pon_type}}</span>
          </div>
          <div class="col-3 text-center">
            <span class="text-top">{{spareDetailsConstant.analysisDetails[3]}}</span>
            <br>
            <span class="count" style="color:red">{{analysisDashboardCount.critical_pon}}</span>
          </div>
        </div>
      </div>
      <br>
      <nav>
        <div class="nav nav-tabs" id="nav-tab" role="tablist">
          <a
            class="nav-item nav-link active"
            id="nav-PONsummary-tab"
            data-toggle="tab"
            href="#nav-PONsummary"
            role="tab"
            aria-controls="nav-PONsummary"
            aria-selected="true"
          >{{spareDetailsConstant.navHeader[0]}}</a>
          <a
            class="nav-item nav-link"
            id="nav-summary-tab"
            data-toggle="tab"
            href="#nav-summary"
            role="tab"
            aria-controls="nav-summary"
            aria-selected="true"
          >{{spareDetailsConstant.navHeader[1]}}</a>

          <a
            class="nav-item nav-link"
            id="nav-home-tab"
            data-toggle="tab"
            href="#nav-home"
            role="tab"
            aria-controls="nav-home"
            aria-selected="true"
          >{{spareDetailsConstant.navHeader[2]}}</a>
          <a
            class="nav-item nav-link"
            id="nav-profile-tab"
            data-toggle="tab"
            href="#nav-profile"
            role="tab"
            aria-controls="nav-profile"
            aria-selected="false"
          >{{spareDetailsConstant.navHeader[3]}}</a>
          <a
            class="nav-item nav-link"
            id="nav-contact-tab"
            data-toggle="tab"
            href="#nav-contact"
            role="tab"
            aria-controls="nav-contact"
            aria-selected="false"
          >{{spareDetailsConstant.navHeader[4]}}</a>
          <a
            class="nav-item nav-link"
            id="nav-netInventory-tab"
            data-toggle="tab"
            href="#nav-netInventory"
            role="tab"
            aria-controls="nav-netInventory"
            aria-selected="false"
          >{{spareDetailsConstant.navHeader[5]}}</a>
          <a
            class="nav-item nav-link"
            id="nav-error-tab"
            data-toggle="tab"
            href="#nav-error"
            role="tab"
            aria-controls="nav-error"
            aria-selected="false"
          >Error</a>
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div
          class="tab-pane fade show"
          id="nav-summary"
          role="tabpanel"
          aria-labelledby="nav-summary-tab"
        >
          <br>
          <AnalysisSummary :analysisId="requestID"/>
        </div>

        <div
          class="tab-pane fade show active"
          id="nav-PONsummary"
          role="tabpanel"
          aria-labelledby="nav-PONsummary-tab"
        >
          <br>
          <PONAnalysisSummary :analysisId="requestID"/>
        </div>
        <!-- current Inventory -->
        <div
          class="tab-pane fade show"
          id="nav-home"
          role="tabpanel"
          aria-labelledby="nav-home-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded" id="CurrDiv">
            <div class="float-right">
              <toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                v-tooltip.top.hover.focus="'Click to Toggle'"
                @change="stateChange()"
              />
              <button
                type="button"
                class="btn btn-success"
                v-tooltip.top.hover.focus="'Click to Download'"
              >
                <DownloadExcel
                  :data="currentInventory"
                  type="csv"
                  name="CurrentInventory.csv"
                  :columnHeaders="currentInventoryTitle"
                >
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </DownloadExcel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <ag-grid-vue
              style="width: 100%; height: 345px;"
              class="ag-theme-balham"
              :columnDefs="currColumnDefs"
              :rowData="currRowData"
              :gridOptions="gridOptions3"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :gridReady="currOnReady"
              :gridSizeChanged="currOnReady"
            ></ag-grid-vue>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-profile"
          role="tabpanel"
          aria-labelledby="nav-profile-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded" id="IbDiv">
            <div class="float-right">
              <button
                type="button"
                class="btn btn-success"
                v-tooltip.top.hover.focus="'Click to Download'"
              >
                <DownloadExcel
                  :data="currentib"
                  type="csv"
                  name="IbQuantity.csv"
                  :columnHeaders="ibTitle"
                >
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </DownloadExcel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <!-- <table id="currentIBQuantity" class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">Product Ordering Name</th>
                  <th scope="col">Node Depot Belongs</th>
                  <th scope="col">PON Quantity</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="x in currentib" :key="x.id">
                  <td>{{x.product_ordering_name}}</td>
                  <td>{{x.node_depot_belongs}}</td>
                  <td>{{x.pon_quanity}}</td>
                </tr>
              </tbody>
            </table>-->
            <ag-grid-vue
              style="width: 100%; height: 345px;"
              class="ag-theme-balham"
              :columnDefs="ibColumnDefs"
              :rowData="ibRowData"
              :gridOptions="gridOptions2"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :gridReady="ibOnReady"
              :gridSizeChanged="ibOnReady"
            ></ag-grid-vue>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-contact"
          role="tabpanel"
          aria-labelledby="nav-contact-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded" id="GrossDiv">
            <div class="float-right">
              <button type="button" class="btn btn-success">
                <DownloadExcel
                  :data="currentGross"
                  type="csv"
                  name="GrossQuantity.csv"
                  :columnHeaders="grossTitle"
                >
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  {{spareDetailsConstant.exportButton}}
                </DownloadExcel>
              </button>
            </div>
            <br>
            <br>
            <br>

            <ag-grid-vue
              style="width: 100%; height: 345px;"
              class="ag-theme-balham"
              :columnDefs="grossColumnDefs"
              :rowData="grossRowData"
              :gridOptions="gridOptions"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :gridReady="grossOnReady"
              :gridSizeChanged="grossOnReady"
            ></ag-grid-vue>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-netInventory"
          role="tabpanel"
          aria-labelledby="nav-netInventory-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded" id="NetDiv">
            <div class="float-right">
              <toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                v-tooltip.top.hover.focus="'Click to Toggle'"
                @change="stateChange()"
              />
              <button
                type="button"
                class="btn btn-success"
                v-tooltip.top.hover.focus="'Click to Download'"
              >
                <DownloadExcel
                  :data="currentNet"
                  type="csv"
                  name="NetQuantity.csv"
                  :columnHeaders="netTitle"
                >
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </DownloadExcel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <ag-grid-vue
              style="width: 100%; height: 345px;"
              class="ag-theme-balham"
              :columnDefs="netColumnDefs"
              :rowData="netRowData"
              :gridOptions="gridOptions1"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :gridReady="netOnReady"
              :gridSizeChanged="netOnReady"
            ></ag-grid-vue>
          </div>
        </div>
        <div class="tab-pane fade" id="nav-error" role="tabpanel" aria-labelledby="nav-error-tab">
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded" id="ErrorDiv">
            <div class="float-right">
              <!--<toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                @change="stateChange()"
              />-->
              <button
                type="button"
                class="btn btn-success"
                v-tooltip.top.hover.focus="'Click to Download'"
              >
                <DownloadExcel
                  :data="errorRowData"
                  type="csv"
                  name="ErrorData.csv"
                  :columnHeaders="errorTitle"
                >
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </DownloadExcel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <ag-grid-vue
              style="width: 100%; height: 400px;"
              class="ag-theme-balham"
              :columnDefs="errorColumnDefs"
              :rowData="errorRowData"
              :gridOptions="ErrorGridOptions"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :gridReady="errorOnReady"
              :gridSizeChanged="errorOnReady"
            ></ag-grid-vue>
          </div>
        </div>
      </div>
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
import AnalysisSummary from "@/components/Parts/AnalysisSummary";
import PONAnalysisSummary from "@/components/Parts/PONAnalysisSummary";
import * as data from "./data.json";
import Vue from "vue";
import * as constant from "../constant/constant";
import { AgGridVue } from "ag-grid-vue";
import DownloadExcel from "@/components/DownloadExcel/JsonExcel";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "SpareDetails",
  components: {
    SideNav,
    headernav,
    AnalysisSummary,
    AgGridVue,
    PONAnalysisSummary,
    DownloadExcel,
    Loading
  },
  created() {
    this.requestID = this.$route.query.id;
    console.log("requestId ---->", this.requestID);
    this.createNetColumnDefs();
    this.createGrossColumnDefs();
    this.createIbColumnDefs();
    this.createCurrColumnDefs();
    this.createErrorColumnDefs();
    this.get_analysis_dashboard_count(this.$route.query.id);
    this.get_error_records(this.$route.query.id);
    this.get_current_inventory_specific_request(this.$route.query.id);
    this.get_gross_specific_request(this.$route.query.id);
    this.get_current_net_specific_request(this.$route.query.id);
    this.get_current_ib_specific_request(this.$route.query.id);
  },
  data() {
    console.log("SpareDetails");
    return {
      requestID: "",
      data: data,
      spareDetailsConstant: constant.SpareSummaryScreen,
      state: true,
      isLoading: false,
      fullPage: true,
      toggle: "reorder",
      currentInventory: [],
      errorTitle: ["Part Name", "Error Reason", "Node Name", "Type"],
      currentInventoryTitle: ["Part Name", "Depot Name", "Reorder Point"],
      currentGross: [],
      currentNet: [],
      netTitle: ["Part Name", "Depot Name", "Net Quantity"],
      currentib: [],
      errorData: [],

      grossColumnDefs: null,
      grossRowData: [],
      grossTitle: ["Part Name", "Depot Name", "Gross Quantity"],
      netColumnDefs: null,
      netRowData: [],
      ibColumnDefs: null,
      ibTitle: ["Depot", "Part", "Quantity"],
      ibRowData: [],
      currColumnDefs: null,
      currRowData: [],
      errorColumnDefs: null,
      errorRowData: [],
      analysisDashboardCount: [],
      postMenu: "Analysis >",
      current: "Analysis Summary",
      gridOptions: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        }
      },
      gridOptions1: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        }
      },
      gridOptions2: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        }
      },
      gridOptions3: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        }
      },
      ErrorGridOptions: {
        rowStyle: {
          color: "#72879d"
          // fontSize: "13.7px",
        }
      }
    };
  },
  mounted() {
    $(document).ready(function() {
      // $("#currentIBQuantity").DataTable();
      // $("#currentInventory").DataTable();
      // $("#netInventory").DataTable();
      // $("#currentCross").DataTable();
    });
  },
  methods: {
    stateChange() {
      this.state = !this.state;

      if (this.state) {
        this.toggle = "reorder";
        this.get_analysis_dashboard_count(this.requestID);
        this.get_current_net_specific_request(this.requestID);
        this.get_current_inventory_specific_request(this.requestID);
      } else {
        this.toggle = "total_stock";
        this.get_analysis_dashboard_count(this.requestID);
        this.get_current_net_specific_request(this.requestID);
        this.get_current_inventory_specific_request(this.requestID);
      }
    },
    // stateChangeFromChild(requestID,toggle) {

    //     this.toggle = toggle;
    //     this.get_analysis_dashboard_count(requestID);
    //     this.get_current_net_specific_request(requestID);
    //     this.get_current_inventory_specific_request(requestID);
    //     this.get_current_inventory_specific_request(requestID);
    //   // } else {
    //   //   this.toggle = "total_stock";
    //   //    this.get_analysis_dashboard_count(requestID);
    //   //   this.get_current_net_specific_request(requestID);
    //   //   this.get_current_inventory_specific_request(requestID);
    //   //   this.get_current_inventory_specific_request(requestID);
    //   // }
    // },
    get_current_inventory_specific_request(requestId) {
      this.isLoading = true;
      this.currRowData = [];
      if (this.toggle === "reorder") {
        this.currColumnDefs = [];
        this.currentInventoryTitle = [
          "Part Name",
          "Depot Name",
          "Reorder Point"
        ];
        this.currColumnDefs = [
          {
            headerName: "Part Name",
            field: "part_name",
            width: 250
          },
          {
            headerName: "Depot Name",
            field: "depot_name",
            width: 150
          },
          {
            headerName: "Reorder Point",
            field: "curr_quantity",
            width: 150,
            cellStyle: { "text-align": "right" }
          }
        ];
      } else if (this.toggle === "total_stock") {
        this.currColumnDefs = [];
        this.currentInventoryTitle = ["Part Name", "Depot Name", "Total Point"];
        this.currColumnDefs = [
          {
            headerName: "Part Name",
            field: "part_name",
            width: 250
          },
          {
            headerName: "Depot Name",
            field: "depot_name",
            width: 150
          },
          {
            headerName: "Total Point",
            field: "curr_quantity",
            width: 150,
            cellStyle: { "text-align": "right" }
          }
        ];
      }

      fetch(
        constant.APIURL +
          "api/v1/get_current_inventory_specific_request?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
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
            console.log(
              "data -- get_current_inventory_specific_request-->",
              data
            );
            this.currOnReady(this.gridOptions3);
            this.currentInventory = data;

            for (let i = 0; i < this.currentInventory.length; i++) {
              this.currRowData.push({
                part_name: this.currentInventory[i].part_name,
                depot_name: this.currentInventory[i].depot_name,
                curr_quantity: this.currentInventory[i].qty
              });
            }
            this.isLoading = false;
            this.currentInventory = this.currRowData;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_gross_specific_request(requestId) {
      this.isLoading = true;
      this.grossRowData = [];
      fetch(
        constant.APIURL +
          "api/v1/get_gross_specific_request?request_id=" +
          requestId,
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
            console.log("data -- get_gross_specific_request-->", data);
            this.currentGross = data;
            for (let i = 0; i < this.currentGross.length; i++) {
              this.grossRowData.push({
                part_name: this.currentGross[i].part_name,
                depot_name: this.currentGross[i].depot_name,
                gross_quantity: this.currentGross[i].gross_qty
              });
            }
            this.isLoading = false;
            this.currentGross = this.grossRowData;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_error_records(requestId) {
      this.isLoading = true;
      this.errorRowData = [];
      fetch(
        constant.APIURL + "api/v1/get_error_records?request_id=" + requestId,
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
            const payload = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            console.log("Get Error data ---->", payload);
            this.errorData = payload;
            for (let i = 0; i < this.errorData.length; i++) {
              this.errorRowData.push({
                part_name: this.errorData[i].PON,
                error_reason: this.errorData[i].error_reason,
                node_name: this.errorData[i].node_name,
                type: this.errorData[i].type
              });
            }

            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_current_net_specific_request(requestId) {
      this.isLoading = true;
      this.netRowData = [];
      fetch(
        constant.APIURL +
          "api/v1/get_current_net_specific_request?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
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
            console.log("data -- get_current_net_specific_request-->", data);
            this.currentNet = data;
            for (let i = 0; i < this.currentNet.length; i++) {
              this.netRowData.push({
                part_name: this.currentNet[i].part_name,
                depot_name: this.currentNet[i].depot_name,
                net_quantity: this.currentNet[i].net_qty
              });
            }
            this.isLoading = false;
            this.currentNet = this.netRowData;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_analysis_dashboard_count(requestId) {
      this.isLoading = true;
      this.analysisDashboardCount = [];
      fetch(
        constant.APIURL +
          "api/v1/get_analysis_dashboard_count?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
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
            console.log("data -- Analysis Dashboard-->", data);
            this.analysisDashboardCount = data;
            this.isLoading = false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_current_ib_specific_request(requestId) {
      this.isLoading = true;
      fetch(
        constant.APIURL +
          "api/v1/get_current_ib_specific_request?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
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
            console.log("data -- get_current_ib_specific_request-->", data);
            this.currentib = data;
            for (let i = 0; i < this.currentib.length; i++) {
              this.ibRowData.push({
                node_depot_belongs: this.currentib[i].node_depot_belongs,
                product_ordering_name: this.currentib[i].product_ordering_name,
                pon_quanity: this.currentib[i].pon_quanity
              });
            }
            this.isLoading = false;
            this.currentib = this.ibRowData;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    redirectToAnalysis() {
      router.push("/parts/analysis/dashboard");
    },
    createGrossColumnDefs() {
      this.grossColumnDefs = [
        {
          headerName: "Part Name",
          field: "part_name",
          width: 250
        },
        {
          headerName: "Depot Name",
          field: "depot_name",
          width: 150
        },
        {
          headerName: "Gross Quantity",
          field: "gross_quantity",
          width: 150,
          cellStyle: { "text-align": "right" }
        }
      ];
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    createNetColumnDefs() {
      this.netColumnDefs = [
        {
          headerName: "Part Name",
          field: "part_name",
          width: 250
        },
        {
          headerName: "Depot Name",
          field: "depot_name",
          width: 150
        },
        {
          headerName: "Net Quantity",
          field: "net_quantity",
          width: 150,
          cellStyle: { "text-align": "right" }
        }
      ];
    },
    createIbColumnDefs() {
      this.ibColumnDefs = [
        {
          headerName: "Depot",
          field: "node_depot_belongs",
          width: 250
        },
        {
          headerName: "Part Name",
          field: "product_ordering_name",
          width: 150
        },
        {
          headerName: "Quantity",
          field: "pon_quanity",
          width: 150,
          cellStyle: { "text-align": "right" }
        }
      ];
    },
    createCurrColumnDefs() {
      this.currColumnDefs = [
        {
          headerName: "Part Name",
          field: "part_name",
          width: 250
        },
        {
          headerName: "Depot Name",
          field: "depot_name",
          width: 150
        },
        {
          headerName: "Reorder Point",
          field: "curr_quantity",
          width: 150,
          cellStyle: { "text-align": "right" }
        }
      ];
    },
    createErrorColumnDefs() {
      this.errorColumnDefs = [
        {
          headerName: "Part Name",
          field: "part_name",
          width: 250
        },
        {
          headerName: "Error Reason",
          field: "error_reason",
          width: 150
        },
        {
          headerName: "Node Name",
          field: "node_name",
          width: 150
        },
        {
          headerName: "Type",
          field: "type",
          width: 150
        }
      ];
    },
    grossOnReady(event) {
      var gridWidth = document.getElementById("GrossDiv").offsetWidth;

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
    },
    netOnReady(event) {
      var gridWidth = document.getElementById("NetDiv").offsetWidth;

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
    },
    ibOnReady(event) {
      var gridWidth = document.getElementById("IbDiv").offsetWidth;

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
    },
    currOnReady(event) {
      var gridWidth = document.getElementById("CurrDiv").offsetWidth;

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
    },
    errorOnReady(event) {
      var gridWidth = document.getElementById("ErrorDiv").offsetWidth;

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
</script>
<style>
a {
  color: black;
  text-decoration: none;
  background-color: transparent;
  -webkit-text-decoration-skip: objects;
}
.nav-tabs .nav-link.active {
  color: #71879e;
  background-color: #fff;
  border-color: #dee2e6 #dee2e6 #fff;
  font-weight: 500;
  font-size: 1.15vw;
}
.nav-tabs .nav-link {
  color: black;
  font-size: 1.15vw;
  border: 1px solid transparent;
  border-top-left-radius: 0.25rem;
  border-top-right-radius: 0.25rem;
}
.text-top {
  font-size: 1.15vw;
  font-weight: 500;
}
.in-progress {
  cursor: pointer;
  font-size: 14px;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.vue-tooltip {
  background-color: white;
  color: #71869e;
}
.count {
  font-size: 2.5em;
  font-weight: 600;
}
</style>
