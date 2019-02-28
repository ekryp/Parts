<template>
<div>
     <headernav msg="Dashboard" :loaderFlag="loaderFlag"/>
    <side-nav/>
     

 <vudal name="myModal">
  <div class="header">
    <i class="close icon"></i>
   <h4 v-if="addFlag">Create Role</h4>
    <h4 v-if="editFlag">Edit Role</h4>
  </div>
  <div class="content">
    <div class="form-group text-left" >
      
      <div>
         <div class="row" align="">
                <label class="col-lg-3" for="usrname">Name :</label>
                <input class="col-lg-8"  type="text" id="usrname"   v-model="roleName">
                </div>
                <br>
                <div class="row">
                <label for="psw" class="col-lg-3">Description : </label>
                <textarea class="col-lg-8"  id="psw" name="psw"  v-model="roleDescription" ></textarea>
                </div>
                <br>
                <div class="row">
                <label for="psw" class="col-lg-3">Permissions : </label>
                
  
                </div>
                 <br>
                 
                <Multiselect v-model="permissionValue" tag-placeholder="Add this as new tag" placeholder="Search or add a Permission" label="name" 
                track-by="_id" :options="options" :multiple="true" :taggable="true" @tag="addTag"></Multiselect>
               
      </div>
        </div>
      
  </div>
  <div class="actions">
    <button v-if="addFlag"  type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Create'" @click="addRoleData()">
                    Create
                </button>
    <button v-if="editFlag" type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Update'" @click="editRoleData()">
                    Update
                </button>
                <button
                type="button"
                class="btn btn-danger"
                @click="hideEntry()"
                v-tooltip.top.hover.focus="'Cancel the option'"
              >Cancel</button>
  </div>
</vudal> 





    <div class="custom-container" style="paddingTop: 6%">
    <div class="row col">
      <div class="col" align="center">
      <h3>Role Management </h3>
      </div>
    </div>
    <br>
    <br>
      <div class="row">
        <div class="col-lg-12">
          <div class=" p-3 mb-5 bg-white ">
              
           <h5 class="gridTitle col-lg-12 " style="marginLeft:-1%" >Role</h5>
            <br>
            
            <div class="row">
                <div class="col-lg-12">
                   
                    
                    <button class="btn btn-sm btn-success" style="margin-bottom: 2%;marginLeft:1%" @click="showAddRole()">Add Role
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
                    <td >{{role.role_name}}</td>
                    <td >{{role.role_description}}</td>
                    <td >
                        &nbsp&nbsp&nbsp&nbsp
                         <button class="btn btn-sm btn-primary" @click="showEditRole(role)">Edit
                                            </button>&nbsp&nbsp
                                            <button class="btn btn-sm btn-danger" @click="deleteRole(role)">Delete
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
import Vudal from "vudal";

export default {
  name: "UserRoleManagement",
  components: {
    SideNav,
    headernav,
    Vudal,
    Multiselect
  },
  created() {
    clearInterval(window.intervalObj);
   
    this.getAllRoles();
    this.getAllPermissions();
    
  },
  data() {
    
    return {
    allRoles:[],
    allPermissions:[],
    editFlag: false,
    addFlag: true,
    roleName:'',
    roleId:'',
    roleDescription:'',
    permissionValue:[],
    options: []
    };
  },
  methods: {

     addTag (newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
      }
      console.log(tag);
      this.options.push(tag)
      this.value.push(tag)
    }
  ,
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    showAddRole()
    {
    this.editFlag=false;
    this.addFlag=true;
    this.roleName='';
    this.roleDescription='';
    this.$modals.myModal.$show();
    },
    addRoleData()
    {
          let formData = new FormData();
         formData.append("role_name", this.roleName);
         formData.append("role_description", this.roleDescription);
         formData.append("role_permission", JSON.stringify(this.permissionValue));
      console.log(this.permissionValue);
         
        //  let roleDate={
        //    role_name:this.roleName,
        //    role_description:this.roleDescription,
        //    role_permission:JSON.stringify(this.permissionValue)
        //  }
        fetch(constant.APIURL + "api/v1/info/members/create-role", {
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
            if (data.http_status_code === 200) {
              
              swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              });
            } else {
              swal({
                title: "Error",
                text: "Role Creation Failed",
                icon: "error"
              });
            }
            console.log("data -- response-->", data);
            this.permissionValue=[];
            this.getAllRoles();
            this.$modals.myModal.$hide();
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },

    editRoleData()
    {
       let formData = new FormData();
         formData.append("role_name", this.roleName);
         formData.append("role_description", this.roleDescription);
         formData.append("role_id",this.roleId);
         formData.append("role_permission", JSON.stringify(this.permissionValue));
      console.log(this.permissionValue);
        
        fetch(constant.APIURL + "api/v1/info/members/modify-role", {
        method: "PUT",
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
            if (data.http_status_code === 200) {
              
              swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              });
            } else {
              swal({
                title: "Error",
                text: "Role Updation Failed",
                icon: "error"
              });
            }
            console.log("data -- response-->", data);
            this.permissionValue=[];
            this.getAllRoles();
             this.$modals.myModal.$hide();
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    deleteRole(role)
    {
console.log(role);
       let roleId = role.role_id;
          
          swal({
            title: "Info",
            text: "Do You Want to Delete the Role ?",
            icon: "info"
          }).then(ok => {
            if (ok) {
              fetch(
                constant.APIURL +
                  "api/v1/info/members/delete-role?role_id=" +
                  roleId,
                {
                  method: "DELETE",
                  headers: {
                    Authorization:
                      "Bearer " + localStorage.getItem("auth0_access_token")
                  }
                }
              )
                .then(response => {
                  response.text().then(text => {
                    const data = text && JSON.parse(text);

                    console.log("data -getallrequest--->", data);

                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                          this.getAllRoles();
                        }
                      });
                    } else {
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
            }
          });
    },
    showEditRole(role){
      this.editFlag=true;
      this.addFlag=false;
      this.roleName=role.role_name;
      this.roleId=role.role_id;
      this.roleDescription=role.role_description;
      for(let i=0;i<role.role_permission.length;i++)
      {
        for(let j=0;j<this.options.length;j++)
        {
          if(role.role_permission[i] === this.options[j]._id)
          {
            this.permissionValue.push(this.options[j]);
          }
        }
      }
      this.$modals.myModal.$show();
    },
    hideEntry(){
      this.permissionValue=[];
    this.$modals.myModal.$hide();
    },
    showModal(){
      this.$modals.myModal.$show();
    },
    getAllRoles()
    {
      this.allRoles=[];
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
            for (let i = 0; i < data.length; i++) {
              this.allRoles.push({
                role_name: data[i].name,
                role_id:data[i]._id,
                role_description:data[i].description,
                role_permission: data[i].permissions
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
    ,
    getAllPermissions()
    {
      fetch(constant.APIURL + "api/v1/info/members/all-permissions" , {
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
            for (let i = 0; i < data.permissions.length; i++) {
              this.allPermissions.push({
                id: data.permissions[i]._id,
                description:data.permissions[i].description,
                name: data.permissions[i].name
              });
              this.options.push(data.permissions[i]);
            }
            console.log('new permission',this.allPermissions);
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
