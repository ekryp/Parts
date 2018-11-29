<template>
  <div>
    <headernav msg="Spare Part Analysis"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="paddingTop:0%">
      <div class="container">
        <div class="content">
          <h3>Spare Part Analysis</h3>
        </div>
        <div class="container">
          <form style="marginTop: 5%">
            <div class="form-group">
              <div class="row">
                <div class="col-lg-3">
                  <label>Analysis Name :</label>
                </div>
                <div class="col-lg-6">
                  <input
                    v-if="requestId !== '' && partsAnalysisData.analyisisName !== undefined"
                    type="text"
                    class="form-control"
                    v-model="partsAnalysisData.analyisisName"
                    disabled
                  >
                  <input
                    v-if="requestId === ''"
                    type="text"
                    class="form-control"
                    placeholder="Enter Analysis Name"
                    v-model="analyisisName"
                  >
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col-lg-3">
                  <label>Customer Name :</label>
                </div>
                <div class="col-lg-6">
                  <input
                    v-if="requestId !== '' && partsAnalysisData.customerNames !== undefined"
                    type="text"
                    class="form-control"
                    v-model="partsAnalysisData.customerNames"
                    disabled
                  >
                  <multiselect
                    v-if="requestId === '' && partsAnalysis.customer_names !== undefined"
                    :value="customerNames"
                    @input="selectedCustomerName"
                    placeholder="Select Customer"
                    :options="partsAnalysis.customer_names"
                    :multiple="false"
                    :taggable="true"
                  ></multiselect>
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col-lg-3">
                  <label>Date :</label>
                </div>
                <div class="col-lg-6">
                  <input
                    v-if="requestId !== '' && partsAnalysisData.date !== undefined"
                    type="text"
                    class="form-control"
                    placeholder="22 Nov 2018"
                    v-model="partsAnalysisData.date"
                    disabled
                  >
                  <input
                    v-if="requestId === ''"
                    type="text"
                    class="form-control"
                    placeholder="22 Nov 2018"
                    :value="date"
                    disabled
                  >
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col-lg-3">
                  <label>Analysis Type :</label>
                </div>
                <div class="col-lg-6">
                  <input
                    v-if="requestId !== '' && partsAnalysisData.analysisType !== undefined"
                    type="text"
                    class="form-control"
                    v-model="partsAnalysisData.analysisType"
                    disabled
                  >
                  <multiselect
                    v-if="requestId === '' && partsAnalysis.analysis_names !== undefined"
                    v-model="analysisType"
                    @input="selectedAnalysisType"
                    placeholder="Select Analysis Type"
                    :options="partsAnalysis.analysis_names"
                    :multiple="false"
                    :taggable="true"
                  ></multiselect>
                </div>
              </div>
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col-lg-3">
                  <label>Replensih time for MTBF based Analaysis :</label>
                </div>
                <div class="col-lg-6">
                  <input
                    v-if="requestId !== '' && partsAnalysisData.replensihTime !== undefined"
                    type="text"
                    class="form-control"
                    v-model="partsAnalysisData.replensihTime"
                    disabled
                  >
                  <multiselect
                    v-if="requestId === '' && partsAnalysis.replenish_times !== undefined"
                    v-model="replensihTime"
                    @input="selectedReplensihTime"
                    placeholder="Select Replensih Time"
                    :options="partsAnalysis.replenish_times"
                    :multiple="false"
                    :taggable="true"
                  ></multiselect>
                </div>
              </div>
            </div>
            <div class="form-group">
              <!-- <strong>Files To Upload</strong> -->
              <div class="row" style="marginTop:0%">
                <div class="col-lg-3">
                  <label>DNA File :</label>
                </div>
                <div class="col-lg-6 form-group">
                  <div class="row">
                    <div class="col-lg-1" v-if="requestId === ''">
                      <label for="fileupload" class="file">
                        <input
                          type="file"
                          @change="handleFile"
                          id="fileupload"
                          style="display:none"
                        >
                        <i class="fas fa-paperclip fa-2x"></i>
                      </label>
                    </div>
                    <div class="col-lg-8" v-if="requestId === ''">
                      <span v-if="dnafileName === ''">no file selected</span>
                      <span v-if="dnafileName !== ''">{{dnafileName}}</span>
                    </div>
                    <div class="col-lg-8" v-if="requestId !== ''">
                      <span
                        v-if="partsAnalysisData.dnafileName !== ''"
                      >{{partsAnalysisData.dnafileName}}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row" style="marginTop:0%">
                <div class="col-lg-3">
                  <label>SAP File :</label>
                </div>
                <div class="col-lg-6 form-group">
                  <div class="row">
                    <div class="col-lg-1" v-if="requestId === ''">
                      <label for="fileupload2" class="file">
                        <input type="file" @change="sapFile" id="fileupload2" style="display:none">
                        <i class="fas fa-paperclip fa-2x"></i>
                      </label>
                    </div>
                    <div class="col-lg-8" v-if="requestId === ''">
                      <span v-if="sapfileName === ''">no file selected</span>
                      <span v-if="sapfileName !== ''">{{sapfileName}}</span>
                    </div>
                    <div class="col-lg-8" v-if="requestId !== ''">
                      <span
                        v-if="partsAnalysisData.sapfileName !== ''"
                      >{{partsAnalysisData.sapfileName}}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row" style="marginTop:0%">
                <div class="col-lg-3"></div>
                <div class="col-lg-3">
                  <div class="form-check">
                    <input
                      type="checkbox"
                      class="form-check-input"
                      id="exampleCheck1"
                      checked="true"
                    >
                    <label class="form-check-label" for="exampleCheck1">MTBF BOM</label>
                  </div>
                </div>
                <div class="col-lg-3">
                  <div class="form-check">
                    <input
                      type="checkbox"
                      class="form-check-input"
                      id="exampleCheck1"
                      checked="true"
                    >
                    <label class="form-check-label" for="exampleCheck1">Use Total Stock</label>
                  </div>
                </div>
              </div>
              <!-- Status Tracker -->
              <div style="marginTop:2%" v-if="requestId !== ''">
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 6">
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                </div>
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 5">
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 4">
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 3">
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 2">
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div class="row" style="marginLeft:7%" v-if="partsAnalysisData.stepId === 1">
                  <span class="dot-green"></span>
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
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 0 || partsAnalysisData.stepId === undefined "
                >
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
                <!-- error -->
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 0 || partsAnalysisData.stepId === undefined  && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-red"></span>
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
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 5 && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-red"></span>
                  <span class="dot-red"></span>
                </div>
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 4 && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-red"></span>
                  <span class="dot-red"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 3 && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-red"></span>
                  <span class="dot-red"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 2 && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-green"></span>
                  <span class="line-green"></span>
                  <span class="dot-green"></span>
                  <span class="line-red"></span>
                  <span class="dot-red"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                  <span class="line"></span>
                  <span class="dot"></span>
                </div>
                <div
                  class="row"
                  style="marginLeft:7%"
                  v-if="partsAnalysisData.stepId === 1 && partsAnalysisData.requestStatus === 'Failed'"
                >
                  <span class="dot-green"></span>
                  <span class="line-red"></span>
                  <span class="dot-red"></span>
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
                <div class="row">
                  <div class="col-lg-4">
                    <button
                      v-if="requestId === ''"
                      type="button"
                      class="btn btn-danger"
                      @click="cancel()"
                    >cancel</button>
                    <button
                      v-if="requestId !== '' && partsAnalysisData.requestStatus !=='Completed'"
                      type="button"
                      class="btn btn-danger"
                      @click="cancel()"
                      disabled
                    >cancel</button>
                    <button
                      v-if="requestId !== '' && partsAnalysisData.requestStatus ==='Completed'"
                      type="button"
                      class="btn btn-danger"
                      @click="cancel()"
                    >cancel</button>
                  </div>

                  <div class="col-lg-3">
                    <button
                      v-if="requestId === ''"
                      type="button"
                      class="btn btn-success"
                      @click="formSubmit()"
                    >Submit For Analysis</button>
                    <button
                      v-if="requestId !== '' && partsAnalysisData.requestStatus !=='Completed'"
                      type="button"
                      class="btn btn-success"
                      @click="formSubmit()"
                      disabled
                    >Processing</button>
                    <button
                      v-if="requestId !== '' && partsAnalysisData.requestStatus ==='Completed'"
                      type="button"
                      class="btn btn-success"
                      @click="formSubmit()"
                      disabled
                    >Completed</button>
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

  created() {
    if (this.$route.query.id !== undefined) {
      console.log("id ---->", this.$route.query.id);
      this.requestId = this.$route.query.id;
      this.get_request_analysis_by_Id(this.$route.query.id);
    } else {
      console.log("created");
      this.get_spare_part_analysis();
    }
  },
  components: {
    SideNav,
    Multiselect,
    Datepicker,
    headernav
  },
  computed: {
    // partsAnalysis() {
    //   console.log("partsAnalysis--computed");
    //   return this.$store.state.partsAnalysis.spare_part_analysis;
    // },
    // partsAnalysisData() {
    //   return this.$store.state.partsAnalysis.get_request_analysis_by_Id;
    // },
    // status() {
    //   return this.$store.state.partsAnalysis.status;
    // },
    // requestAnalysisSuccess(value) {
    //   console.log("success");
    // }
  },
  data() {
    console.log("Parts-Analysis", this.$store.state);
    return {
      requestId: "",
      dnafileName: "",
      sapfileName: "",
      analyisisName: "",
      customerNames: "",
      analysisType: "",
      replensihTime: "",
      date: new Date(),
      dnafile: "",
      sapfile: "",
      partsAnalysisData: "",
      partsAnalysis: ""
    };
  },
  methods: {
    // ...mapActions("partsAnalysis", [
    //   "get_spare_part_analysis",
    //   "post_spare_part_analysis",
    //   "get_request_analysis_by_Id"
    // ]),
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
      if (
        file.name.endsWith("xlsx") ||
        file.name.endsWith("csv") ||
        file.name.endsWith("XLSX") ||
        file.name.endsWith("CSV")
      ) {
        console.log(file.name);
        this.dnafileName = file.name;
        this.dnafile = file;
      } else {
        alert("error");
      }
    },
    sapFile(e) {
      console.log("image ----sap->", e.target.files);
      const file = e.target.files[0];
      if (
        file.name.endsWith("xlsx") ||
        file.name.endsWith("csv") ||
        file.name.endsWith("XLSX") ||
        file.name.endsWith("CSV")
      ) {
        console.log(file.name);
        this.sapfileName = file.name;
        this.sapfile = file;
      } else {
        alert("error");
      }
    },
    cancel() {
      // router.push("/parts/anlaysis/dashboard");
    },
    formSubmit() {
      let data = {
        dnafileName: this.dnafileName,
        sapfileName: this.sapfileName,
        analyisisName: this.analyisisName,
        customerNames: this.customerNames,
        analysisType: this.analysisType,
        replensihTime: this.replensihTime,
        date: new Date(),
        dnafile: this.dnafile,
        sapfile: this.sapfile
      };
      if (
        this.analyisisName !== "" &&
        this.customerNames !== "" &&
        this.analysisType !== "" &&
        this.replensihTime !== ""
      ) {
        if (this.dnafile !== "") {
          if (this.sapfile !== "") {
            console.log("post data --------->", data);
            this.post_spare_part_analysis(data);
          } else {
            alert("Please add your SAP File");
          }
        } else {
          alert("Please add your DNA File");
        }
      } else {
        alert("Please fill the Form to submit");
      }
    },

    // API calls
    get_request_analysis_by_Id(requestId) {
      fetch(
        "http://10.138.1.2:5000/api/v1/get_steps_specific_request?request_id=" +
          requestId,
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const payload = text && JSON.parse(text);
            console.log("data ---->", payload);
            let object = {
              sapfileName: payload[0].sap_file_name,
              dnafileName: payload[0].dna_file_name,
              analyisisName: payload[0].analysis_name,
              customerNames: payload[0].customer_name,
              analysisType: payload[0].analysis_type,
              replensihTime: payload[0].replenish_time,
              date: payload[0].analysis_request_time,
              requestStatus: payload[0].requestStatus,
              stepName: payload[0].step_name,
              stepId: payload[0].step_id
            };
            this.partsAnalysisData = object;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    get_spare_part_analysis() {
      fetch("http://10.138.1.2:5000/api/v1/get_spare_part_analysis", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data ---->", data);
            this.partsAnalysis = data;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    post_spare_part_analysis(data) {
      let formData = new FormData();
      formData.append("analysis_name", data.analyisisName);
      formData.append("analysis_type", data.analysisType);
      formData.append("replenish_time", data.replensihTime);
      formData.append("customer_dna_file", data.dnafile);
      formData.append("user_email_id", "khali.saran@ekryp.com");
      formData.append("customer_name", data.customerNames);
      formData.append("sap_export_file", data.sapfile);
      console.log("formdata ----->", formData.get("analysis_name"));
      fetch("http://10.138.1.2:5000/api/v1/post_spare_part_analysis", {
        method: "POST",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data ---->", data);
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
.dot-green {
  height: 50px;
  width: 50px;
  background-color: green;
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
.line-green {
  height: 10px;
  width: 110px;
  margin-top: 2%;
  background-color: green;
  display: inline-block;
}
.line-red {
  height: 10px;
  width: 110px;
  margin-top: 2%;
  background-color: red;
  display: inline-block;
}
.dot-red {
  height: 50px;
  width: 50px;
  background-color: red;
  border-radius: 50%;
  display: inline-block;
}
</style>
