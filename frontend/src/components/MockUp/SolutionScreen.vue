<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 5%">
         <div class="myBreadCrumb" style="margin-bottom:1px;fontSize:0.875em">
          <p>
            <span class="in-progress" >Solution</span>
           
          </p>
        </div>
     <div class="row">
         
         <div class="col-md-5 align-margin bg-white align" >
           <div class="row align">
             <label class="col-md-10">Problem Description </label>
           
           </div>

            <div class="row align ">
            <div class="col-md-10">
             <textarea  class="form-control " rows="4" id="email"  placeholder="Enter the Problem Description" ></textarea>
           </div>
           </div>
          
           <div class="row align">
             <label class="col-md-10">Log Info</label>
           
           </div>

            <div class="row align ">
            <div class="col-md-10">
             <textarea  class="form-control " col="4" id="email"  placeholder="Enter the Log-Info" ></textarea>
           </div>
           </div>
            
             <div class="row align">
             <label class="col-md-10">Tags</label>
           
           </div>

            <div class="row align ">
            <div class="col-md-10 ">
             <tagsinput
             class="tags form-control"
             style="color: #495057"
                :tags="tags"
                placeholder= "Add Tags"
                @tags-change="handleChange"
             ></tagsinput>
           </div>
           </div>
            

           <div class="row align">
             <label class="col-md-10">TAR Ball</label>
           
           </div>

            <div class="row align ">
            <div class="col-md-10">
            <div class="row">
                <div class="col-lg-1" >
                  <label for="fileupload" class="file">
                    <input type="file" @change="handleFile" id="fileupload" style="display:none">
                    <i class="fas fa-paperclip fa-1.5x in-progress"></i>
                  </label>
                </div>
                <div class="col-lg-8" >
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
                    @click="onReserve()"
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
                 <div class="col-md-4">  <button
                    type="button"
                    class="btn btn-success"
                    @click="onReserve()"
                    v-tooltip.top.hover.focus="'Move to Reference Page'"
                     >Reserve</button></div>
             </div>
       
             <div class="row align">
                 
                     <div class="col-md-12">
                     <h5 align="center"> Potential Problem Areas</h5>
                     </div>
             </div>
             <div class="row align">
                    <div class="col-md-1"></div>
                     <div class="col-md-10 " align="center" >
                         <table class="table responsive">
                             <tbody>
                                 <tr>
                                     <td class="in-progress">Electrical</td>
                                     <td>76%</td>
                                 </tr>
                                 <tr>
                                     <td class="in-progress">Mechanical</td>
                                     <td>65%</td>
                                 </tr>
                                 <tr>
                                     <td class="in-progress">Software</td>
                                     <td>45%</td>
                                 </tr>
                             </tbody>
                         </table>
                     </div>
             </div>

             
             <div class="row align">
                 
                     <div class="col-md-12">
                     <h5 align="center"> Solution and Effectiveness</h5>
                     </div>
             </div>
             <div class="row align">
                    <div class="col-md-1"></div>
                     <div class="col-md-10 " align="center" >
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

             <div class="row ">
                     <div class="col-md-12">
                     <h5 align="center"> Release Notes</h5>
                     </div>
             </div>

             <div class="row ">
                     <div class="col-md-12">
                         <div class="row">
                            <div class="col" style="text-align: center"> RN1</div>
                            <div class="col" style="text-align: center"> RN2</div>
                            <div class="col" style="text-align: center"> RN3</div>
                         </div>
                        
                     </div>
             </div>
             
             <div class="row align">
                     <div class="col-md-12">
                     <h5 align="center"> Patches</h5>
                     </div>
             </div>

             <div class="row ">
                     <div class="col-md-12">
                         <div class="row">
                            <div class="col" style="text-align: center"> P1</div>
                            <div class="col" style="text-align: center"> P2</div>
                            <div class="col" style="text-align: center"> P3</div>
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
        tags:[],
        showGreen : true,
        tarFileName:'',
        tarFile:''
      
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
      onReserve()
      {
          console.log(this.showGreen);
          if(this.showGreen)
          {
              this.showGreen=false;
          }
          else{
              this.showGreen=true;
          }
      },
      handleChange(removeIndex,tag)
      {
          if(this.tags.length == removeIndex)
          {
              console.log(removeIndex);
              this.tags.push(tag);

          }
          else{
              this.tags.splice(removeIndex,1);
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

.align{

  padding:0.75em;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.align-rl{

  padding-left:8em;
}

.align-margin{

  margin-left:3em;
   margin-right:3em;
}
.tags{
   color: #495057 !important;
   font-size: 1rem !important;
   border: 1px solid #ced4da !important;
    border-radius: .25rem !important;
    transition: border-color .15s ease-in-out,box-shadow .15s ease-in-out !important;
}

::input-placeholder {
  opacity: 10;
  color:brown;
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

