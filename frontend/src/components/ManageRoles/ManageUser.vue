<template>
<div>
     <headernav msg="Dashboard"/>
    <side-nav/>
     
    <div class="custom-container" style="paddingTop: 6%">
    <div class="row col">
      <div class="col" align="center">
      <h3>User Management </h3>
      </div>
    </div>
    <br>
    <br>
      <div class="row">
        <div class="col-lg-12">
          <div class=" p-3 mb-5 bg-white ">
              
           <h5 class="gridTitle col-lg-12 " style="marginLeft:-1%" >Users</h5>
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
                <tr v-for="role in allRoles" :key="role.name">
                    <td >{{role.name}}</td>
                    <td >{{role.description}}</td>
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
  name: "ManageUser",
  components: {
    SideNav,
    headernav
  },
  created() {
    clearInterval(window.intervalObj);
   
    this.getAllRoles();
    
  },
  data() {
    
    return {
    allRoles:[]
    };
  },
  methods: {
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    getAllRoles()
    {
      fetch(constant.APIURL + "api/v1/info/members/all-role" , {
        method: "GET",
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
            console.log("data -- get_top_extended-->", data);
            //this.allRoles = data;
            for (let i = 0; i < this.data.length; i++) {
              this.allRoles.push({
                name: this.data[i].name,
                description:this.data[i].description,
                permissions: this.data[i].permissions
              });
            }
            $(document).ready(function() {
              $("#example").DataTable();
            });
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

</style>
