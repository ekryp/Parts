<template>
  <div>
    <headernav msg="Analysis Dashboard"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div class="row">
        <div class="col-lg-2">
          <span class="text-top">Total Analysis Request</span>
          <br>
        </div>
        <div class="col-lg-2">
          <span class="text-top">Completed Request</span>
          <br>
        </div>
        <div class="col-lg-2">
          <span class="text-top">Completed Request with Error</span>
          <br>
        </div>
        <div class="col-lg-2">
          <span class="text-top">Completed Request Successfully</span>
          <br>
        </div>
        <div class="col-lg-2">
          <span class="text-top">Requests In Progress</span>
          <br>
        </div>
        <div class="col-lg-2">
          <span class="text-top">Requests To Be Submitted</span>
          <br>
        </div>
      </div>
      <div class="row" style="marginTop:0%" v-if="dashboard_request_count !== undefined">
        <div class="col-lg-2">
          <span class="count">{{dashboard_request_count.total_request}}</span>
        </div>
        <div class="col-lg-2">
          <span class="count">{{dashboard_request_count.complete_request}}</span>
        </div>
        <div class="col-lg-2">
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
        <div class="col-lg-2" style="color:green">
          <span class="count">{{dashboard_request_count.complete_request_succesfully}}</span>
        </div>
        <div class="col-lg-2">
          <span class="count">{{dashboard_request_count.incomplete_request}}</span>
        </div>
        <div class="col-lg-2">
          <span class="count">{{dashboard_request_count.saved_request}}</span>
        </div>
      </div>
      <div class="float-right" style="marginTop:1%">
        <button type="button" class="btn btn-success" @click="createAnalysis">Create Analysis</button>
      </div>
      <div class="shadow-lg p-3 mb-5 bg-white rounded" style="marginTop:7%">
        <div class="row">
          <div class="col-lg-4">
            <!-- <input type="text" class="form-control" placeholder="Search by Analysis Name"> -->
          </div>
          <div class="col-lg-4"></div>
          <div class="col-lg-4">
            <!-- <multiselect
              placeholder="Filter By Status"
              :options="options"
              label="name"
              :multiple="false"
              :taggable="true"
            ></multiselect>-->
          </div>
        </div>
        <div style="marginTop:0%">
          <table class="table table-borderless">
            <thead>
              <tr style="color:#26b99a">
                <th scope="col">Analysis Name</th>
                <th scope="col">Analysis Type</th>
                <th scope="col">Customer Name</th>
                <th scope="col">Status</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in partsAnalysisRequestList" :key="item.analysis_request_id">
                <th>{{item.analysis_name}}</th>
                <th>{{item.analysis_type}}</th>
                <th>{{item.customer_name}}</th>
                <th
                  v-if="item.requestStatus ==='Completed'"
                  style="color:#86B21D"
                >{{item.requestStatus}}</th>
                <th
                  v-if="item.requestStatus ==='Processing'"
                  style="color:#2699FB"
                >{{item.requestStatus}}</th>
                <th v-if="item.requestStatus ==='failed'" style="color:red">{{item.requestStatus}}</th>
                <th style="cursor:pointer">
                  <i class="far fa-eye" @click="update(item)"></i>
                  <i
                    v-if="item.requestStatus ==='Completed'"
                    class="fas fa-poll"
                    @click="summaryResult(item)"
                  ></i>
                  <!-- <i class="far fa-trash-alt"></i> -->
                </th>
              </tr>
            </tbody>
          </table>
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

export default {
  name: "PartsAnalysisList",
  components: {
    SideNav,
    Multiselect,
    headernav
  },
  created() {
    console.log("beforeMount -- get_all_request_analysis", this.$store);
    this.get_all_request_analysis();
    this.get_dashboard_request_count();
  },
  // Vuex Configure Its not updating the Value once State Changed
  computed: {
    // ...mapState({
    //   partsAnalysisRequestList: state =>
    //     state.partsAnalysis.get_all_request_analysis,
    //   dashboard_request_count: state =>
    //     state.partsAnalysis.get_dashboard_request_count
    // })
  },
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
      dashboard_request_count: ""
    };
  },
  methods: {
    // ...mapActions("partsAnalysis", [
    //   "get_all_request_analysis",
    //   "get_dashboard_request_count"
    // ]),
    createAnalysis() {
      router.push("/parts/analysis/create");
    },
    update(data) {
      console.log("dasta ----->", data.analysis_request_id);
      router.push({
        path: "/parts/analysis/create",
        query: { id: data.analysis_request_id }
      });
    },
    summaryResult(data) {
      router.push({
        path: "/parts/analysis/summary",
        query: { id: data.analysis_request_id }
      });
    },

    // API Calls
    get_all_request_analysis() {
      console.log("working successfully");
      fetch("http://10.138.1.2:5000/api/v1/get_steps_all_users", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data ---->", data);
            this.partsAnalysisRequestList = data;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_dashboard_request_count() {
      fetch("http://10.138.1.2:5000/api/v1/get_dashboard_request_count", {
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
    }
  }
};
</script>
<style>
.text-top {
  font-size: 13px;
  font-weight: 400;
}
.count {
  font-size: 40px;
  font-weight: 600;
}
</style>
