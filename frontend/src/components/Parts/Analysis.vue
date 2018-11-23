<template>
    <div v-if="partsAnalysis.status.success">
         <side-nav menu="analysis" />
         <div class='custom-container'>
             <div class='container'>
                 <div class='content'>
                     <h2>Spare Part Analaysis</h2>
                </div>
                <div class='container'>
                    <form style='marginTop: 5%'>
                    <div class='form-group'>
                    <div class='row'>
                        <div class='col-lg-3'>
                            <label>Analysis Name :</label>
                        </div>
                        <div class='col-lg-6'>
                            <input type='text' class='form-control' placeholder='Enter Analysis Name'>
                        </div>
                    </div>
                    </div>
                    <div class='form-group'>
                    <div class='row' >
                        <div class='col-lg-3'>
                            <label>Customer Name :</label>
                        </div>
                        <div class='col-lg-6'>
                                <multiselect :value='customerNames' @input='selectedCustomerName' placeholder='Select Customer' :options='partsAnalysis.spare_part_analysis.customer_names' :multiple='false' :taggable='true' ></multiselect>
                        </div>
                    </div>
                    </div>
                      <div class='form-group'>
                    <div class='row' >
                        <div class='col-lg-3'>
                            <label>Date :</label>
                        </div>
                        <div class='col-lg-6'>
                            <input type='text' class='form-control' placeholder='22 Nov 2018' :value="date" disabled>
                        </div>
                    </div>
                    </div>
                      <div class='form-group'>
                    <div class='row' >
                        <div class='col-lg-3'>
                            <label>Analysis Type :</label>
                        </div>
                        <div class='col-lg-6'>
                                <multiselect v-model='analysisType' @input='selectedAnalysisType' placeholder='Select Analysis Type' :options='partsAnalysis.spare_part_analysis.analysis_names' :multiple='false' :taggable='true'></multiselect>
                        </div>
                    </div>
                    </div>
                      <div class='form-group'>
                    <div class='row' >
                        <div class='col-lg-3'>
                            <label>Replensih time for MTBF based Analaysis :</label>
                        </div>
                        <div class='col-lg-6'>
                                <multiselect v-model='replensihTime' @input='selectedReplensihTime' placeholder='Select Replensih Time'  :options='partsAnalysis.spare_part_analysis.replenish_times' :multiple='false' :taggable='true'></multiselect>
                        </div>
                    </div>
                    </div>
                     <div class='form-group'>
                    <!-- <strong>Files To Upload</strong> -->
                    <div class='row' style="marginTop:2%" >
                        <div class='col-lg-3'>
                            <label>Upload File</label>
                        </div>
                        <div class='col-lg-6'>
                            <label for='fileupload' style='cusor:pointer'>
                                <input type='file' @change="handleImage" id='fileupload' style='display:none' />
                                <i class='fas fa-file'></i>
                            </label>
                        </div>
                    </div>
                    <div class="float-right" style="marginTop:5%">
                    <div class='row'>
                        <div class="col-lg-3">
                        <button type='button' class='btn btn-danger' @click='submit()'>cancel</button>
                        </div>
                        <div class="col-lg-3">
                        <button type='button' class='btn btn-success' @click='submit()'>Submit For Analysis</button>
                        </div>
                    </div>
                    </div>
                    </div>
                    </form>
                </div>
             </div>
         </div>
    </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import Multiselect from "vue-multiselect";
import Datepicker from "vuejs-datepicker";
import { mapState, mapActions } from "vuex";

export default {
  name: "PartsAnalysis",
  watch: {},
  created() {
    console.log("created");
    this.get_spare_part_analysis();
  },
  components: {
    SideNav,
    Multiselect,
    Datepicker
  },
  updated() {
    console.log("updated");
  },
  computed: {
    ...mapState({
      partsAnalysis: state => state.partsAnalysis
    })
  },
  data() {
    console.log("Parts-Analysis", this.$store.state);
    return {
      customerNames: "",
      analysisType: "",
      replensihTime: "",
      date: new Date()
    };
  },
  methods: {
    ...mapActions("partsAnalysis", ["get_spare_part_analysis"]),
    submit() {
      console.log("comming");
    },
    selectedCustomerName(value) {
      this.customerNames = value;
    },
    selectedAnalysisType(value) {
      console.log(value);
      this.analysisType = value;
    },
    selectedReplensihTime(value) {
      console.log(value);
      this.replensihTime = value;
    },
    handleImage(e) {
      console.log("image ------>", e.target.files);
    }
  }
};
</script>
<style>
.content {
  max-width: 500px;
  margin: auto;
  padding: 10px;
}
</style>
