<template>
  <div>
    <!-- <headernav msg="Analysis Summary Result"/> -->
    <!-- <side-nav menu="analysis"/> -->
    <div style=" marginTop:2%">
      <div class="shadow p-3 mb-5 bg-white rounded">
        <div class="row" v-if="partsAnalysisSummaryReslut.length !== 0">
          <div class="col-lg-4">
            <div class="form-group">
              <strong>Analysis Name</strong>
              <input
                type="email"
                v-model="partsAnalysisSummaryReslut[0].analysis_name"
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
                v-model="partsAnalysisSummaryReslut[0].analysis_request_id"
                placeholder="Analysis Id"
                disabled
                style="text-align:right; fontSize:1vw; marginTop:2%"
              >
            </div>
          </div>
        </div>

        <table id="example" class="table table-bordered table-hover center">
          <thead>
            <tr style="fontSize:1vw">
              <th colspan="4"></th>
              <!-- <th colspan="2">Shared Depot</th> -->
              <th colspan="2">Gross Requirement</th>
              <th colspan="2">Net by Depots</th>
              <th scope="col">Has High Spare?</th>
            </tr>
            <tr style="fontSize:1vw">
              <th scope="col">Item Number</th>
              <th scope="col">Material</th>
              <th scope="col">IB Qty (from BOM)</th>
              <th scope="col">Std Cost ($)</th>
              <!-- <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost</th>-->
              <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost ($)</th>
              <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost ($)</th>
              <th scope="col">Checkbox</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in partsAnalysisSummaryReslut"
              :key="item.analysis_request_id"
              style="fontSize:1vw; cursor:pointer"
            >
              <td class="left">{{item.PON}}</td>
              <td>{{item.material_number}}</td>
              <td>{{item.Qty}}</td>
              <td class="right">{{item.standard_cost | currency('')}}</td>
              <td>{{item.gross_table_count}}</td>
              <td class="right">{{item.extd_std_cost | currency('')}}</td>
              <td>{{item.net_depot_count}}</td>
              <td class="right">{{item.net_extd_std_cost | currency('')}}</td>
              <td>{{item.High_Spares}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import { mapActions, mapState } from "vuex";
import Vue2Filters from "vue2-filters";
import Vue from "vue";

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
    this.get_request_analysis_summary_result(this.requestId);
  },
  computed: {},
  data() {
    console.log("AnalysisSummary", this.$store.state);
    return {
      requestId: "",
      partsAnalysisSummaryReslut: []
    };
  },
  methods: {
    formatPrice(value) {
      let val = (value / 1).toFixed(2).replace(".", ",");
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",", ".");
    },
    spareDetails() {},
    get_request_analysis_summary_result(requestId) {
      fetch(
        "http://10.138.1.2:5000/api/v1/get_summary_specific_request?request_id=" +
          requestId,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_dashboard_request_count-->", data);
            this.partsAnalysisSummaryReslut = data;
            // $(document).ready(function() {
            //   $("#example").DataTable();
            // });
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
</style>
