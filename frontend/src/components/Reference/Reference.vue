<template>
  <div>
    <headernav msg="Reference"/>
    <side-nav menu="refernce"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div class="myBreadCrumb" style="margin-bottom:1px">
        <p>
          <span style="font-size: 14px;">Reference</span>
        </p>
      </div>
      <div class>
        <h5>Reference File Information :</h5>
        <div class="form-group">
          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Part File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="fileupload" class="file">
                    <input
                      type="file"
                      @change="partsFileEvent"
                      id="fileupload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{partsFileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer">
              <DownloadExcel :data="partsAnalysisRequestList" type="csv" name="Sample_Parts.csv"  >
 
                <div class="float-left" style="marginTop:1%">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%">
                  <span>Download Sample_Parts.csv</span>
                </div>
              </DownloadExcel>
            </div>
            <div class="col-lg-2">
              <button type="button" class="btn btn-success" @click="uploadPartsData()">Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('parts')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">High Spare File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="highSpareUpload" class="file">
                    <input
                      type="file"
                      @change="highSpareFileEvent"
                      id="highSpareUpload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{highSpareFileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer">
             
                <DownloadExcel :data="highSpareFilesList" type="csv" name="Sample_High_Spare.csv"  >
                <div class="float-left" style="marginTop:1%">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%">
                  <span>Download Sample_High_Spare.csv</span>
                </div>
                </DownloadExcel>
            </div>
            <div class="col-lg-2">
              <button type="button" class="btn btn-success" @click="uploadHighSpareData()">Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('highspare')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Node File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="nodeUpload" class="file">
                    <input type="file" @change="nodeFileEvent" id="nodeUpload" style="display:none">
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{nodeFileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer">
              <DownloadExcel :data="nodeFilesList" type="csv" name="Sample_Node.csv"  >
                <div class="float-left" style="marginTop:1%">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%">
                  <span>Download Sample_Node.csv</span>
                </div>
              </DownloadExcel>
            </div>
            <div class="col-lg-2">
              <button type="button" class="btn btn-success" @click="uploadNodeData()">Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('node')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Depot File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="depotUpload" class="file">
                    <input
                      type="file"
                      @change="depotFileEvent"
                      id="depotUpload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{depotFileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer">
              <DownloadExcel :data="depotFilesList" type="csv" name="Sample_Depot.csv"  >
                <div class="float-left" style="marginTop:1%">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%">
                  <span>Download Sample_Depot.csv</span>
                </div>
              </DownloadExcel>
            </div>
            <div class="col-lg-2">
              <button type="button" class="btn btn-success" @click="uploadDepotData()">Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('depot')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Minsomer File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="minsomerUpload" class="file">
                    <input
                      type="file"
                      @change="minsomerFileEvent"
                      id="minsomerUpload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{minsomerFileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer">
               <DownloadExcel :data="minsomerFilesList" type="csv" name="Sample_Minsomer.csv"  >
                 <div class="float-left" style="marginTop:1%">
                  <i class="fa fa-download" aria-hidden="true"></i>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%">
                  <span>Download Sample_Minsomer.csv</span>
                </div>
               </DownloadExcel>
            </div>
            <div class="col-lg-2">
              <button type="button" class="btn btn-success" @click="uploadMinsomerData()">Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('misnomer')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Ratio of PON - 2Day File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="ratio2Upload" class="file">
                    <input
                      type="file"
                      @change="ratio2FileEvent"
                      id="ratio2Upload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{ratio2FileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer" @click="downloadRatio2CSV()">
              <!-- <download-excel :data="ratioFilesList" type="csv" name="Sample_Ratio.csv"> -->
              <div class="float-left" style="marginTop:1%">
                <i class="fa fa-download" aria-hidden="true"></i>
              </div>
              <div style="paddingLeft:7%;paddingTop:1%">
                <span>Download Sample_Ratio_2Day.csv</span>
              </div>
              <!-- </download-excel>   -->
            </div>
            <div class="col-lg-2">
              <button
                type="button"
                class="btn btn-success"
                @click="uploadRatioData('Ratio of PON - 2Day')"
              >Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('Ratio of PON - 2Day')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Ratio of PON - 7Day File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="ratio7Upload" class="file">
                    <input
                      type="file"
                      @change="ratio7FileEvent"
                      id="ratio7Upload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{ratio7FileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer" @click="downloadRatio7CSV()">
              <!-- <download-excel :data="ratioFilesList" type="csv" name="Sample_Ratio.csv"> -->
              <div class="float-left" style="marginTop:1%">
                <i class="fa fa-download" aria-hidden="true"></i>
              </div>
              <div style="paddingLeft:7%;paddingTop:1%">
                <span>Download Sample_Ratio_7Day.csv</span>
              </div>
              <!-- </download-excel>   -->
            </div>
            <div class="col-lg-2">
              <button
                type="button"
                class="btn btn-success"
                @click="uploadRatioData('Ratio of PON - 7Day')"
              >Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('Ratio of PON - 7Day')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Ratio of PON - 30Day File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="ratio30Upload" class="file">
                    <input
                      type="file"
                      @change="ratio30FileEvent"
                      id="ratio30Upload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{ratio30FileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer" @click="downloadRatio30CSV()">
              <!-- <download-excel :data="ratioFilesList" type="csv" name="Sample_Ratio.csv"> -->
              <div class="float-left" style="marginTop:1%">
                <i class="fa fa-download" aria-hidden="true"></i>
              </div>
              <div style="paddingLeft:7%;paddingTop:1%">
                <span>Download Sample_Ratio_30Day.csv</span>
              </div>
              <!-- </download-excel>   -->
            </div>
            <div class="col-lg-2">
              <button
                type="button"
                class="btn btn-success"
                @click="uploadRatioData('Ratio of PON - 30Day')"
              >Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('Ratio of PON - 30Day')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>

          <div class="row" style="marginTop:2%;font-size:17px">
            <div class="col-lg-3">
              <label style="font-size:17px">Ratio of PON - 60Day File</label>
            </div>
            <div class="col-lg-4">
              <div class="row">
                <div class="col-lg-1">
                  <label for="ratio60Upload" class="file">
                    <input
                      type="file"
                      @change="ratio60FileEvent"
                      id="ratio60Upload"
                      style="display:none"
                    >
                    <i style="cursor:pointer" class="fas fa-paperclip fa-2x"></i>
                  </label>
                </div>
                <div style="paddingLeft:7%;paddingTop:1%" class="col-lg-4">
                  <span>{{ratio60FileName}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-3" style="cursor:pointer" @click="downloadRatio60CSV()">
              <!-- <download-excel :data="ratioFilesList" type="csv" name="Sample_Ratio.csv"> -->
              <div class="float-left" style="marginTop:1%">
                <i class="fa fa-download" aria-hidden="true"></i>
              </div>
              <div style="paddingLeft:7%;paddingTop:1%">
                <span>Download Sample_Ratio_60Day.csv</span>
              </div>
              <!-- </download-excel>   -->
            </div>
            <div class="col-lg-2">
              <button
                type="button"
                class="btn btn-success"
                @click="uploadRatioData('Ratio of PON - 60Day')"
              >Save</button>
              <button
                type="button"
                class="btn btn-success"
                @click="routeToView('Ratio of PON - 60Day')"
                style="margin-left:10%"
              >View</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";
import * as partsData from "../../utilies/sampleparts.json";
import * as highSpareData from "../../utilies/samplehighspare.json";
import * as nodeData from "../../utilies/samplenode.json";
import * as minsomerData from "../../utilies/sampleminsomer.json";
import * as depotData from "../../utilies/sampledepot.json";
import * as ratio2Data from "../../utilies/sampleratio2Day.txt";
import * as ratio7Data from "../../utilies/sampleratio7Day.txt";
import * as ratio30Data from "../../utilies/sampleratio30Day.txt";
import * as ratio60Data from "../../utilies/sampleratio60Day.txt";
import DownloadExcel from "@/components/DownloadExcel/JsonExcel";

import swal from "sweetalert";

export default {
  name: "Reference",
  components: {
    SideNav,
    headernav,
    DownloadExcel
  },
  created() {},
  data() {
    console.log("home");
    return {
      partsFile: "",
      partsFileName: "no file chosen",
      email_id: "khali.saran@ekryp.com",
      partsAnalysisRequestList: partsData,
      highSpareFile: "",
      highSpareFileName: "no file chosen",
      highSpareFilesList: highSpareData,
      nodeFile: "",
      nodeFileName: "no file chosen",
      nodeFilesList: nodeData,
      minsomerFile: "",
      minsomerFileName: "no file chosen",
      minsomerFilesList: minsomerData,
      depotFile: "",
      depotFileName: "no file chosen",
      depotFilesList: depotData,
      ratio2File: "",
      ratio2FileName: "no file chosen",
      ratio2FilesList: ratio2Data,
      ratio7File: "",
      ratio7FileName: "no file chosen",
      ratio7FilesList: ratio7Data,
      ratio30File: "",
      ratio30FileName: "no file chosen",
      ratio30FilesList: ratio30Data,
      ratio60File: "",
      ratio60FilesList: ratio60Data,
      ratio60FileName: "no file chosen"
    };
  },
  methods: {
    partsFileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.partsFile = file;
        this.partsFileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    highSpareFileEvent(e) {
      console.log("hi");
      console.log("image ----highspare->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.highSpareFile = file;
        this.highSpareFileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    depotFileEvent(e) {
      console.log("hi");
      console.log("image ----depot->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.depotFile = file;
        this.depotFileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    nodeFileEvent(e) {
      console.log("hi");
      console.log("image ----highspare->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.nodeFile = file;
        this.nodeFileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    minsomerFileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.minsomerFile = file;
        this.minsomerFileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    ratio2FileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.ratio2File = file;
        this.ratio2FileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    ratio7FileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.ratio7File = file;
        this.ratio7FileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    ratio30FileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.ratio30File = file;
        this.ratio30FileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    ratio60FileEvent(e) {
      console.log("hi");
      console.log("image ----parts->", e.target.files);
      const file = e.target.files[0];
      if (file.name.endsWith("csv") || file.name.endsWith("CSV")) {
        console.log(file.name);
        this.ratio60File = file;
        this.ratio60FileName = file.name;
      } else {
        swal({
          title: "Error",
          text: "Upload a .csv File",
          icon: "error"
        });
      }
    },
    uploadPartsData() {
      console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      let data = {
        partsFile: this.partsFile,
        email_id: this.email_id
      };

      if (this.partsFile !== "") {
        this.post_parts_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your Parts File",
          icon: "info"
        });
      }
    },
    post_parts_data(data) {
      let formData = new FormData();
      formData.append("parts_file", data.partsFile);
      formData.append("user_email_id", data.email_id);
      console.log("inside the da");
      fetch(constant.APIURL+"api/v1/post_parts", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "Parts File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    uploadHighSpareData() {
      //console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      let data = {
        highSpareFile: this.highSpareFile,
        email_id: this.email_id
      };

      if (this.highSpareFile !== "") {
        this.post_high_spare_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your High Spare File",
          icon: "info"
        });
      }
    },
    post_high_spare_data(data) {
      let formData = new FormData();
      formData.append("high_spare_file", data.highSpareFile);
      formData.append("user_email_id", data.email_id);
      fetch(constant.APIURL+"api/v1/post_high_spare", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "High Spare File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    uploadNodeData() {
      //console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      let data = {
        nodeFile: this.nodeFile,
        email_id: this.email_id
      };

      if (this.nodeFile !== "") {
        this.post_node_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your Node File",
          icon: "info"
        });
      }
    },
    post_node_data(data) {
      let formData = new FormData();
      formData.append("node_file", data.nodeFile);
      formData.append("user_email_id", data.email_id);
      fetch(constant.APIURL+"api/v1/post_node", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "Node File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    uploadMinsomerData() {
      //console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      let data = {
        minsomerFile: this.minsomerFile,
        email_id: this.email_id
      };

      if (this.minsomerFile !== "") {
        this.post_minsomer_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your Minsomer File",
          icon: "info"
        });
      }
    },
    post_minsomer_data(data) {
      let formData = new FormData();
      formData.append("misnomer_file", data.minsomerFile);
      formData.append("user_email_id", data.email_id);
      fetch(constant.APIURL+"api/v1/post_misnomer", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "Minsomer File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    uploadDepotData() {
      //console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      let data = {
        depotFile: this.depotFile,
        email_id: this.email_id
      };

      if (this.depotFile !== "") {
        this.post_depot_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your Depot File",
          icon: "info"
        });
      }
    },
    post_depot_data(data) {
      let formData = new FormData();
      formData.append("depot_file", data.depotFile);
      formData.append("user_email_id", data.email_id);
      fetch(constant.APIURL+"api/v1/post_depot", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            console.log("Response from backend data ---->", data);
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "Minsomer File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    uploadRatioData(analysis_type) {
      //console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      console.log(analysis_type);
      let data;
      if (analysis_type === "Ratio of PON - 2Day") {
        data = {
          ratio_file: this.ratio2File,
          email_id: this.email_id,
          analysis_type: analysis_type
        };
      }
      if (analysis_type === "Ratio of PON - 7Day") {
        data = {
          ratio_file: this.ratio7File,
          email_id: this.email_id,
          analysis_type: analysis_type
        };
      }
      if (analysis_type === "Ratio of PON - 30Day") {
        data = {
          ratio_file: this.ratio30File,
          email_id: this.email_id,
          analysis_type: analysis_type
        };
      }
      if (analysis_type === "Ratio of PON - 60Day") {
        data = {
          ratio_file: this.ratio60File,
          email_id: this.email_id,
          analysis_type: analysis_type
        };
      }
      if (data.ratio_file !== "") {
        this.post_ratio_data(data);
      } else {
        swal({
          title: "Info",
          text: "Please add your ratio File",
          icon: "info"
        });
      }
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    post_ratio_data(data) {
      let formData = new FormData();
      formData.append("ratio_file", data.ratio_file);
      formData.append("user_email_id", data.email_id);
      formData.append("analysis_type", data.analysis_type);
      console.log(data.ratio_file);
      fetch(constant.APIURL+"api/v1/post_ratio", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("Response from backend data ---->", data);
            if(data.code === "token_expired")
            {
              this.logout();
            }
            if (data.http_status_code == 200) {
              swal({
                title: "Success",
                text: "Ratio File Uploaded Successfully",
                icon: "success"
              });
            } else if (data.http_status_code == 400) {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    downloadRatio2CSV() {
      var fileContent = String(this.ratio2FilesList);
      var fileType = "csv";

      fileType = fileType || "csv";
      var blobType = "text/csv";
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(
        new Blob([fileContent], { type: blobType })
      );
      a.download = "SampleRatio2Day" + "." + fileType;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
    },
    downloadRatio60CSV() {
      var fileContent = String(this.ratio60FilesList);
      var fileType = "csv";

      fileType = fileType || "csv";
      var blobType = "text/csv";
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(
        new Blob([fileContent], { type: blobType })
      );
      a.download = "SampleRatio60Day" + "." + fileType;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
    },
    downloadRatio7CSV() {
      var fileContent = String(this.ratio7FilesList);
      var fileType = "csv";

      fileType = fileType || "csv";
      var blobType = "text/csv";
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(
        new Blob([fileContent], { type: blobType })
      );
      a.download = "SampleRatio7Day" + "." + fileType;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
    },
    downloadRatio30CSV() {
      var fileContent = String(this.ratio30FilesList);
      var fileType = "csv";

      fileType = fileType || "csv";
      var blobType = "text/csv";
      var a = document.createElement("a");
      a.href = window.URL.createObjectURL(
        new Blob([fileContent], { type: blobType })
      );
      a.download = "SampleRatio30Day" + "." + fileType;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
    },
    routeToView(fileType) {
      router.push({
        path: "/reference/view",
        query: { fileType: fileType }
      });
    }
  }
};
</script>
<style>
.main {
  height: 100vh;
  background-color: #293f55;
}
.content {
  padding-top: 20%;
  text-align: center;
  vertical-align: middle;
}
</style>
