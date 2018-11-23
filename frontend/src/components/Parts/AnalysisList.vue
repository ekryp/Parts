<template>
     <div>
     <side-nav menu="analysis" />
     <div class="custom-container" style="padding:3%">
     <div class="row" style="color: green">
         <div class="col-lg-2">
             <span class="text-top">Total Analysis Request</span><br/>
        </div>
        <div class="col-lg-2">
             <span class="text-top">Completed Request</span><br/>
        </div>
        <div class="col-lg-2">
             <span class="text-top">Completed Request with Error</span><br/>
        </div>
        <div class="col-lg-2">
             <span class="text-top">Completed Request Successfully</span><br/>
        </div>
        <div class="col-lg-2">
             <span class="text-top">Requests In Progress</span><br/>
        </div>
        <div class="col-lg-2">
             <span class="text-top">Requests To Be Submitted</span><br/>
        </div>
    </div>
    <div class="row" style="marginTop:2%">
        <div class="col-lg-2">
             <span class="count">100</span>
        </div>
         <div class="col-lg-2" style="color: red">
             <span class="count">10</span>
        </div>
         <div class="col-lg-2">
             <span class="count">100</span>
        </div>
         <div class="col-lg-2" style="color: red">
             <span class="count">10</span>
        </div>
         <div class="col-lg-2">
             <span class="count">100</span>
        </div>
         <div class="col-lg-2">
             <span class="count">100</span>
        </div>
    </div>
    <div class="float-right" style="marginTop:3%">
        <button type='button' class='btn btn-success' @click="createAnalysis" >Create Analysis</button>
    </div>
    <div class="shadow-lg p-3 mb-5 bg-white rounded" style="marginTop:10%">
    <div class="row" >
        <div class="col-lg-4">
            <input type='text' class='form-control' placeholder='Search by Analysis Name'>
        </div>
         <div class='col-lg-4'>
            </div>
        <div class='col-lg-4'>
            <multiselect placeholder='Filter By Status'  :options='options' label='name' :multiple='false' :taggable='true'></multiselect>
        </div>
       </div>
       <div style="marginTop:3%">
       <table class="table table-borderless">
  <thead>
    <tr style="color:green">
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
    <tr>
      <th scope="row">4</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
    <tr>
      <th scope="row">5</th>
      <td>Larry</td>
      <td>the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
</div>
    </div>
    </div>
    </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import Multiselect from "vue-multiselect";

export default {
  name: "PartsAnalysisList",
  components: {
    SideNav,
    Multiselect
  },
  data() {
    console.log("AnalysisList");
    return {
      options: [
        { name: "Vue.js", code: "vu" },
        { name: "Javascript", code: "js" },
        { name: "Open Source", code: "os" }
      ]
    };
  },
  methods: {
    createAnalysis() {
      router.push("/parts/analysis");
    }
  }
};
</script>
<style>
.content {
  max-width: 500px;
  margin: auto;
  background: white;
  padding: 10px;
}
.text-top {
  font-size: 1vw;
}
.count {
  font-size: 2vw;
}
</style>
