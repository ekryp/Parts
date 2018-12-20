<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 5%">
        <div class="row">
        <div class="myBreadCrumb"  style="margin-bottom:1px">
          <p>
          <span  style="font-size: 14px;">Upload</span>
          </p>
        </div>
        </div>
      <div class="row" >
        <div class="col-lg-12 col-lg-12 shadow-lg p-3 mb-5 bg-white rounded">
          <h4>Upload Reference File</h4>
           <div class="row" style="marginTop:2%">
              <div class="col-lg-2" >
                <label>Version Name :</label>
              </div>
              <div class="col-lg-3">
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter Version Name"
                  v-model="analyisisName"
                >
              </div>
              <div class="col-lg-1">
              </div>
              <div class="col-lg-2">
                <label>Version No :</label>
              </div>
              <div class="col-lg-3">
                <input
                  type="text"
                  class="form-control"
                  placeholder="Enter Version No"
                  v-model="analyisisName"
                >
              </div>
              
            </div>
            <br>
            <div class="input-group">
            <div class="custom-file">
                <input type="file" class="custom-file-input" id="inputGroupFile01" @change="analysisFile" style="display:none">
                <label class="custom-file-label" for="inputGroupFile01">Choose file</label>
            </div>
            </div> 
            
            <div class="input-group-prepend" style="marginTop:2%" >
                <span class="input-group-text" id="inputGroupFileAddon01" @click="uploadData()"  style="marginLeft:42%">Upload</span>
                <span class="input-group-text" id="inputGroupFileAddon01" @click="uploadData()" style="marginLeft:3%">Reset</span>
            </div>
            
        </div>
      </div>
      
      <div class="row">
        <div class="col-lg-12 shadow-lg p-3 mb-5 bg-white rounded">
              <h4>Reference File Table</h4>
            <div class="card-body" style="margin-bottom:20px">
              
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th scope="col">S.No</th>  
                      <th scope="col">File Name</th>
                      <th scope="col">Version</th>
                      <th scope="col">Default</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>1</td>
                      <td>ABC.txt</td>
                      <td>1.0</td>
                      <td><input type="checkbox" name="vehicle3" value="{item.high_spare}" ></td> 
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>123.txt</td>
                        <td>1.1</td>
                        <td><input type="checkbox" name="vehicle3" value="{item.high_spare}" checked></td> 
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>ABC123.txt</td>
                        <td>2.0</td>
                        <td><input type="checkbox" name="vehicle3" value="{item.high_spare}" ></td> 
                    </tr>
                  </tbody> 
                </table>
              </div> 
            
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";

export default {
  name: "UploadData",
  components: {
    SideNav,
    headernav
  },
  created() {
    
  },
  data() {
    console.log("home");
    return {
        analysisfile:"",
        analysisFileName: ""


    };
  },
  methods: {
       analysisFile(e) {
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

      uploadData()
      {
          console.log(this.analysisFile);
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
