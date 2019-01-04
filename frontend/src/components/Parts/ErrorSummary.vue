<template>
  <div>
    <headernav msg="Spare Details"/>
    <side-nav menu="analysis"/>

    <div class="custom-container" style="padding:3%; paddingTop:7.57%; marginLeft:3%">
      <div>
        <div class="myBreadCrumb" style="margin-bottom:1px">
          <p>
            <span class="in-progress" @click="redirectToAnalysis()">{{postMenu}}</span>
            <span style="font-size: 14px;">{{current}}</span>
          </p>
        </div>
      </div>
      <nav>
        <div class="nav nav-tabs" id="nav-tab" role="tablist">
          <a
            class="nav-item nav-link active"
            id="nav-netInventory-tab"
            data-toggle="tab"
            href="#nav-netInventory"
            role="tab"
            aria-controls="nav-netInventory"
            aria-selected="false"
          >Error</a>
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div
          class="tab-pane fade show active"
          id="nav-summary"
          role="tabpanel"
          aria-labelledby="nav-summary-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <br>
            <div class="row" v-if="partsAnalysisSummaryReslut.length !== 0">
              <div class="col-lg-4">
                <div class="form-group">
                  <strong>Analysis Name</strong>
                  <input
                    type="email"
                    v-model="analysisName[0].analysis_name"
                    class="form-control"
                    placeholder="Analysis Name"
                    disabled
                    style="fontSize:1vw; marginTop:2%"
                  >
                </div>
              </div>
              <div class="col-lg-4">
                <div class="form-group">
                  <strong>Customer Name</strong>
                  <input
                    type="email"
                    class="form-control"
                    v-model="partsAnalysisSummaryReslut[0].customer_name"
                    placeholder="Customer Name"
                    disabled
                    style="fontSize:1vw;marginTop:2%"
                  >
                </div>
              </div>
              <div class="col-lg-4">
                <div class="form-group">
                  <strong>Analysis ID</strong>
                  <input
                    type="email"
                    class="form-control"
                    v-model="dispId"
                    placeholder="Analysis Id"
                    disabled
                    style="text-align:right; fontSize:1vw; marginTop:2%"
                  >
                </div>
              </div>
            </div>

            <div class="float-right" style="paddingBottom:1%"></div>

            <table id="example" class="table table-bordered table-hover center">
              <thead>
                <tr>
                  <th scope="col">Parts Name</th>
                  <th scope="col">Error Reason</th>
                  <th scope="col">Node Name</th>
                  <th scope="col">Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in errorData" :key="item.id">
                  <td>{{item.PON}}</td>
                  <td>{{item.error_reason}}</td>
                  <td>{{item.node_name}}</td>
                  <td>{{item.type}}</td>
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
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as data from "./data.json";
import Vue from "vue";
import * as constant from "../constant/constant";

export default {
  name: "ErrorSummary",
  components: {
    SideNav,
    headernav
  },
  created() {
    this.requestId = this.$route.query.id;
    this.get_error_records(this.$route.query.id);
    console.log("requestId ---->", this.$route.query.id);
    this.get_analysis_name(this.$route.query.id);
    this.get_request_analysis_summary_result(this.$route.query.id);
    this.dispId = `AR0000` + this.requestId;
  },
  data() {
    console.log("SpareDetails");
    return {
      requestID: "",
      data: data,
      state: true,
      toggle: "reorder",
      currentInventory: [],
      partsAnalysisSummaryReslut: [],
      dispId: "",
      analysisName: [],
      currentGross: [],
      errorData: [],
      currentib: [],
      postMenu: "Analysis >",
      current: "Error Summary"
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
    redirectToAnalysis() {
      router.push("/parts/analysis/dashboard");
    },
    get_analysis_name(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_analysis_name?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_analysis_name-->", data);
            this.analysisName = data;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_error_records(requestId) {
      fetch(
        constant.APIURL + "api/v1/get_error_records?request_id=" + requestId,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const payload = text && JSON.parse(text);
            console.log("Get Error data ---->", payload);
            this.errorData = payload;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_request_analysis_summary_result(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_summary_specific_request?request_id=" +
          requestId +
          "&toggle=" +
          this.toggle,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_dashboard_request_count-->", data);
            this.partsAnalysisSummaryReslut = data;
            $(document).ready(function() {
              $("#example").DataTable();
            });
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

.in-progress {
  cursor: pointer;
  font-size: 14px;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
</style>
