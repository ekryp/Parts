<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>




    <Loading :active="isLoading" 
        :can-cancel="false" 
        color=#15ba9a
        :is-full-page="fullPage"></Loading>


    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4 v-if="releaseFlag">Release Notes</h4>
        <h4 v-if="patchFlag">Patches</h4>
      </div>
      <div class="content modal-content1">
        <span class="textOverlay">{{descriptionContent}}</span>
      </div>
      <div class="actions">
        <button type="button" class="btn btn-danger" @click="hideModal()">OK</button>
      </div>
    </vudal>

    <div class="custom-container" style="paddingTop: 7%">
      <div class="myBreadCrumb" style="margin-bottom:1px;fontSize:0.875em">
        <p>
          <span class="in-progress">{{solutionScreenConstants.breadcrumb}}</span>
        </p>
      </div>
      <div class="row">
        <div class="col-md-5 align-margin bg-white align">
          <div class="row align">
            <label class="col-md-10">{{solutionScreenConstants.problemDescriptionName}}</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <textarea
                v-model="problemDescription"
                class="form-control"
                rows="4"
                id="email"
                :placeholder="problemDescriptionPlaceholder"
              ></textarea>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">{{solutionScreenConstants.logInfo}}</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <textarea class="form-control" col="4" id="email" placeholder="Enter the Log-Info" disabled></textarea>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">{{solutionScreenConstants.tags}}</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <tagsinput
                class="tags form-control"
                style="color: #495057"
                :tags="tags"
                placeholder="Add Tags"
                @tags-change="handleChange"
              ></tagsinput>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">{{solutionScreenConstants.tarBall}}</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <div class="row">
                <div class="col-lg-1">
                  <label for="fileupload" class="file">
                    <!-- <input type="file" @change="handleFile" id="fileupload" style="display:none"> -->
                    <i class="fas fa-paperclip fa-1.5x in-progress"></i>
                  </label>
                </div>
                <div class="col-lg-8 in-progress">
                  <span v-if="tarFileName === ''">no file selected</span>
                  <span v-if="tarFileName !== ''">{{tarFileName}}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="row align float-right">
            <div class="col-md-10">
              <button
                v-if="problemDescription !== ''"
                type="button"
                class="btn btn-success"
                @click="onAnalyze()"
              >{{solutionScreenConstants.buttons[0]}}</button>
              <button
                v-if="problemDescription === ''"
                type="button"
                class="btn btn-success"
                disabled
              >{{solutionScreenConstants.buttons[0]}}</button>
            </div>
          </div>
        </div>

        <div class="col-md-5 bg-white align-margin">
          <div class="row align">
            <div class="col-md-2"></div>
            <div class="col-md-4">
              <label>{{solutionScreenConstants.labAvailablity}}</label>
            </div>
            <div class="col-md-2" align="left">
              <i class="fas fa-dot-circle" style="color:green" v-if="showGreen"></i>
              <i class="fas fa-dot-circle" style="color:#d62828f7" v-if="!showGreen"></i>
            </div>
            <div class="col-md-4" v-if="analyzeFlag">
              <button type="button" class="btn btn-success" @click="onReserve()">{{solutionScreenConstants.buttons[1]}}</button>
            </div>
          </div>

          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-12">
              <h5 align="center">{{solutionScreenConstants.potentialSolutionHeader}}</h5>
            </div>
          </div>

          
           <div class="row align" v-if="errorFlag">
            <div class="col-md-12">
              <h5 align="center">{{solutionScreenConstants.errorMessage}}</h5>
            </div>
          </div>
          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <!-- <tr v-for="item in devTrackData" :key="item.ids"
                  class="in-progress col"
                  
                  @click="showSolution(item.index)"
                  >
                      <td>{{item.ids}}</td>
                      
                    </tr> -->
                  
                  
                   <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution2()"
                      v-bind:style="{ backgroundColor: b2color }"
                    >Dev Track Data</td>
                    <!-- <td @click="showSolution()" v-bind:style="{ backgroundColor: b2color }">76%</td> -->
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution1()"
                      v-bind:style="{ backgroundColor: b1color }"
                    >FSB Tech Notes</td>
                    <!-- <td @click="showSolution()" v-bind:style="{ backgroundColor: b1color }">65%</td> -->
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution3()"
                      v-bind:style="{ backgroundColor: b3color }"
                    >Wiki Links</td>
                    <!-- <td @click="showSolution()" v-bind:style="{ backgroundColor: b3color }">45%</td> -->
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution4()"
                      v-bind:style="{ backgroundColor: b4color }"
                    >Configurations</td>
                    <!-- <td @click="showSolution()" v-bind:style="{ backgroundColor: b4color }">45%</td> -->
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution5()"
                      v-bind:style="{ backgroundColor: b5color }"
                    >TOI Area</td>
                    <!-- <td @click="showSolution()" v-bind:style="{ backgroundColor: b5color }">44%</td> -->
                  </tr> 
                </tbody>
              </table>
            </div>
            
          </div>

          <div class="row align" v-if="problem1Flag">
            <div class="col-md-12">
              <h5 align="center" v-if="problem1Flag || problem2Flag ">Solution Links</h5>
            </div>
          </div>

          <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
              <h5 align="left" v-if="problem1Flag">Description</h5>
            </div>
          </div> 

          <div class="row align" v-if="problem1Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive table-hover">
                <tbody>
                  <tr>
                    <td
                      @click="showPatchModal()"
                      v-bind:style="{ backgroundColor: p1color }"
                      class="col in-progress"
                    >Description</td>
                    
                  </tr>
                  <tr>
                    <td
                      class="col in-progress"
                      @click="showPatchModal()"
                      v-bind:style="{ backgroundColor: p2color }"
                    >Patch 2</td>
                    <td class="col in-progress" v-bind:style="{ backgroundColor: p2color }">92%</td>
                  </tr>
                   <tr>
                    <td class="col">Upgraded firmware</td>
                    <td class="col">45%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
              <h5 align="left" v-if="problem2Flag">Dev Track</h5>
            </div>
          </div>

          <div class="row align" v-if="problem2Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive table-hover">
                <thead>
                  <th>Issue Id</th>
                  <th>Severity</th>
                </thead>
                <tbody>
                  <tr v-for="item in devTrackData" :key="item.ids"
                  
                  
                  @click="showPatchModal(item.index)"
                  >
                  <td class=" in-progress">
                    {{item.ids}}</td>
                      <td class=" in-progress">{{item.severity}}</td>
                    </tr>
                  <!-- <tr>
                    <td
                      class="col in-progress"
                      @click="showModal()"
                      v-bind:style="{ backgroundColor: rl1color }"
                    >Release Notes 1</td>
                    <td class="col" v-bind:style="{ backgroundColor: rl1color }">81%</td>
                  </tr>
                  <tr>
                    <td
                      class="col in-progress"
                      @click="showModal()"
                      v-bind:style="{ backgroundColor: rl2color }"
                    >Release Notes 2</td>
                    <td class="col" v-bind:style="{ backgroundColor: rl2color }">82%</td>
                  </tr> -->
                   
                </tbody>
              </table>
            </div>
          </div>

           <div class="row align" v-if="problem3Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <tr>
                    <td class="col">Replace part</td>
                    <td class="col">71%</td>
                  </tr>
                  <tr>
                    <td class="col">Reseated part</td>
                    <td class="col">72%</td>
                  </tr>
                  <tr>
                    <td class="col">Upgraded firmware</td>
                    <td class="col">73%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- <div class="row">
            <div class="col-md-12">
              <h5 align="center" v-if="problem1Flag || problem2Flag || problem3Flag">Release Notes</h5>
            </div>
          </div>

          <div class="row" v-if="problem1Flag || problem2Flag || problem3Flag">
            <div class="col-md-12">
              <div class="row">
                <div class="col" style="text-align: center">
                  <button type="button" class="btn btn-info" @click="showModal()">Release Notes 1</button>
                </div>
                <div class="col" style="text-align: center">
                  <button type="button" class="btn btn-info" @click="showModal()">Release Notes 2</button>
                </div>
              </div>
            </div>
          </div> -->

          <!-- <div class="row align" v-if="problem1Flag || problem2Flag || problem3Flag">
            <div class="col-md-12">
              <h5 align="center">Patches</h5>
            </div>
          </div>

          <div class="row" v-if="problem1Flag || problem2Flag || problem3Flag">
            <div class="col-md-12">
              <div class="row">
                <div class="col" style="text-align: center">
                  <button type="button" class="btn btn-info" @click="showPatchModal()">Patch 1</button>
                </div>
                <div class="col" style="text-align: center">
                  <button type="button" class="btn btn-info" @click="showPatchModal()">Patch 2</button>
                </div>
                <div class="col" style="text-align: center">
                  <button type="button" class="btn btn-info" @click="showPatchModal()">Patch 3</button>
                </div>
              </div>
            </div>
          </div> -->
          <br>
        </div>
      </div>
      
    </div>
    <div>
        <!-- Footer -->
        <footer class="footer  font-small blue">
          <!-- Copyright -->
          <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
          <!-- Copyright -->
        </footer>
        <!-- Footer -->
      </div>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";

import * as constant from "../constant/constant";
import tagsinput from "vue-tagsinput";
import Vudal from "vudal";
import Loading from 'vue-loading-overlay';

import DownloadExcel from "@/components/DownloadExcel/JsonExcel";
export default {
  name: "SolutionScreen",
  components: {
    SideNav,
    headernav,
    DownloadExcel,
    tagsinput,
    Vudal,
    Loading
  },
  created() {
    clearInterval(window.intervalObj);
  },
  data() {
    console.log("dashboard", this.data);
    return {
      isLoading: false,
      tags: [],
      solutionScreenConstants:constant.SolutionScreen,
      showGreen: true,
      devTrackData:[],
      errorFlag:false,
      tarFileName: "",
      tarFile: "",
      b1color: "",
      b2color: "",
      b3color: "",
      b4color: "",
      b5color: "",
      p1color: "",
      p2color: "",
      rl1color: "",
      rl2color: "",
      descriptionContent:"",
      problemDescriptionPlaceholder:"Enter the Problem Description",
      valueIndex:"",
      releaseFlag: true,
      patchFlag: false,
      problemDescription: "",
      analyzeFlag: false,
      problem1Flag: false,
      problem2Flag: false,
      problem3Flag: false
    };
  },
  methods: {
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
        this.tarFileName = file.name;
        this.tarFile = file;
      } else {
        alert("error");
      }
    },
    onReserve() {
      console.log(this.showGreen);
      if (this.showGreen) {
        this.showGreen = false;
      } else {
        this.showGreen = true;
      }
    },
    onAnalyze() {
      this.isLoading=true;
      this.errorFlag=false;
      this.devTrackData=[];
     
      fetch("http://localhost:5002/api/getDevTrackData?search_param="+this.problemDescription, {
      
      headers: {
        'Content-Type': 'application/json'
      }
       })
         .then(response => {
           response.text().then(text => {
             const data = text && JSON.parse(text);
             if (data.http_status_code === 200) {
              this.isLoading=false;
             
              for(var i=0;i<data.data.devTrack.length;i++)
              {
                if(i<5){
                  this.devTrackData.push({ids:data.data.devTrack[i].id,index:i,
                description:data.data.devTrack[i].description,
                severity:data.data.devTrack[i].severity});
                }
                
              }
              console.log('asdasd',this.devTrackData);
              if(data.data.devTrack.length>0)
              {
                 this.analyzeFlag = true;
              }
              else{
                this.analyzeFlag = false;
                this.problem2Flag = false;
                this.errorFlag=true;
                this.problemDescriptionPlaceholder="Sorry ...No Data is Present for the Specified Issue";
                this.problemDescription="";
              }
               
             } else {
                this.isLoading=false;
             }
             console.log("data -- response-->", data);
             
           });
         })
         .catch(handleError => {
           console.log(" Error Response ------->", handleError);
         });
    },
    showModal() {
      this.patchFlag = false;
      this.releaseFlag = true;
      this.$modals.myModal.$show();
    },
    showPatchModal(index) {
      this.patchFlag = true;
      this.descriptionContent=this.devTrackData[index].description;
      this.releaseFlag = false;
      this.$modals.myModal.$show();
    },
    hideModal() {
      this.$modals.myModal.$hide();
    },
    showSolution(index) {
      console.log(index);
      this.valueIndex=index;
      this.problem1Flag = true;
      this.problem2Flag = false;
      this.problem3Flag = false;
      this.b1color = "#88e288";
      this.b2color = "";
      this.b3color = "";
      this.b4color = "";
      this.b5color = "";
    },
    showSolution1() {
      // this.problem1Flag = true;
       this.problem2Flag = false;
      // this.problem3Flag = false;
      this.b1color = "#88e288";
      this.b2color = "";
      this.b3color = "";
      this.b4color = "";
      this.b5color = "";
    },
    showSolution2() {
      this.problem1Flag = false;
      this.problem2Flag = true;
      this.problem3Flag = false;
      this.b2color = "#88e288";
      this.b1color = "";
      this.b3color = "";
      this.b4color = "";
      this.b5color = "";
    },
    showSolution3() {
      // this.problem3Flag = true;
       this.problem2Flag = false;
      // this.problem1Flag = false;
      this.b3color = "#88e288";
      this.b1color = "";
      this.b2color = "";
      this.b4color = "";
      this.b5color = "";
    },
    showSolution4() {
      // this.problem3Flag = true;
       this.problem2Flag = false;
      // this.problem1Flag = false;
      this.b3color = "";
      this.b2color = "";
      this.b4color = "#88e288";
      this.b5color = "";
      this.b1color = "";
    },
    showSolution5() {
      // this.problem3Flag = true;
       this.problem2Flag = false;
      // this.problem1Flag = false;
      this.b3color = "";
      this.b2color = "";
      this.b1color = "";
      this.b4color = "";
      this.b5color = "#88e288";
    },
    ChangeColour(id) {
      if (id === "1") {
        this.p1color = "#88e288";
        this.p2color = "";
      } else if (id === "2") {
        this.p2color = "#88e288";
        this.p1color = "";
      }
    },
    hideColour(id) {
      this.p1color = "";
      this.p2color = "";
    },
    ChangeRlColour(id) {
      if (id === "1") {
        this.rl1color = "#88e288";
        this.rl2color = "";
      } else if (id === "2") {
        this.rl2color = "#88e288";
        this.rl1color = "";
      }
    },
    hideRlColour(id) {
      this.rl1color = "";
      this.rl2color = "";
    },
    handleChange(removeIndex, tag) {
      if (this.tags.length == removeIndex) {
        console.log(removeIndex);
        this.tags.push(tag);
      } else {
        this.tags.splice(removeIndex, 1);
      }
      console.log(removeIndex);
      console.log(tag);
    }
  }
};
</script>

<style>
.container {
  width: 100% !important;
  height: 100%;
}

/* For cursor Pointer Change to Hand Icon */

.align {
  padding: 0.75em;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.align-rl {
  padding-left: 8em;
}

.align-margin {
  margin-left: 3em;
  margin-right: 3em;
}
.tags {
  color: #495057 !important;
  font-size: 1rem !important;
  border: 1px solid #ced4da !important;
  border-radius: 0.25rem !important;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
}

::input-placeholder {
  opacity: 10;
  color: brown;
  font-weight: lighter;
}

.in-progress {
  cursor: pointer;
  
}
.vue-tooltip {
  background-color: white;
  color: #71869e;
}
.modal-content1{
  width: 80%;
}

.textOverlay
{
  word-break: break-all;
}
</style>

