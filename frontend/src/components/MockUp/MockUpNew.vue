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
      <div class="content contentwidth">
        <nav>
         <div class="nav nav-tabs" id="nav-tab" role="tablist">
          <a
            class="nav-item nav-link active navHeaderColor"
            id="nav-Details-tab"
            data-toggle="tab"
            href="#nav-Details"
            role="tab"
            aria-controls="nav-Details"
            aria-selected="true"
          >Details</a>
          <a
            class="nav-item nav-link navHeaderColor"
            id="nav-Description-tab"
            data-toggle="tab"
            href="#nav-Description"
            role="tab"
            aria-controls="nav-Description"
            aria-selected="true"
          >Description</a>

          
        </div>

      
      </nav>
        <div class="tab-content" id="nav-tabContent">

            <div
          class="tab-pane fade show"
          id="nav-Description"
          role="tabpanel"
          aria-labelledby="nav-Description-tab"
        >
        <br>
        <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Title:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.title}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">Description:</label>
          <br>
          <span class="textOverlay">{{devTrackContent.description}}</span>
        </div>

          <div
          class="tab-pane active show"
          id="nav-Details"
          role="tabpanel"
          aria-labelledby="nav-Details-tab"
        >
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Progress Status:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.progressStatus}}</span>
            </div>
          </div>

          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Group:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.group}}</span>
            </div>
          </div>

          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Severity:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.severity}}</span>
            </div>
          </div>


          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Found In Build:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.foundInBuild}}</span>
            </div>
          </div>

           <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Traget Release:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.tragetRelease}}</span>
            </div>
          </div>


          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Date Closed:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.dateClosed}}</span>
            </div>
          </div>

           <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Product:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.product}}</span>
            </div>
          </div>

          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Service Account:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.serviceAccount}}</span>
            </div>
          </div>

          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">Fixed In Release:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.fixedinRelease}}</span>
            </div>
          </div>

          <!-- <div class="row">
            <div class="col-lg-5">
              <label>Issue Id:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.ids}}</span>
            </div>
          </div>
           <div class="row">
            <div class="col-lg-5">
              <label>Current Owner:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.currentOwner}}</span>
            </div>
          </div>
           <div class="row">
            <div class="col-lg-5">
              <label>Case Reason:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.caseReason}}</span>
            </div>
          </div>
           <div class="row">
            <div class="col-lg-5">
              <label>Current Owner:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.currentOwner}}</span>
            </div>
          </div>
           
           <div class="row">
            <div class="col-lg-5">
              <label>Date Submitted:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.dateSubmitted}}</span>
            </div>
          </div>
           <div class="row">
            <div class="col-lg-5">
              <label>Final Test RootCause Analysis Comments:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.finalTestRootCauseAnalysisComments}}</span>
            </div>
          </div>
           
           <div class="row">
            <div class="col-lg-5">
              <label>Found In Build:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.foundInBuild}}</span>
            </div>
          </div>
           <div class="row">
            <div class="col-lg-5">
              <label>Found On Platform:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.foundOnPlatform}}</span>
            </div>
          </div>
           
          <div class="row">
            <div class="col-lg-5">
              <label>Hw PON:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.hwPON}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Priority:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.priority}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Problem Description Impacted:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.problemDescriptionImpacted}}</span>
            </div>
          </div>
         
          
          <div class="row">
            <div class="col-lg-5">
              <label>Reporting Customer:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.reportingCustomer}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Resolution:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.resolution}}</span>
            </div>
          </div>
           
          <div class="row">
            <div class="col-lg-5">
              <label>Submitted By:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.submittedBy}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Symptoms:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.symptoms}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Title:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.title}}</span>
            </div>
          </div>
         
          <div class="row">
            <div class="col-lg-5">
              <label>Type:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.type}}</span>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-5">
              <label>Workaround:</label>
            </div>
            <div class="col-lg-7">
              <span>{{devTrackContent.workaround}}</span>
            </div>
          </div>
 -->

        </div>
          </div>

      </div>
      <div class="actions">
        <button type="button" class="btn btn-danger" @click="hideModal()">OK</button>
      </div>
    </vudal>

    <div class="custom-container" style="paddingTop: 6%">
      <div class="row-one" style="paddingBo">
        <div class="myBreadCrumb">
          <p>
            <span style="font-size: 14px;">Solution</span>
          </p>
        </div>
        <div class="row">
          <div class="col-lg-12">
            <div class="p-3 mb-3 bg-white">
                 <div class="row align">
            <div class="col-md-2">
              <label>{{solutionScreenConstants.labAvailablity}}</label>
            </div>
            <div class="col-md-2" align="left">
              <i class="fas fa-dot-circle" style="color:green" v-if="showGreen"></i>
              <i class="fas fa-dot-circle" style="color:#d62828f7" v-if="!showGreen"></i>
            </div>
            <div class="col-md-4" v-if="analyzeFlag">
              <button type="button" style="fontSize:0.75vw;" class="btn btn-success" @click="onReserve()">{{solutionScreenConstants.buttons[1]}}</button>
            </div>
          </div>
              <div class="row align">
                <label class="col-md-6 labelweight">{{solutionScreenConstants.problemDescriptionName}}</label>
                <label class="col-md-6 labelweight">Problem Area</label>
              </div>

              <div class="row align">
                <div class="col-md-6">
                  <textarea
                  @change="problemDescriptionChange()"
                    v-model="problemDescription"
                    class="form-control"
                    rows="4"
                    id="email"
                    :placeholder="problemDescriptionPlaceholder"
                  ></textarea>
                </div>
                <div class="col-md-6"> 
                <div class="row">
                  <div class="col-md-12">
                    <Multiselect
                          v-model="filterValue"
                          tag-placeholder="Add this as new tag"
                          placeholder="Problem Area"
                          label="name"
                          track-by="name"
                          :options="filterOptions"
                          :close-on-select="false"
                          :multiple="true"
                          :clear-on-select="false"
                          :hide-selected="true"
                          :taggable="true"
                        ></Multiselect>
                  </div>
                  <div class="col-lg-8">
                    <br/>
              <!-- <tagsinput
                class="tags form-control"
                style="color: #495057"
                :tags="tags"
                placeholder="Add Tags"
                @tags-change="handleChange"
              ></tagsinput> -->
                  </div>
                  <div class="col-lg-2" style="paddingTop:1.89em">
                  <button
                    v-if="problemDescription !== ''"
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="getMlKeywords()"
                  >{{solutionScreenConstants.buttons[0]}}</button>
                  <button
                    v-if="problemDescription === ''"
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="getMlKeywords()"
                    disabled
                  >{{solutionScreenConstants.buttons[0]}}</button>
                </div>
                <div class="col-lg-2" style="paddingTop:1.89em">
                  <button
                    v-if="searchFlag "
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="onAnalyze()"
                  >{{solutionScreenConstants.buttons[2]}}</button>
                  <button
                    v-if="!searchFlag "
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="onAnalyze()"
                    disabled
                  >{{solutionScreenConstants.buttons[2]}}</button>
                </div>
                </div>
               
                </div>
              </div>
              <!-- <div class="row">
                <div class="col-lg-10"></div>
                <div class="col-lg-2">
                  <button
                    v-if="problemDescription !== ''"
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="onAnalyze()"
                  >{{solutionScreenConstants.buttons[0]}}</button>
                  <button
                    v-if="problemDescription === ''"
                    style="fontSize:0.75vw;"
                    type="button"
                    class="btn btn-success btn-block"
                    @click="onAnalyze()"
                    disabled
                  >{{solutionScreenConstants.buttons[0]}}</button>
                </div>
              </div> -->
            </div>
          </div>
        </div>
      </div>

      <div class="row" style="textAlign:center" v-if="analyzeFlag">
        <div class="col-lg-12">
          <div class="row  ">
           
            <div class="col-lg-4" >
              <div class="card  shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b1color , color:textcolor1}">
                <div class="card-body in-progress labelweight cardFontChange"
                @click="showDevTrack()"> <span class="float-left">Dev Track</span>
                <span class="float-right">{{this.devTrackData.length}}</span> </div>
              </div>
            </div>
            
            <div class="col-lg-4">
              <div class="card shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b2color , color:textcolor2}">
                <div class="card-body in-progress labelweight cardFontChange"
                @click="showReleaseNotes()">
                <span class="float-left">Release Notes</span>
                <span class="float-right">0</span> </div>
              </div>
            </div>
            
            <div class="col-lg-4">
              <div class="card shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b3color , color:textcolor3}">
                <div class="card-body in-progress labelweight cardFontChange"
                v-bind:style="{ backgroundColor: b3color }"
                @click="showSDFC()"><span class="float-left">SDFC</span>
                <span class="float-right">0</span> </div>
              </div>
            </div>
           
          </div>
        </div>
      </div>

      <div class="row" v-if="devTrackFlag" style="marginTop:-1.8%">
          <div class="col-lg-12">
            <div class="p-3 mb-3 bg-white">
              <!-- <div class="row">
               
                <div class="col-md-10">
                <h5 align="left" >Dev Track</h5>
                </div>
            </div> -->

              <div class="row align">
                <div class="col-md-12" align="center">
              <table class="table responsive table-hover">
                <thead>
                  <th>Issue Id</th>
                  <th style="width: 55.66%">Title</th>
                  <th >Severity</th>
                  <th>Found In Release</th>
                  <th>Date Submitted</th>
                </thead>
                <tbody>
                  <tr v-for="item in devTrackData" :key="item.ids"
                  
                  
                  @click="showPatchModal(item.index)"
                  >
                  <td class=" in-progress">
                    {{item.ids}}</td>
                    <td class=" in-progress">{{item.title}}</td>
                      <td class=" in-progress">{{item.severity}}</td>
                      <td class=" in-progress">{{item.fixedinRelease}}</td>
                      <td class=" in-progress">{{item.dateSubmitted}}</td>
                    </tr>
                </tbody>
                <!-- <tbody>
                  <tr 
                  
                  
                  @click="showPatchModal(item.index)"
                  >
                  <td class=" in-progress">111111
                    </td>
                      <td class=" in-progress">major</td>
                    
                    <td class=" in-progress">Dev Track</td>
                    <td class=" in-progress">12/03/13</td>
                    </tr>
                    <tr 
                  
                  
                  @click="showPatchModal(item.index)"
                  >
                  <td class=" in-progress">2222
                    </td>
                      <td class=" in-progress">major</td>
                    
                    <td class=" in-progress">Dev Track2</td>
                    <td class=" in-progress">13/03/13</td>
                    </tr>
                    <tr 
                  
                  
                  @click="showPatchModal(item.index)"
                  >
                  <td class=" in-progress">33333
                    </td>
                      <td class=" in-progress">minor</td>
                    
                    <td class=" in-progress">Dev Track 3</td>
                    <td class=" in-progress">12/05/13</td>
                    </tr>

                 
                   
                </tbody> -->
              </table>
            </div>
                </div>

                
              
             
            </div>
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
  </div>
</template>
<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";
import swal from "sweetalert";
import Vudal from "vudal";
import Multiselect from "vue-multiselect";
import tagsinput from "vue-tagsinput";

//import * as data from "../../utilies/tabledata.json";

export default {
  name: "MockUpNew",
  components: {
    SideNav,
    headernav,
    Multiselect,
    tagsinput,
    Vudal
  },
  created() {
    clearInterval(window.intervalObj);
  },
  data() {
    console.log("dashboard", this.data);
    return {
      isLoading: false,
      tags: [],
      solutionScreenConstants: constant.SolutionScreen,
      showGreen: true,
      searchFlag:false,
      devTrackData: [],
      errorFlag: false,
      tarFileName: "",
      tarFile: "",
      b1color: "",
      b2color: "",
      b3color: "",
      textcolor1:"",
      textcolor2:"",
      textcolor3:"",
      rl1color: "",
      rl2color: "",
      devTrackContent: "",
      filterOptions:[],
      filterValue:[],
      problemDescriptionPlaceholder: "Enter the Problem Description",
      valueIndex: "",
      releaseFlag: true,
      patchFlag: false,
      problemDescription: "",
      analyzeFlag: false,
      devTrackFlag: false,
      releaseNotesFlag: false,
      sdfcFlag: false,
      mlKeywords:""
    };
  },
  methods: {
    onReserve() {
      console.log(this.showGreen);
      if (this.showGreen) {
        this.showGreen = false;
      } else {
        this.showGreen = true;
      }
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
    },
      showDevTrack(){
          this.devTrackFlag=true;
          this.b1color="#2a629a";
          this.textcolor1="#f8f9fa";
          this.b2color="";
          this.textcolor2="";
          this.b3color="";
          this.textcolor3="";

      },
      showPatchModal(index) {
      this.patchFlag = true;
      this.devTrackContent=this.devTrackData[index];
      this.releaseFlag = false;
      this.$modals.myModal.$show();
    },
      showReleaseNotes(){
        this.devTrackFlag=false;
        this.b2color="#2a629a";
        this.textcolor2="#f8f9fa";
        this.b1color="";
        this.textcolor1="";
        this.b3color="";
        this.textcolor3="";
      },
      showSDFC(){
           this.devTrackFlag=false;
           this.b3color="#2a629a";
          this.textcolor3="#f8f9fa";
           this.b2color="";
          this.textcolor2="";
          this.b1color="";
          this.textcolor1="";
      },
      onAnalyze() {
      this.isLoading=true;
      this.errorFlag=false;
      this.devTrackData=[];
      if(this.filterValue.length>0)
      {
        this.mlKeywords="OR";
      }else{
        this.mlKeywords="";
      }
      for(var i=0;i<this.filterValue.length;i++)
      {
        this.mlKeywords=this.mlKeywords+" "+this.filterValue[i].name;
      }
     
      fetch(constant.ELKURL+"api/getDevTrackData?search_param="+this.problemDescription+" "+this.mlKeywords, {
      
      headers: {
        'Content-Type': 'application/json'
      }
       })
         .then(response => {
           response.text().then(text => {
             const data = text && JSON.parse(text);
             if (data.http_status_code === 200) {
              this.isLoading=false;
              if(data.data.devTrack.length < 0){
                 this.analyzeFlag = true;
              }
             
              for(var i=0;i<data.data.devTrack.length;i++)
              {
                
                  
                  this.devTrackData.push({ids:data.data.devTrack[i].id,index:i,
                description:data.data.devTrack[i].description,
                severity:data.data.devTrack[i].severity,
                caseReason:data.data.devTrack[i].caseReason,
                currentOwner:data.data.devTrack[i].currentOwner,
                dateClosed:data.data.devTrack[i].dateClosed,
                dateSubmitted:data.data.devTrack[i].dateSubmitted,
                finalTestRootCauseAnalysisComments:data.data.devTrack[i].finalTestRootCauseAnalysisComments,
                fixedinRelease:data.data.devTrack[i].fixedinRelease,
                foundInBuild:data.data.devTrack[i].foundInBuild,
                foundOnPlatform:data.data.devTrack[i].foundOnPlatform,
                group:data.data.devTrack[i].group,
                product:data.data.devTrack[i].product,
                progressStatus:data.data.devTrack[i].progressStatus,
                reportingCustomer:data.data.devTrack[i].reportingCustomer,
                resolution:data.data.devTrack[i].resolution,
                serviceAccount:data.data.devTrack[i].serviceAccount,
                submittedBy:data.data.devTrack[i].submittedBy,
                symptoms:data.data.devTrack[i].symptoms,
                title:data.data.devTrack[i].title,
                tragetRelease:data.data.devTrack[i].tragetRelease,
                type:data.data.devTrack[i].type,
                workaround:data.data.devTrack[i].workaround});
                
                
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
             this.mlKeywords = "";
           });
         })
         .catch(handleError => {
           console.log(" Error Response ------->", handleError);
         });
    },
    getMlKeywords()
    {
      this.mlKeywords = ''
      fetch(constant.ELKURL + "api/get_ml_keywords?search_param="+this.problemDescription, {
         
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
             if (data.http_status_code === 200) {
              this.isLoading=false;
              let count = 0
              for(var i=0;i<data.ml_keywords.length;i++)
              {
                this.filterOptions.push({
                  name:data.ml_keywords[i]
                });
                 this.filterValue.push({
                  name:data.ml_keywords[i]
                });
                console.log("count ----->",count)
                
                
              }
              this.searchFlag=true;
             }
             
           });
         })
         .catch(handleError => {
           console.log(" Error Response ------->", handleError);
         });
    },
     hideModal() {
      this.$modals.myModal.$hide();
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    routeDashboard() {
      router.push("/");
    },
    problemDescriptionChange()
    {
      if(this.problemDescription === "")
      {
        this.searchFlag=false;
      }
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
.contentwidth {
  width: 80%;
}

.textOverlay {
  word-break: break-all;
}
.navHeaderColor {
  color: #495057;
}

.labelweight {
  font-weight: 800;
}
</style>
