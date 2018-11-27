<template>
    <div v-if="partsAnalysis.status.success">
        <headernav  msg='Spare Part Analaysis'/>
         <side-nav menu="analysis" />
         <div class='custom-container' style="paddingTop:0%">
             <div class='container'>
                 <div class='content'>
                     <h3>Spare Part Analaysis</h3>
                </div>
                <div class='container'>
                    <form style='marginTop: 5%'>
                    <div class='form-group'>
                    <div class='row'>
                        <div class='col-lg-3'>
                            <label>Analysis Name :</label>
                        </div>
                        <div class='col-lg-6'>
                            <input type='text' class='form-control' placeholder='Enter Analysis Name' v-model="analyisisName">
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
                    <div class='row' style="marginTop:0%" >
                        <div class='col-lg-3'>
                            <label>Upload File :</label>
                        </div>
                        <div class='col-lg-6 form-group'>
                            <div class="row">
                            <div class="col-lg-1">
                            <label for='fileupload' class='file'>
                                <input type='file' @change="handleFile" id='fileupload' style="display:none" />
                                 <i class="fas fa-paperclip fa-2x"></i>
                            </label>
                            </div>
                            <div class="col-lg-8" >
                               <span v-if="fileName === ''">no file selected </span>
                               <span v-if="fileName !== ''">{{fileName}} </span>
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="row" style="marginTop:0%">
                        <div class="col-lg-3"></div>
                        <div class="col-lg-3">
                             <div class="form-check">
                             <input type="checkbox" class="form-check-input" id="exampleCheck1" checked="true">
                             <label class="form-check-label" for="exampleCheck1">MTBF BOM</label>
                            </div>
                        </div>
                        <div class="col-lg-3">
                             <div class="form-check">
                             <input type="checkbox" class="form-check-input" id="exampleCheck1" checked='true'>
                             <label class="form-check-label" for="exampleCheck1">Use Total Stock</label>
                            </div>
                        </div>
                    </div>
                    <!-- Status Tracker -->
                    <div style="marginTop:2%">
                        <div class="row" style="marginLeft:7%">
                        <span class="dot"></span>
                        <span class="line"></span>
                        <span class="dot"></span>
                        <span class="line"></span>
                        <span class="dot"></span>
                        <span class="line"></span>
                        <span class="dot"></span>
                        <span class="line"></span>
                        <span class="dot"></span>
                        <span class="line"></span>
                        <span class="dot"></span>
                        </div>
                        <div class="row" style="marginLeft:4%">
                        <div class="col-lg-2">Process Files</div>
                        <div class="col-lg-2">Generating Flat Files</div>
                        <div class="col-lg-2">Combining Flat Files</div>
                        <div class="col-lg-2">Analyzing Data</div>
                        <div class="col-lg-2">Generation BOM</div>
                        <div class="col-lg-2">Generting Output</div>
                        </div>
                    </div>
                    <!-- Tracker Ends -->
                    <div class="float-right" style="marginTop:5%">
                    <div class='row'>
                        <div class="col-lg-3">
                        <button type='button' class='btn btn-danger' @click='cancel()'>cancel</button>
                        </div>
                        <div class="col-lg-3">
                        <button type='button' class='btn btn-success' @click='formSubmit()'>Submit For Analysis</button>
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
import headernav from "@/components/header/header";
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
    Datepicker,
    headernav
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
      fileName: "",
      analyisisName: "",
      customerNames: "",
      analysisType: "",
      replensihTime: "",
      date: new Date(),
      file: ""
    };
  },
  methods: {
    ...mapActions("partsAnalysis", [
      "get_spare_part_analysis",
      "post_spare_part_analysis"
    ]),
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
    handleFile(e) {
      console.log("image ------>", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("xlsx") || file.name.endsWith("csv")) {
        console.log(file.name);
        this.fileName = file.name;
        this.file = file;
      } else {
        alert("error");
      }
    },
    formSubmit() {
      let data = {
        fileName: this.fileName,
        analyisisName: this.analyisisName,
        customerNames: this.customerNames,
        analysisType: this.analysisType,
        replensihTime: this.replensihTime,
        date: new Date(),
        file: this.file
      };
      console.log("post data --------->", data);
      this.post_spare_part_analysis(data);
    }
  }
};
</script>
<style>
.file {
  cursor: pointer;
}
.dot {
  height: 50px;
  width: 50px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
.line {
  height: 10px;
  width: 110px;
  margin-top: 2%;
  background-color: #bbb;
  display: inline-block;
}
</style>
