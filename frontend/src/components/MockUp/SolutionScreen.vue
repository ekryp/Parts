<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4 v-if="releaseFlag">Release Notes</h4>
        <h4 v-if="patchFlag">Patches</h4>
      </div>
      <div class="content">
        <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
        <br>
        <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
      </div>
      <div class="actions">
        <button type="button" class="btn btn-danger" @click="hideModal()">OK</button>
      </div>
    </vudal>

    <div class="custom-container" style="paddingTop: 5%">
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
                placeholder="Enter the Problem Description"
              ></textarea>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">{{solutionScreenConstants.logInfo}}</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <textarea class="form-control" col="4" id="email" placeholder="Enter the Log-Info"></textarea>
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
                    <input type="file" @change="handleFile" id="fileupload" style="display:none">
                    <i class="fas fa-paperclip fa-1.5x in-progress"></i>
                  </label>
                </div>
                <div class="col-lg-8">
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
                @click="onAnalyze()"
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
            <div class="col-md-4">
              <button type="button" class="btn btn-success" @click="onReserve()">{{solutionScreenConstants.buttons[1]}}</button>
            </div>
          </div>

          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-12">
              <h5 align="center">{{solutionScreenConstants.potentialSolutionHeader}}</h5>
            </div>
          </div>
          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution1()"
                      v-bind:style="{ backgroundColor: b1color }"
                    >Matching Defects</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b1color }">76%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution2()"
                      v-bind:style="{ backgroundColor: b2color }"
                    >FSB Tech Notes</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b2color }">65%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution3()"
                      v-bind:style="{ backgroundColor: b3color }"
                    >Wiki Links</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b3color }">45%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution4()"
                      v-bind:style="{ backgroundColor: b4color }"
                    >Configurations</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b4color }">45%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress col"
                      @click="showSolution5()"
                      v-bind:style="{ backgroundColor: b5color }"
                    >TOI Area</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b5color }">44%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="row align">
            <div class="col-md-12">
              <h5 align="center" v-if="problem1Flag || problem2Flag ">Solution Links</h5>
            </div>
          </div>

          <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
              <h5 align="left" v-if="problem1Flag">Patches</h5>
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
                    >Patch 1</td>
                    <td class="col in-progress" v-bind:style="{ backgroundColor: p1color }">97%</td>
                  </tr>
                  <tr>
                    <td
                      class="col in-progress"
                      @click="showPatchModal()"
                      v-bind:style="{ backgroundColor: p2color }"
                    >Patch 2</td>
                    <td class="col in-progress" v-bind:style="{ backgroundColor: p2color }">92%</td>
                  </tr>
                  <!-- <tr>
                    <td class="col">Upgraded firmware</td>
                    <td class="col">45%</td>
                  </tr>-->
                </tbody>
              </table>
            </div>
          </div>

          <div class="row">
            <div class="col-md-1"></div>
            <div class="col-md-10">
              <h5 align="left" v-if="problem2Flag">Release Notes</h5>
            </div>
          </div>

          <div class="row align" v-if="problem2Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive table-hover">
                <tbody>
                  <tr>
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
                  </tr>
                  <!-- <tr>
                    <td class="col">Upgraded firmware</td>
                    <td class="col">83%</td>
                  </tr>-->
                </tbody>
              </table>
            </div>
          </div>

          <!--  <div class="row align" v-if="problem3Flag">
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

          <div class="row">
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
          </div>

          <div class="row align" v-if="problem1Flag || problem2Flag || problem3Flag">
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
          </div>-->
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

import DownloadExcel from "@/components/DownloadExcel/JsonExcel";
export default {
  name: "SolutionScreen",
  components: {
    SideNav,
    headernav,
    DownloadExcel,
    tagsinput,
    Vudal
  },
  created() {
    clearInterval(window.intervalObj);
  },
  data() {
    console.log("dashboard", this.data);
    return {
      tags: [],
      solutionScreenConstants:constant.SolutionScreen,
      showGreen: true,
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
      this.analyzeFlag = true;
    },
    showModal() {
      this.patchFlag = false;
      this.releaseFlag = true;
      this.$modals.myModal.$show();
    },
    showPatchModal() {
      this.patchFlag = true;
      this.releaseFlag = false;
      this.$modals.myModal.$show();
    },
    hideModal() {
      this.$modals.myModal.$hide();
    },
    showSolution1() {
      this.problem1Flag = true;
      this.problem2Flag = false;
      this.problem3Flag = false;
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
      this.problem3Flag = true;
      this.problem2Flag = false;
      this.problem1Flag = false;
      this.b3color = "#88e288";
      this.b1color = "";
      this.b2color = "";
      this.b4color = "";
      this.b5color = "";
    },
    showSolution4() {
      this.problem3Flag = true;
      this.problem2Flag = false;
      this.problem1Flag = false;
      this.b3color = "";
      this.b2color = "";
      this.b4color = "#88e288";
      this.b5color = "";
      this.b1color = "";
    },
    showSolution5() {
      this.problem3Flag = true;
      this.problem2Flag = false;
      this.problem1Flag = false;
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
</style>

