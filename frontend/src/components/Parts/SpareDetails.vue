<template>
  <div>
    <headernav msg="Spare Details"/>
    <side-nav menu="analysis"/>

    <div class="custom-container" style="padding:3%; paddingTop:7.57%;marginLeft:4%">
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
            id="nav-summary-tab"
            data-toggle="tab"
            href="#nav-summary"
            role="tab"
            aria-controls="nav-summary"
            aria-selected="true"
          >Summary Result</a>
          <a
            class="nav-item nav-link"
            id="nav-home-tab"
            data-toggle="tab"
            href="#nav-home"
            role="tab"
            aria-controls="nav-home"
            aria-selected="true"
          >Current Inventory</a>
          <a
            class="nav-item nav-link"
            id="nav-profile-tab"
            data-toggle="tab"
            href="#nav-profile"
            role="tab"
            aria-controls="nav-profile"
            aria-selected="false"
          >Install Base Quantity</a>
          <a
            class="nav-item nav-link"
            id="nav-contact-tab"
            data-toggle="tab"
            href="#nav-contact"
            role="tab"
            aria-controls="nav-contact"
            aria-selected="false"
          >Gross</a>
          <a
            class="nav-item nav-link"
            id="nav-netInventory-tab"
            data-toggle="tab"
            href="#nav-netInventory"
            role="tab"
            aria-controls="nav-netInventory"
            aria-selected="false"
          >Net</a>
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
          class="tab-pane fade show active"
          id="nav-summary"
          role="tabpanel"
          aria-labelledby="nav-summary-tab"
        >
          <br>
          <AnalysisSummary :analysisId="requestID"/>
        </div>
        <!-- current Inventory -->
        <div
          class="tab-pane fade show"
          id="nav-home"
          role="tabpanel"
          aria-labelledby="nav-home-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                @change="stateChange()"
              />
              <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'">
                <download-excel :data="currentInventory" type="csv">
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </download-excel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <table id="currentInventory" class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">Part Name</th>
                  <th scope="col">Depot Name</th>
                  <th v-if="state === true" scope="col">ReOrder Point</th>
                  <th v-if="state === false" scope="col">Total Stock</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in currentInventory" :key="item.summary_id">
                  <th>{{item.part_name}}</th>
                  <td>{{item.depot_name}}</td>
                  <td>{{item.qty}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-profile"
          role="tabpanel"
          aria-labelledby="nav-profile-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'">
                <download-excel :data="currentib" type="csv">
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </download-excel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <table id="currentIBQuantity" class="table table-bordered">
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
            </table>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-contact"
          role="tabpanel"
          aria-labelledby="nav-contact-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <button type="button" class="btn btn-success">
                <download-excel :data="currentGross" type="csv">
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </download-excel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <table id="currentCross" class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">Part Name</th>
                  <th scope="col">Depot Name</th>
                  <th scope="col">Shared Quantity</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in currentGross" :key="i.summary_id">
                  <td>{{i.part_name}}</td>
                  <td>{{i.depot_name}}</td>
                  <td>{{i.gross_qty}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div
          class="tab-pane fade"
          id="nav-netInventory"
          role="tabpanel"
          aria-labelledby="nav-netInventory-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                @change="stateChange()"
              />
              <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'">
                <download-excel :data="currentNet" type="csv">
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </download-excel>
              </button>
            </div>
            <br>
            <br>
            <br>
            <table id="netInventory" class="table table-bordered">
              <thead>
                <tr>
                  <th scope="col">Part Name</th>
                  <th scope="col">Depot Name</th>
                  <th scope="col">Net Quantity</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="i in currentNet" :key="i.summary_id">
                  <td>{{i.part_name}}</td>
                  <td>{{i.depot_name}}</td>
                  <td>{{i.net_qty}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
         <div
          class="tab-pane fade"
          id="nav-error"
          role="tabpanel"
          aria-labelledby="nav-error-tab"
        >
          <br>
          <div class="shadow p-3 mb-5 bg-white rounded">
            <!-- <div class="float-right">
              <toggle-button
                :value="state"
                :color="{checked: 'green', unchecked: 'green'}"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                :width="80"
                @change="stateChange()"
              />
              <button type="button" class="btn btn-success">
                <download-excel :data="currentNet" type="csv">
                  <i class="fas fa-file-excel"></i>
                  &nbsp;
                  Export
                </download-excel>
              </button>
            </div>
            <br>
            <br> -->
            <br>
            <table id="errorTable" class="table table-bordered table-hover center">
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
import AnalysisSummary from "@/components/Parts/AnalysisSummary";
import * as data from "./data.json";
import Vue from "vue";
import * as constant from "../constant/constant";


export default {
  name: "SpareDetails",
  components: {
    SideNav,
    headernav,
    AnalysisSummary
  },
  created() {
    this.requestID = this.$route.query.id;
    console.log("requestId ---->", this.requestId);
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
      state: true,
      toggle: "reorder",
      currentInventory: [],
      currentGross: [],
      currentNet: [],
      currentib: [],
      errorData: [],
      postMenu: "Analysis >",
      current: "Analysis Summary"
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
        this.get_current_net_specific_request(this.$route.query.id);
        this.get_current_inventory_specific_request(this.$route.query.id);
        this.get_current_inventory_specific_request(this.$route.query.id);
      } else {
        this.toggle = "total_stock";
        this.get_current_net_specific_request(this.$route.query.id);
        this.get_current_inventory_specific_request(this.$route.query.id);
        this.get_current_inventory_specific_request(this.$route.query.id);
      }
    },
    get_current_inventory_specific_request(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_current_inventory_specific_request?request_id=" +
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
            console.log(
              "data -- get_current_inventory_specific_request-->",
              data
            );
            this.currentInventory = data;
            $(document).ready(function() {
              $("#currentInventory").DataTable();
            });
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_gross_specific_request(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_gross_specific_request?request_id=" +
          requestId,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_gross_specific_request-->", data);
            this.currentGross = data;
            $(document).ready(function() {
              $("#currentCross").DataTable();
            });
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
    get_current_net_specific_request(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_current_net_specific_request?request_id=" +
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
            console.log("data -- get_current_net_specific_request-->", data);
            this.currentNet = data;
            $(document).ready(function() {
              $("#netInventory").DataTable();
            });
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_current_ib_specific_request(requestId) {
      fetch(
        constant.APIURL +
          "api/v1/get_current_ib_specific_request?request_id=" +
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
            console.log("data -- get_current_ib_specific_request-->", data);
            this.currentib = data;
            $(document).ready(function() {
              $("#currentIBQuantity").DataTable();
            });
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    redirectToAnalysis() {
      router.push("/parts/analysis/dashboard");
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
.vue-tooltip {
    background-color: white;
    color:#71869e;

}
.vue-tooltip {
    background-color: white;
    color:#71869e;
    
}

</style>
