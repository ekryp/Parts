<template>
  <div>
    <headernav msg="Spare Details"/>
    <side-nav menu="analysis"/>

    
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div>
      <div class="breadcrumb">
        <p class="in-progress" @click="redirectToAnalysis()">{{postMenu}}/</p><p>{{current}}  </p>
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
          >IB Quantity</a>
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
        </div>
      </nav>
      <div class="tab-content" id="nav-tabContent">
        <div
          class="tab-pane fade show active"
          id="nav-summary"
          role="tabpanel"
          aria-labelledby="nav-summary-tab"
        >
          <AnalysisSummary :analysisId="requestID"/>
        </div>
        <!-- current Inventory -->
        <div
          class="tab-pane fade show"
          id="nav-home"
          role="tabpanel"
          aria-labelledby="nav-home-tab"
        >
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <toggle-button
                :value="state"
                color="green"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                width="80"
                @change="stateChange()"
              />
            </div>
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
          <!-- <div id="progress" class="form_wizard wizard_horizontal">
            <ul id="progress_ul" class="wizard_steps anchor">
              <li>
                <a class="disabled" isdone="0" rel="1">
                  <span class="step_no">1</span>
                  <span class="step_descr">Data Setup and
                    <br>Schema verification
                  </span>
                </a>
              </li>
              <li>
                <a class="disabled" isdone="0" rel="2">
                  <span class="step_no">2</span>
                  <span class="step_descr">Text Preprocessing</span>
                </a>
              </li>
              <li>
                <a class="disabled" isdone="0" rel="3">
                  <span class="step_no">3</span>
                  <span class="step_descr">Feature Generation</span>
                </a>
              </li>
              <li>
                <a class="disabled" isdone="0" rel="4">
                  <span class="step_no" style="backgroundColor:green">4</span>
                  <span class="step_descr">Problem Category
                    <br>Prediction
                  </span>
                </a>
              </li>
              <li>
                <a class="disabled" isdone="0" rel="5">
                  <span id="predictionDownload" class="step_no blink" style="backgroundColor:green">
                    <span>5</span>
                    <i style="display:none" class="fa fa-download"></i>
                  </span>
                  <span class="step_descr">Save Results</span>
                </a>
              </li>
            </ul>
          </div>-->
        </div>
        <div
          class="tab-pane fade"
          id="nav-profile"
          role="tabpanel"
          aria-labelledby="nav-profile-tab"
        >
          <div class="shadow p-3 mb-5 bg-white rounded">
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
          <div class="shadow p-3 mb-5 bg-white rounded">
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
          <div class="shadow p-3 mb-5 bg-white rounded">
            <div class="float-right">
              <toggle-button
                :value="state"
                color="green"
                :sync="true"
                :labels="{checked: 'ReOrder', unchecked: 'Total'}"
                width=80
                @change="stateChange()"
              />
            </div>
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
import ToggleButton from "vue-js-toggle-button";
import * as constant from "../constant/constant";

Vue.use(ToggleButton);

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
      toggle: "total_stock",
      currentInventory: [],
      currentGross: [],
      currentNet: [],
      currentib: [],
      postMenu:"Analysis",
      current:"Analysis Summary"
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
    redirectToAnalysis(){
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
/* .form_wizard .stepContainer {
  display: block;
  position: relative;
  margin: 0;
  padding: 0;
  border: 0 solid #ccc;
  overflow-x: hidden;
}
.wizard_horizontal ul.wizard_steps {
  display: table;
  list-style: none;
  position: relative;
  width: 100%;
  margin: 0 0 20px;
}
.wizard_horizontal ul.wizard_steps li {
  display: table-cell;
  text-align: center;
}
.wizard_horizontal ul.wizard_steps li a,
.wizard_horizontal ul.wizard_steps li:hover {
  display: block;
  position: relative;
  -moz-opacity: 1;
  filter: alpha(opacity=100);
  opacity: 1;
  color: #666;
}
.wizard_horizontal ul.wizard_steps li a:before {
  content: "";
  position: absolute;
  height: 4px;
  background: #ccc;
  top: 20px;
  width: 100%;
  z-index: 4;
  left: 0;
}
.wizard_horizontal ul.wizard_steps li a.disabled .step_no {
  background: #ccc;
}
.wizard_horizontal ul.wizard_steps li a .step_no {
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 100px;
  display: block;
  margin: 0 auto 5px;
  font-size: 16px;
  text-align: center;
  position: relative;
  z-index: 5;
}
.wizard_horizontal ul.wizard_steps li a.selected:before,
.step_no {
  background: #34495e;
  color: #fff;
}
.wizard_horizontal ul.wizard_steps li a.done:before,
.wizard_horizontal ul.wizard_steps li a.done .step_no {
  background: #1abb9c;
  color: #fff;
}
.wizard_horizontal ul.wizard_steps li:first-child a:before {
  left: 50%;
}
.wizard_horizontal ul.wizard_steps li:last-child a:before {
  right: 50%;
  width: 50%;
  left: auto;
} */
.in-progress {
  cursor: pointer;
}
</style>
