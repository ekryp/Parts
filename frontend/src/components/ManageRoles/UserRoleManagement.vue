<template>
<div>
     <headernav msg="Dashboard"/>
    <side-nav/>
     
    <div class="custom-container" style="paddingTop: 10%">
      <div class="row">
        <div class="col-lg-12">
          <div class=" p-3 mb-5 bg-white ">
              
           <h5 class="gridTitle col-lg-12 " style="marginLeft:-1%" >Roles</h5>
            <br>
            
            <div class="row">
                <div class="col-lg-12">
                   
                    
                    <button class="btn btn-sm btn-success" style="margin-bottom: 2%;marginLeft:1%" @click="editRoleModal('','add')">Add Role
                                    </button>
            <table id="example" class="table table-bordered col-lg-12" align="center"  style="fontSize:14px">
              <thead align="left">
                <tr>
                  <th  scope="col">Name</th>
                  <th  scope="col">Description</th>
                  <th  align="center">Action</th>
                </tr>
              </thead>
              <tbody >
                <!-- <tr v-for="item in top_extended" :key="item.id">
                  <td>{{item.customer_name}}</td>
                  <td>{{item.part_name}}</td>
                  <td>{{item.depot_name}}</td>
                  <td>{{item.critical_pon_count}}</td>
                </tr> -->
                <tr>
                    <td >Phoenix</td>
                    <td >asdsad</td>
                    <td >
                        &nbsp&nbsp&nbsp&nbsp
                         <button class="btn btn-sm btn-primary" @click="editRoleModal(row,'edit')">Edit
                                            </button>&nbsp&nbsp
                                            <button class="btn btn-sm btn-danger" @click="confirmBeforeDelete(row['_id'])">Delete
                                            </button>
                    </td>
                </tr>
                <tr>
                    <td >Phoenix</td>
                    <td >asdsad</td>
                    <td >
                        &nbsp&nbsp&nbsp&nbsp
                         <button class="btn btn-sm btn-primary" @click="editRoleModal(row,'edit')">Edit
                                            </button>&nbsp&nbsp
                                            <button class="btn btn-sm btn-danger" @click="confirmBeforeDelete(row['_id'])">Delete
                                            </button>
                    </td>
                </tr>
                <tr>
                    <td >Phoenix</td>
                    <td >asdsad</td>
                    <td >
                        &nbsp&nbsp&nbsp&nbsp
                         <button class="btn btn-sm btn-primary" @click="editRoleModal(row,'edit')">Edit
                                            </button>&nbsp&nbsp
                                            <button class="btn btn-sm btn-danger" @click="confirmBeforeDelete(row['_id'])">Delete
                                            </button>
                    </td>
                </tr>
              </tbody>
            </table>
            </div>
            </div>
          </div>
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
import Multiselect from "vue-multiselect";
import * as constant from "../constant/constant";
//import * as data from "../../utilies/tabledata.json";

export default {
  name: "UserRoleManagement",
  components: {
    SideNav,
    headernav
  },
  created() {
    clearInterval(window.intervalObj);
    $(document).ready(function() {
     $("#example").DataTable();
     });
    
  },
  data() {
    console.log("dashboard", this.data);
    return {
      data: [],
      top_extended: [],
      topTable: "true",
      midTable: "false",
      lastTable: "false",
      customer: null,
      parts: null,
      depots: null,
      partName: "",
      customerName: "",
      toggle: "reorder",
      state: true
    };
  },
  methods: {
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    }
    
  }
};
</script>
<style>

</style>
