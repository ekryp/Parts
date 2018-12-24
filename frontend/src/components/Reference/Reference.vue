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
     <div class="shadow-lg p-3 mb-5 bg-white rounded">
       <h5>Refernce File Information</h5>
       <div class="form-group">
         <div class="row" style="marginTop:2%">
           <div class="col-lg-5">
             <div class="col-lg-4">
               <label style="font-size:19px"> Refernce Name :</label>
             </div>
             <div class="col-lg-6">
              <input v-if="referenceId === ''"  
               type="text" 
               class="form-control"
              placeholder="Enter Reference Name" 
              v-model="referenceName">
              <input v-if="referenceName !== '' && referenceName !== undefined"
               type="text" 
               class="form-control"
               v-model="referenceName"
               >
             </div>
           </div>
           <div class="col-lg-5">
             <div class="col-lg-4">
               <label style="font-size:19px">Reference File :</label>
             </div>
             <div class="col-lg-6">
               <div class="row">
                 <div class="col-lg-1">
                   <label for="fileupload" class="file">
                     <input type="file" @change="analysisFile" id="fileupload" style="display:none">
                     <i class="fas fa-paperclip fa-2x"></i>
                   </label>
                 </div>
                 <div style="paddingLeft:7%">
                   <span>{{analysisFileName}}</span>
                 </div>
               </div>
             </div>
           </div>
           <div class="col-lg-2">
             <button  v-if="referenceId !== ''" type="button" class="btn btn-success" @click="updateReferenceData()">Update</button>
             <button  v-else type="button" class="btn btn-success" @click="uploadReferenceData()">Save</button>
           </div>
         </div>
       </div>
     </div>
     <div class="shadow-lg p-3 mb-5 bg-white rounded">
       <table class="table">
         <thead>
           <tr>
             <th scope="col">Active Version</th>
             <th scope="col">Reference Name</th>
             <th scope="col">Version</th>
             <th scope="col">Update</th>
           </tr>
         </thead>
         <tbody>
           <tr
              v-for="reference in referenceDetails"
              :key="reference.id"
              style="fontSize:1vw; cursor:pointer"
            >
              <!-- <td class="left">{{item.customer_name}}</td> -->
              <td v-if="reference.isactive != 0">
                <input type="checkbox" name="{reference.id}" value="{reference.id}" id="{reference.id}"  checked >
              </td>
              <td v-else>
                <input type="checkbox" name="{reference.id}"  >
              </td>
              <td>{{reference.name}}</td>
              <td>{{reference.version}}</td>
              <td>
              <i class="fas fa-pencil-alt" @click="uncheckOthers(reference.id)"></i>
              </td>
            </tr>
         </tbody>
       </table>
     </div>
   </div>
 </div>
</template>

<script>
import router from "../../router";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";

export default {
  name: "Reference",
  components: {
    SideNav,
    headernav
  },
  created() {
    this.getreference();
  },
  data() {
    console.log("home");
    return {
      analysisfile: "",
      analysisFileName: "",
      referenceName:"",
      email_id:"khali.saran@ekryp.com",
      referenceDetails:[],
      referenceId:""
    };
  },
  methods: {
    analysisFile(e) {
      console.log("hi");
      console.log("image ----sap->", e.target.files);
      const file = e.target.files[0];
      if (
        file.name.endsWith("xlsx") ||
        file.name.endsWith("csv") ||
        file.name.endsWith("XLSX") ||
        file.name.endsWith("CSV")
      ) {
        console.log(file.name);
        this.analysisFileName = file.name;
        this.analysisfile = file;
      } else {
        alert("error");
      }
    },
    getreference() {
      console.log(this.email_id);
      fetch(
        constant.APIURL +
          "api/v1/getreference?user_email_id=" +
          this.email_id ,
        {
          method: "GET"
        }
      ).then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- Reference Data-->", data);
            this.referenceDetails = data;
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    }


    ,

    uploadReferenceData() {
      console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      this.email_id = "khali.saran@ekryp.com";
       let data = {
         referenceName: this.referenceName,
         analysisFileName: this.analysisFileName,
         analysisfile: this.analysisfile,
         email_id:this.email_id

       };
       if (
         this.referenceName !== "" ) {
         if (this.analysisfile !== "") {
             this.post_reference_data(data);
           }
           else {
           alert("Please add your Reference File");
         }
         } 
       else {
         alert("Please fill the Form to submit");
       }
     },
     uncheckOthers(id){
      //  let tmp=[1,3,4]
      //  console.log("The id is ",id);
      //  for(var i=0;i<this.referenceDetails.length;i++)
      //  {
      //    if(tmp[i]!=id)
      //    {
      //      console.log("The yttp is ",tmp[i]);
      //      //document.getElementById(String(tmp[i])).checked = false;
      //      $("#"+String(tmp[i])).prop("checked", false);
      //    }
        
      //    console.log("The  id is ",id);
      //  }
      //  //document.getElementById("checkbox").checked = false;
      for(var i=0;i<this.referenceDetails.length;i++)
       {
         if(this.referenceDetails[i].id===id)
         {
           this.referenceName=this.referenceDetails[i].name;
           this.referenceId=this.referenceDetails[i].id;
         }
         console.log("refer name",this.referenceName);
         console.log("refer ID",this.referenceId);
        }
     },
     updateReferenceData()
     {
       console.log(localStorage.getItem('email_id'));
      //let email_id = localStorage.getItem("email_id");
      this.email_id = "khali.saran@ekryp.com";
       let data = {
         referenceName: this.referenceName,
         analysisFileName: this.analysisFileName,
         analysisfile: this.analysisfile,
         email_id:this.email_id,
         //reference_id:this.referenceId

       };
         if (this.analysisfile !== "") {
             this.post_reference_data(data);
           }
           else {
           alert("Please add your Reference File");
         }
         }
         ,
     post_reference_data(data)
     {

      let formData = new FormData();

      formData.append("reference_name", data.referenceName);
      formData.append("user_email_id", data.email_id);
      formData.append("reference_file", data.analysisfile);
      if(this.referenceId !== "")
      {
        formData.append("reference_id",this.referenceId);
      }
      
      console.log("formdata ----->", formData.get("reference_file"));
      fetch(constant.APIURL + "api/v1/reference", {
        method: "POST",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("Response from backend data ---->", data);
            this.getreference();
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
