<template>
  <div>
    <headernav msg="Spare Part Analysis" :loaderFlag="loaderFlag"/>
    <side-nav menu="analysis" :diasableFlag="diasableFlag"/>
    <div class="custom-container" style="paddingTop:3%">
      <!-- <div class="container"> -->
      <form style="marginTop: 5%;">
        <div>
          <div class="myBreadCrumb">
            <p>
              <span class="in-progress" @click="cancel()">{{postMenu}}</span>
              <span v-if="requestId!==''" style="font-size: 14px;">{{createAnalysisConstant.breadcrumbs[0]}}</span>
              <span v-if="requestId===''" style="font-size: 14px;">{{createAnalysisConstant.breadcrumbs[1]}}</span>
            </p>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-3">
              <label>{{createAnalysisConstant.createAnalysisLabels[0]}}</label>
            </div>
            <div class="col-lg-6">
              <input
                v-if="requestId === ''"
                type="text"
                class="form-control"
                :placeholder="createAnalysisConstant.createAnalysisPlaceHolders[0]"
                v-model="analyisisName"
              >
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-3">
              <label>{{createAnalysisConstant.createAnalysisLabels[1]}}</label>
            </div>
            <div class="col-lg-6">
              <multiselect
                v-if="requestId === '' && partsAnalysis.customer_names !== undefined"
                :value="customerNames"
                @input="selectedCustomerName"
                :placeholder="createAnalysisConstant.createAnalysisPlaceHolders[1]"
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
              <label>{{createAnalysisConstant.createAnalysisLabels[2]}}</label>
            </div>
            <div class="col-lg-6">
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
              <label>{{createAnalysisConstant.createAnalysisLabels[3]}}</label>
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
                :placeholder="createAnalysisConstant.createAnalysisPlaceHolders[2]"
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
              <label>{{createAnalysisConstant.createAnalysisLabels[4]}}</label>
            </div>
            <div class="col-lg-6">
              <multiselect
                v-if="requestId === '' && partsAnalysis.replenish_times !== undefined"
                v-model="replensihTime"
                @input="selectedReplensihTime"
                :placeholder="createAnalysisConstant.createAnalysisPlaceHolders[3]"
                :options="partsAnalysis.replenish_times"
                :multiple="false"
                :taggable="true"
              ></multiselect>
            </div>
          </div>
        </div>
        <div class="row" style="marginTop:0%">
           <div class="col-lg-3">
             <label>{{createAnalysisConstant.createAnalysisLabels[8]}}</label>
           </div>
           
           <div class="col-lg-2">
             <input type="checkbox" id="checkbox" v-model="mtbf">

           </div>
          </div>
          <br>
        <div class="form-group">
          
          <div class="row" style="marginTop:0%" >
            <div class="col-lg-3">
              <label>{{createAnalysisConstant.createAnalysisLabels[5]}}</label>
            </div>
            <div class="col-lg-6 form-group">
              <div class="row">
                <div class="col-lg-2">
             <input type="radio" id="DNA" value="dna" v-model="fileType">
             &nbsp
             <label>DNA </label>
           </div>
           <div class="col-lg-2">
             <input type="radio" id="BOM" value="bom" v-model="fileType">
           &nbsp
             <label>BOM</label>
           </div> 
                
              </div>
              <!-- <div class="row" style="marginTop:3%">
                
              </div> -->
            </div>
          </div>

          <div class="row" style="marginTop:0%">
            <div class="col-lg-3">

              <label v-if="fileType === 'dna'">{{createAnalysisConstant.createAnalysisLabels[9]}}</label>
              <label v-if="fileType === 'bom'">{{createAnalysisConstant.createAnalysisLabels[7]}}</label>
            </div >
            <div class="col-lg-6 form-group">
              <div class="row">
                <div class="col-lg-1" v-if="fileType === 'dna'">
                  <label for="fileupload" class="file">
                    <input type="file" @change="handleFile" id="fileupload" style="display:none">
                    <i class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                  
                <div class="col-lg-5" v-if="fileType === 'dna'" >
                  <span v-if="dnafileName === ''">{{createAnalysisConstant.createAnalysisPlaceHolders[4]}}</span>
                  <span v-if="dnafileName !== ''">{{dnafileName}}</span>
                </div>
                <div class="col-lg-5" v-if="fileType === 'dna'">
                  <span
                    v-if="partsAnalysisData.dnafileName !== ''"
                  >{{partsAnalysisData.dnafileName}}</span>
                </div>
                 <div class="col-lg-1" v-if="fileType === 'bom'">
                  <label for="fileupload" class="file">
                    <input type="file" @change="bomFileEvent" id="fileupload" style="display:none">
                    <i class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                 <div class="col-lg-5" v-if="fileType === 'bom'">
                  <span v-if="bomFileName === ''">{{createAnalysisConstant.createAnalysisPlaceHolders[4]}}</span>
                  <span v-if="bomFileName !== ''">{{bomFileName}}</span>
                </div>
                <div class="col-lg-5" v-if="fileType === 'bom'">
                  <span
                    v-if="partsAnalysisData.bomFileName !== ''"
                  >{{partsAnalysisData.bomFileName}}</span>
                </div>
              </div>
            </div>
          </div>

         

          <div class="row" style="marginTop:0%">
            <div class="col-lg-3">
              <label>{{createAnalysisConstant.createAnalysisLabels[6]}}</label>
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
                  <span v-if="sapfileName === ''">{{createAnalysisConstant.createAnalysisPlaceHolders[4]}}</span>
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
          <!-- <div class="row" style="marginTop:0%">
              <div class="col-lg-3"></div>
              <div class="col-lg-3">
                <div class="form-check">
                  <input type="checkbox" class="form-check-input" id="exampleCheck1" checked="true">
                  <label class="form-check-label" for="exampleCheck1">MTBF BOM</label>
                </div>
              </div>
              <div class="col-lg-3">
                <div class="form-check">
                  <input type="checkbox" class="form-check-input" id="exampleCheck1" checked="true">
                  <label class="form-check-label" for="exampleCheck1">Use Total Stock</label>
                </div>
              </div>
          </div>-->
          <div class="float-right" style="marginBottom:5%">
            <div class="row">
              <button type="button" v-if="uploading" class="btn btn-danger" disabled>{{createAnalysisConstant.buttons[0]}}</button>&nbsp; &nbsp;
              <button
                type="button"
                v-if="!uploading"
                class="btn btn-danger"
                @click="cancel()"
                v-tooltip.top.hover.focus="'Move to Analysis Dashboard'"
              >{{createAnalysisConstant.buttons[0]}}</button>&nbsp; &nbsp;
              <button
                v-if="requestId === '' && !uploading && !resubmit"
                type="button"
                class="btn btn-success"
                @click="formSubmit()"
                v-tooltip.top.hover.focus="'Click to Submit'"
              >{{createAnalysisConstant.buttons[1]}}</button>
              <button
                v-if="requestId === '' && !uploading && resubmit"
                type="button"
                class="btn btn-success"
                @click="formSubmit()"
                v-tooltip.top.hover.focus="'Click to Resubmit'"
              >{{createAnalysisConstant.buttons[2]}}</button>
              <button v-if="uploading " type="button" class="btn btn-success" disabled>{{createAnalysisConstant.buttons[3]}}</button>
            </div>
          </div>
        </div>
      </form>
      <!-- </div> -->

    </div>
     <div>
        <!-- Footer -->
        <footer class="footer fixed-bottom font-small blue">
          <!-- Copyright -->
          <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
          <!-- Copyright -->
        </footer>
        <!-- Footer -->
      </div>
  </div>
</template>
<script>
import Vue from "vue";
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import Multiselect from "vue-multiselect";
import Datepicker from "vuejs-datepicker";
import { mapState, mapActions } from "vuex";
import * as constant from "../constant/constant";
import swal from "sweetalert";
import * as sampleBomData from "../../utilies/sampleBOM.txt";

export default {
  name: "CreateAnalysis",

  created() {
    clearInterval(window.intervalObj);
    console.log("created");
    this.get_spare_part_analysis();
  },
  components: {
    SideNav,
    Multiselect,
    Datepicker,
    headernav
  },
  computed: {},
  data() {
    console.log("Parts-Analysis", this.$store.state);
    return {
      createAnalysisConstant:constant.CreateAnalysisScreen,
      requestId: "",
      dnafileName: "",
      sapfileName: "",
      bomFileName: "",
      analyisisName: "",
      customerNames: "",
      analysisType: "4 Hr Analysis",
      replensihTime: "Ratio of PON - 2Day",
      date: new Date(),
      dnafile: "",
      sapfile: "",
      bomFile:"",
      partsAnalysisData: "",
      partsAnalysis: "",
      partsClose: true,
      showPartsChild: false,
      postMenu: "Analysis >",
      current: "Analysis Update",
      show: false,
      label: "Loading...",
      errorData: [],
      uploading: false,
      resubmit: false,
      loaderFlag: false,
      diasableFlag: false,
      mtbf:true,
      fileType:"dna",
    
      sampleBOM:sampleBomData
      };
  },
  methods: {
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
        file.name.endsWith("CSV") ||
        file.name.endsWith("txt") ||
        file.name.endsWith("TXT")
      ) {
        console.log(file.name);
        this.dnafileName = file.name;
        this.dnafile = file;
      } else {
       swal({
              title: "Error",
              text: "Please Upload a .CSV or .TXT or .XLSX File",
              icon: "error"
            });
      }
    },
   
    bomFileEvent(e) {
      console.log("image ------>", e.target.files);
      const file = e.target.files[0];
      if (
        file.name.endsWith("xlsx")||
        file.name.endsWith("csv") ||
        file.name.endsWith("XLSX") ||
        file.name.endsWith("CSV")

      ) {
        console.log(file.name);
        this.bomFileName = file.name;
        this.bomFile = file;
      } else {
       swal({
              title: "Error",
              text: "Please Upload a .CSV or .XSLX File",
              icon: "error",
                buttons:{
                  download :{
                    text:"Download Sample",
                    value:"yes"
                    },
                    ok : true
                      },
                      })
                  .then((value) => {
                    switch (value) {
                    case "yes":
                    this.downloadSampleBOM();
                    }
              
            });
      }
    },
    downloadSampleBOM() {
      var fileContent = String(this.sampleBOM);
      var fileType = "csv";

      fileType = fileType || "csv";
      var blobType = "text/csv";
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(
        new Blob([fileContent], { type: blobType })
      );
      a.download = "SampleBOM" + "." + fileType;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
    },
    sapFile(e) {
      console.log("image ----sap->", e.target.files);
      const file = e.target.files[0];
      if (
        file.name.endsWith("xlsx") ||
        file.name.endsWith("xls") ||
        file.name.endsWith("XLSX") ||
        file.name.endsWith("XLS") 
       
        
      ) {
        console.log(file.name);
        this.sapfileName = file.name;
        this.sapfile = file;
      } else {
        swal({
              title: "Error",
               text: "Please Upload a  .XLS or .XLSX File",
              icon: "error"
              
                    });
      }
    },
    
    cancel() {
      router.push("/parts/analysis/dashboard");
    },
    routeToView(data) {
      router.push({
        path: "/parts/analysis/view",
        query: { id: data.analysis_id }
      });
    },
    formSubmit() {
      var mtbfValue;
      if(this.mtbf)
      {
        mtbfValue="yes";
      }else
      {
        mtbfValue="no"
      }
      let data = {
        dnafileName: this.dnafileName,
        sapfileName: this.sapfileName,
        analyisisName: this.analyisisName,
        customerNames: this.customerNames,
        analysisType: this.analysisType,
        replensihTime: this.replensihTime,
        date: new Date(),
        dnafile: this.dnafile,
        sapfile: this.sapfile,
        bomfile:this.bomFile,
        mtbf:mtbfValue
      };
      var filePresent=false;
      if (
        this.analyisisName !== "" &&
        this.customerNames !== "" &&
        this.analysisType !== "" &&
        this.replensihTime !== ""
      ) {
        if(this.fileType === "dna")
        {
          if(this.dnafile !== "")
          {
            filePresent=true
          }else
          {
            swal({
              title: "Error",
              text: "Please Attach the DNA File",
              icon: "error"
            });
          }
        }else
        {
           if(this.bomFile !== "")
          {
            filePresent=true
          }else
          {
          swal({
            title: "Error",
            text: "Please Attach the BOM File",
            icon: "error"
            });
          }
        }

        if(filePresent)
        {
          if (this.sapfile !== "") {
            this.diasableFlag = true;
            this.uploading = true;
            this.diasableFlag = true;
            if (this.resubmit) {
              swal({
                title: "Info",
                text: "Are you sure want to Resubmit the Request ?",
                icon: "info"
              }).then(ok => {
                if (ok) {
                  this.resubmit = false;
                  this.post_spare_part_analysis(data);
                }
              });
            } else {
              this.post_spare_part_analysis(data);
            }
          } else {
            swal({
              title: "Error",
              text: "Please Attach the SAP File",
              icon: "error"
            });
          }
        }
      } else {
        swal({
          title: "Error",
          text: "Please Fill the Form",
          icon: "error"
        });
      }
    },

    // API calls
    get_spare_part_analysis() {
      fetch(constant.APIURL + "api/v1/get_spare_part_analysis", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data ---->", data);
            if (data.code === "token_expired") {
              this.logout();
            }
            this.partsAnalysis = data;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    redirectToSummary() {
      console.log("inside summary");
      router.push({
        path: "/parts/analysis",
        query: { id: this.requestId }
      });
    },
    post_spare_part_analysis(data) {
      let formData = new FormData();
      console.log("loader show");

      this.loaderFlag = true;
      formData.append("analysis_name", data.analyisisName);
      formData.append("analysis_type", data.analysisType);
      formData.append("replenish_time", data.replensihTime);

      formData.append("user_email_id", localStorage.getItem("email_id"));
      formData.append("customer_name", data.customerNames);
      formData.append("sap_export_file", data.sapfile);
      formData.append("is_mtbf",data.mtbf)
      if(this.fileType ==="dna")
      {
        formData.append("customer_dna_file", data.dnafile);
      }else{
        formData.append("bom_file", data.bomfile);
      }
      console.log("formdata ----->", formData.get("analysis_name"));
      fetch(constant.APIURL + "api/v1/post_spare_part_analysis", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code === 200) {
              this.routeToView(data);
            } else {
              swal("Hello world!");
              this.uploading = false;
              this.resubmit = true;
              this.diasableFlag = false;

              swal({
                title: "Error",
                text: data.msg,
                icon: "error",
                buttons:{
                  download :{
                    text:"Download Sample",
                    value:"yes"
                    },
                    ok : true
                      },
                      })
                  .then((value) => {
                    switch (value) {
                    case "yes":
                    this.downloadSampleBOM();
                    }
              });
              this.loaderFlag = false;
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    }
  }
};
</script>
<style>
.file {
  cursor: pointer;
}
.nav-custom {
  padding-top: 20px rem !important;
}
.dot {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
.dot-green {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: green;
  border-radius: 50%;
  display: inline-block;
}
.line {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: #bbb;
  display: inline-block;
}
.line-green {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: green;
  display: inline-block;
}
.line-red {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: red;
  display: inline-block;
}
.dot-red {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: red;
  border-radius: 50%;
  display: inline-block;
}
.in-progress {
  cursor: pointer;
  font-size: 14px;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.form_wizard .stepContainer {
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
}
.overlay {
  background-color: #efefef;
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 1000;
  top: 0px;
  left: 0px;
  opacity: 0.5; /* in FireFox */
  filter: alpha(opacity=50); /* in IE */
}
</style>
