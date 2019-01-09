<template>
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

    <div class="float-right" style="paddingBottom:1%">
      <toggle-button
        :value="state"
        :color="{checked: 'green', unchecked: 'green'}"
        :sync="true"
        cssColors:true
        :labels="{checked: 'ReOrder', unchecked: 'Total'}"
        :width="80"
        v-tooltip.top.hover.focus="'Click to Toggle'"
        @change="stateChange()"
      />
      <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" >
        <download-excel :data="partsAnalysisSummaryReslut" type="csv">
          <i class="fas fa-file-excel"></i>
          &nbsp;
          Export
        </download-excel>
      </button>
    </div>
    <br>
    <br>
    <br>
    <table id="example" class="table table-bordered table-hover center">
      <thead>
        <tr style="fontSize:1vw">
          <th rowspan="2" scope="col">Part Name</th>
          <th rowspan="2" scope="col">Depot Name</th>
          <th rowspan="2" scope="col">Material</th>
          <th rowspan="2" scope="col">Install Base Quantity</th>
          <th rowspan="2" scope="col">Standard Cost($)</th>
          <th colspan="2" scope="col">Gross Requirement</th>
          <th colspan="2" scope="col">Net Requirement</th>
          <th rowspan="2" scope="col">Has High Spare?</th>
        </tr>
        <tr style="fontSize:1vw">
          <!-- <th scope="col">Customer Name</th> -->
          <th scope="col">Quantity</th>
          <th scope="col">Ext Standard Cost($)</th>
          <th scope="col">Quantity</th>
          <th scope="col">Standard Cost($)</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in partsAnalysisSummaryReslut"
          :key="item.analysis_request_id"
          style="fontSize:1vw; cursor:pointer"
        >
          <!-- <td class="left">{{item.customer_name}}</td> -->
          <td>{{item.part_name}}</td>
          <td>{{item.depot_name}}</td>
          <td>{{item.material_number}}</td>
          <td>{{item.ib_quantity}}</td>
          <td class="right">{{item.standard_cost | currency('')}}</td>
          <td>{{item.gross_qty}}</td>
          <td class="right">{{item.std_gross_cost | currency('')}}</td>
          <td>{{item.net_qty}}</td>
          <td class="right">{{item.net_std_cost | currency('')}}</td>
          <td v-if="item.high_spare != 0">
            <input type="checkbox" name="vehicle3" value="{item.high_spare}" checked>
          </td>
          <td v-else>
            <input type="checkbox" name="vehicle3" value="{item.high_spare}">
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import { mapActions, mapState } from "vuex";
import Vue2Filters from "vue2-filters";
import Vue from "vue";
import * as constant from "../constant/constant";
import { AgGridVue } from "ag-grid-vue";
import Tooltip from 'vue-directive-tooltip';
import 'vue-directive-tooltip/css/index.css';
Vue.use(Tooltip);

Vue.use(Vue2Filters);
export default {
  name: "PartsAnalysisSummary",
  props: ["analysisId"],
  components: {
    SideNav,
    headernav
  },
  created() {
    console.log("props ----->", this.$props);
    this.requestId = this.$props.analysisId;
    this.dispId = `AR0000` + this.requestId;
    this.get_request_analysis_summary_result(this.requestId);
    this.get_analysis_name(this.requestId);
  },
  computed: {},
  data() {
    console.log("AnalysisSummary", this.$store.state);
    return {
      requestId: "",
      partsAnalysisSummaryReslut: [],
      dispId: "",
      analysisName: [],
      toggle: "reorder",
      state: true,
      columnDefs: null,
      rowData: null,
      msg:"gededed"
    };
  },
  methods: {
    formatPrice(value) {
      let val = (value / 1).toFixed(2).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",", ".");
    },
    stateChange() {
      this.state = !this.state;
      if (this.state) {
        console.log(this.toggle);
        this.toggle = "reorder";
        this.get_request_analysis_summary_result(this.requestId);
      } else {
        this.toggle = "total_stock";
        this.get_request_analysis_summary_result(this.requestId);
      }
    },
    spareDetails() {},
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
.center {
  text-align: center;
}
.left {
  text-align: left;
}
.right {
  text-align: right;
}
.form-control:disabled,
.form-control[readonly] {
  background-color: #f5f5f5 !important;
  opacity: 1;
}
.vue-tooltip {
    background-color: white;
    color:#71869e;
    
}



</style>
