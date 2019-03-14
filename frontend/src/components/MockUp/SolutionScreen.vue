<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 5%">
      <div class="myBreadCrumb" style="margin-bottom:1px;fontSize:0.875em">
        <p>
          <span class="in-progress">Solution</span>
        </p>
      </div>
      <div class="row">
        <div class="col-md-5 align-margin bg-white align">
          <div class="row align">
            <label class="col-md-10">Problem Description</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <textarea
                class="form-control"
                rows="4"
                id="email"
                placeholder="Enter the Problem Description"
              ></textarea>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">Log Info</label>
          </div>

          <div class="row align">
            <div class="col-md-10">
              <textarea class="form-control" col="4" id="email" placeholder="Enter the Log-Info"></textarea>
            </div>
          </div>

          <div class="row align">
            <label class="col-md-10">Tags</label>
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
            <label class="col-md-10">TAR Ball</label>
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
                type="button"
                class="btn btn-success"
                @click="onAnalyze()"
                v-tooltip.top.hover.focus="'Move to Reference Page'"
              >Analyze</button>
            </div>
          </div>
        </div>

        <div class="col-md-5 bg-white align-margin">
          <div class="row align">
            <div class="col-md-2"></div>
            <div class="col-md-4">
              <label>Lab Availablity</label>
            </div>
            <div class="col-md-2" align="left">
              <i class="fas fa-dot-circle" style="color:green" v-if="showGreen"></i>
              <i class="fas fa-dot-circle" style="color:#d62828f7" v-if="!showGreen"></i>
            </div>
            <div class="col-md-4">
              <button
                type="button"
                class="btn btn-success"
                @click="onReserve()"
                v-tooltip.top.hover.focus="'Move to Reference Page'"
              >Reserve</button>
            </div>
          </div>

          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-12">
              <h5 align="center">Potential Problem Areas</h5>
            </div>
          </div>
          <div class="row align" v-if="analyzeFlag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <tr>
                    <td
                      class="in-progress"
                      @click="showSolution1()"
                      v-bind:style="{ backgroundColor: b1color }"
                    >Electrical</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b1color }">76%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress"
                      @click="showSolution2()"
                      v-bind:style="{ backgroundColor: b2color }"
                    >Mechanical</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b2color }">65%</td>
                  </tr>
                  <tr>
                    <td
                      class="in-progress"
                      @click="showSolution3()"
                      v-bind:style="{ backgroundColor: b3color }"
                    >Software</td>
                    <td @click="showSolution()" v-bind:style="{ backgroundColor: b3color }">45%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="row align">
            <div class="col-md-12">
              <h5 align="center" v-if="problemFlag">Solution and Effectiveness</h5>
            </div>
          </div>
          <div class="row align" v-if="problem1Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <tr>
                    <td>Replace part</td>
                    <td>87%</td>
                  </tr>
                  <tr>
                    <td>Reseated part</td>
                    <td>82%</td>
                  </tr>
                  <tr>
                    <td>Upgraded firmware</td>
                    <td>45%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="row align" v-if="problem2Flag">
            <div class="col-md-1"></div>
            <div class="col-md-10" align="center">
              <table class="table responsive">
                <tbody>
                  <tr>
                    <td>Replace part</td>
                    <td>81%</td>
                  </tr>
                  <tr>
                    <td>Reseated part</td>
                    <td>82%</td>
                  </tr>
                  <tr>
                    <td>Upgraded firmware</td>
                    <td>83%</td>
                  </tr>
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
                    <td>Replace part</td>
                    <td>71%</td>
                  </tr>
                  <tr>
                    <td>Reseated part</td>
                    <td>72%</td>
                  </tr>
                  <tr>
                    <td>Upgraded firmware</td>
                    <td>73%</td>
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
                <div class="col" style="text-align: center">Release Notes 1</div>
                <div class="col" style="text-align: center">Release Notes 2</div>
                <div class="col" style="text-align: center">Release Notes 3</div>
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
                <div class="col" style="text-align: center">Patch 1</div>
                <div class="col" style="text-align: center">Patch 2</div>
                <div class="col" style="text-align: center">Patch 3</div>
              </div>
            </div>
          </div>
          <br>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";

import * as constant from "../constant/constant";
import tagsinput from "vue-tagsinput";

import DownloadExcel from "@/components/DownloadExcel/JsonExcel";
export default {
  name: "SolutionScreen",
  components: {
    SideNav,
    headernav,
    DownloadExcel,
    tagsinput
  },
  created() {
    clearInterval(window.intervalObj);
  },
  data() {
    console.log("dashboard", this.data);
    return {
      tags: [],
      showGreen: true,
      tarFileName: "",
      tarFile: "",
      b1color: "",
      b2color: "",
      b3color: "",
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
    showSolution1() {
      this.problem1Flag = true;
      this.problem2Flag = false;
      this.problem3Flag = false;
      this.b1color = "#88e288";
      this.b2color = "";
      this.b3color = "";
    },
    showSolution2() {
      this.problem1Flag = false;
      this.problem2Flag = true;
      this.problem3Flag = false;
      this.b2color = "#88e288";
      this.b1color = "";
      this.b3color = "";
    },
    showSolution3() {
      this.problem3Flag = true;
      this.problem2Flag = false;
      this.problem1Flag = false;
      this.b3color = "#88e288";
      this.b2color = "";
      this.b1color = "";
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

