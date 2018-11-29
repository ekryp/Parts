<template>
  <div>
    <headernav msg="Analysis Summary Result"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div class="row" v-if="partsAnalysisSummaryReslut.length !== 0">
        <div class="col-lg-4">
          <div class="form-group">
            <label>Analysis Name</label>
            <input
              type="email"
              v-model="partsAnalysisSummaryReslut[0].analysis_name"
              class="form-control"
              placeholder="Analysis Name"
              disabled
            >
          </div>
        </div>
        <div class="col-lg-4">
          <div class="form-group">
            <label>Customer Name</label>
            <input
              type="email"
              class="form-control"
              v-model="partsAnalysisSummaryReslut[0].customer_name"
              placeholder="Customer Name"
              disabled
            >
          </div>
        </div>
        <div class="col-lg-4">
          <div class="form-group">
            <label>Analysis ID</label>
            <input
              type="email"
              class="form-control"
              v-model="partsAnalysisSummaryReslut[0].analysis_request_id"
              placeholder="Analysis Id"
              disabled
            >
          </div>
        </div>
      </div>
      <div class="shadow p-3 mb-5 bg-white rounded">
        <table class="table table-bordered center">
          <thead>
            <tr style="fontSize:0.75vw">
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
              <!-- <th colspan="2">Shared Depot</th> -->
              <th colspan="2">Gross Requirement</th>
              <th colspan="2">Net by Depots</th>
              <th scope="col">Has High Spare?</th>
            </tr>
            <tr style="fontSize:0.85vw">
              <th scope="col">Item Number</th>
              <th scope="col">Material</th>
              <th scope="col">IB Qty (from BOM)</th>
              <th scope="col">Std Cost</th>
              <!-- <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost</th>-->
              <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost</th>
              <th scope="col">Qty</th>
              <th scope="col">Ext Std Cost</th>
              <th scope="col">Checkbox</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in partsAnalysisSummaryReslut" :key="item.analysis_request_id">
              <td>{{item.PON}}</td>
              <td>{{item.material_number}}</td>
              <td>{{item.Qty}}</td>
              <td>{{item.standard_cost}}</td>
              <td>{{item.gross_table_count}}</td>
              <td>{{item.extd_std_cost}}</td>
              <td>{{item.net_depot_count}}</td>
              <td>{{item.net_extd_std_cost}}</td>
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

export default {
  name: "PartsAnalysisSummary",
  components: {
    SideNav,
    headernav
  },
  created() {
    this.requestId = this.$route.query.id;
    this.get_request_analysis_summary_result(this.requestId);
  },
  computed: {
    // ...mapState({
    //   partsAnalysisSummaryReslut: state =>
    //     state.partsAnalysis.get_request_analysis_summary_result
    // })
  },
  data() {
    console.log("AnalysisSummary", this.$store.state);
    return {
      requestId: "",
      partsAnalysisSummaryReslut: []
    };
  },
  methods: {
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
</style>
