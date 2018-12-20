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
            <div class="col-lg-6">
              <div class="col-lg-3">
                <label>Refernce Name :</label>
              </div>
              <div class="col-lg-6">
                <input type="text" class="form-control" placeholder="Enter Reference Name">
              </div>
            </div>
            <div class="col-lg-6">
              <div class="col-lg-3">
                <label>Refernce Version :</label>
              </div>
              <div class="col-lg-6">
                <input type="text" class="form-control" placeholder="Enter Reference Version">
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-10">
            <div class="form-group">
              <div class="col-lg-3">
                <label>Reference File :</label>
              </div>
              <div class="col-lg-6">
                <div class="row">
                  <div class="col-lg-1">
                    <label for="fileupload" class="file">
                      <input type="file" @change="handleFile" id="fileupload" style="display:none">
                      <i class="fas fa-paperclip fa-2x"></i>
                    </label>
                  </div>
                </div>
              </div>
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
            <tr>
              <td>
                <input type="checkbox" value>
              </td>
              <td>Mark</td>
              <td>Otto</td>
              <td>
                <i class="fas fa-pencil-alt"></i>
              </td>
            </tr>
            <tr>
              <td>
                <input type="checkbox" value>
              </td>
              <td>Jacob</td>
              <td>Thornton</td>
              <td>
                <i class="fas fa-pencil-alt"></i>
              </td>
            </tr>
            <tr>
              <td>
                <input type="checkbox" value>
              </td>
              <td>Larry</td>
              <td>the Bird</td>
              <td>
                <i class="fas fa-pencil-alt"></i>
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

export default {
  name: "Reference",
  components: {
    SideNav,
    headernav
  },
  created() {},
  data() {
    console.log("home");
    return {
      analysisfile: "",
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
    handleFile() {},

    uploadData() {
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
