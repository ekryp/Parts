<template>
<div>
     <headernav msg="Dashboard" :loaderFlag="loaderFlag"/>
    <side-nav/>
     

 <vudal name="myModal">
  <div class="header">
    <i class="close icon"></i>
   <h4 v-if="editFlag">Manage Roles</h4>
   <h4 v-if="addFlag">Create User</h4>
  </div>
  <div class="content">
    <div class="form-group text-left" >
      
      <div v-if="editFlag">
                <br>
                <div class="row">
                <label for="psw" class="col-lg-3">Permissions : </label>
                </div>
                 <br>
                <Multiselect v-model="permissionValue" tag-placeholder="Add this as new tag" placeholder="Search or add a Permission" label="role_name" 
                track-by="role_id" :options="options" :multiple="true" :taggable="true" @tag="addTag"></Multiselect>  
      </div>
      <div v-if="addFlag">
        <div class="row" >
                <label class="col-lg-3" for="usrname">Username :</label>
                <input class="col-lg-8"  type="text" id="usrname" v-model="user.username" >
                </div>
                <br>
                <div class="row" >
                <label class="col-lg-3" for="email">Email :</label>
                <input class="col-lg-8"  type="text" id="email" v-model="user.email"  >
                </div>
                <br>
                <div class="row">
                  <div class="col-lg-6"><p> Auto Generate Password</p></div>
                   <div class="col-lg-1"></div>
                  <div class="col-lg-1">
                    <toggle-button
                      :value="state"
                      :color="{checked: 'green', unchecked: 'grey'}"
                      :sync="true"
                      cssColors:true
                      :labels="{checked: 'On', unchecked: 'off'}"
                      :width="80"
                      v-tooltip.top.hover.focus="'Click to Toggle'"
                      @change="stateChange()"
                    /> </div>
                   
                    
                 
                </div>
                <div class="row" v-if="!state">
                <label class="col-lg-3" for="password">Password :</label>
                <input class="col-lg-8"  type="text" id="password" v-model="user.password" >
                <div class="col-lg-3"></div>
                <p style="font-size:13px"> *Password should contain atleast one special character,number,<br>uppercase character and of length 8</p>
                </div>
                <br>
                <div class="row" v-if="!state">
                <label class="col-lg-3" for="password">Confirm Password :</label>
                <input class="col-lg-8"  type="password" id="password" v-model="user.cnf_password" >
                <div class="col-lg-3"></div>
                </div>
      </div>
        </div>
      
  </div>
  <div class="actions">
    <button v-if="addFlag"  type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Create'" @click="addUser()">
                    Create
                </button>
    <button v-if="editFlag" type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Update'" @click="editUserRole()">
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
      <h3>User Management </h3>
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
                   
                    
                    <button class="btn btn-sm btn-success" style="margin-bottom: 2%;marginLeft:1%" @click="showAddRole()">Add User
                                    </button>
            <table id="example" class="table table-bordered col-lg-12" align="center"  style="fontSize:14px">
              <thead align="left">
                <tr>
                  <th  scope="col">User</th>
                  <th  scope="col">Roles</th>
                  <th  align="center">Manage Roles</th>
                </tr>
              </thead>
              <tbody >
                
                <tr v-for="user in allusers" :key="user.name">
                    <td scope="col">{{user.email}}</td>
                    <td scope="col">{{user.roles}}</td>
                    <td scope="col">
                      <div class="row">
                        &nbsp&nbsp&nbsp&nbsp
                         <button class="btn btn-sm btn-primary" @click="showEditRole(user)">Manage
                          </button>&nbsp&nbsp
                          <button class="btn btn-sm btn-danger" @click="deleteRole(user)">Delete
                          </button>
                      </div>
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
import generator from "generate-password";

export default {
  name: "ManageUser",
  components: {
    SideNav,
    headernav,
    Vudal,
    Multiselect
  },
  created() {
    clearInterval(window.intervalObj);
    
     
    this.getAllUsers();
    this.getAllRoles();
    
    
  },
  data() {
    
    return {
    allusers:[],
    allPermissions:[],
    editFlag: false,
    addFlag: true,
    userId:'',
    loaderFlag:false,
    permissionValue:[],
    options: [],
    state:true,
    user:{
      username:'',
      password:'',
      email:'',
      cnf_password:''
    },
    regPass:/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/,
    reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
    };
  },
  methods: {

    stateChange() {
      this.state = !this.state;
      
    },
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
    console.log(this.options);
    this.$modals.myModal.$show();
    },
    addUser()
    {
    if(this.state)
    {
      var password = generator.generate({
    length: 8,
    numbers: true,
    symbols: true
      });
      console.log('password',password);
      this.user.password=password;
    }
    // if((this.user.password!==this.user.cnf_password)){
      if(this.reg.test(this.user.email))
      {

      if((this.regPass.test(this.user.password))||(this.state))
      {
        
          let userDate={
            email:this.user.email,
            password:this.user.password,
            username:this.user.username,
            connection:'db-users'
          }
        fetch(constant.APIURL + "api/v1/info/members/create-user", {
        method: "POST",
        body: JSON.stringify(userDate),
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token"),
          'Content-Type':'application/json'
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
            this.user.username='';
            this.user.email='';
            this.user.password='';
            this.user.cnf_password='';
            this.state=true;
            this.getAllUsers();
            this.$modals.myModal.$hide();
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
        }else{
          if(this.user.cnf_password !== this.user.password)
              {
                this.user.password='';
                this.user.cnf_password='';
                    swal({
                          title: "Info",
                          text: "Password Doesn't Match",
                          icon: "info"
                        });
            }else{
                    this.user.password='';
                    this.user.cnf_password='';
                    swal({
                          title: "Info",
                          text: "Password is too weak",
                          icon: "info"
                        });
                  }
        }
        }else{

          this.user.email='';
          swal({
                title: "Info",
                text: "Please Provide Valid Email-Id",
                icon: "info"
              });
        }
    
    // else{
     
    // }
    },

    editUserRole()
    {
    
    let formData = new FormData();
         formData.append("userId", this.userId);
    for(var i=0;i<this.permissionValue.length;i++)
    {
      formData.append("checkedRoles", this.permissionValue[i].role_id);
    }
       
        
         
        
         fetch(constant.APIURL + "api/v1/info/members/update-roles", {
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
             this.getAllUsers();
              this.$modals.myModal.$hide();
           });
         })
         .catch(handleError => {
           console.log(" Error Response ------->", handleError);
         });
    },
    deleteRole(user)
    {
console.log(user)
          swal({
            title: "Info",
            text: "Do You Want to Delete the Role ?",
            icon: "info"
          }).then(ok => {
            if (ok) {
              fetch(
                constant.APIURL +
                  "api/v1/info/members/delete-user?user_id=" +
                  user.user_id,
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
                         this.getAllUsers();
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
    showEditRole(user){
      this.editFlag=true;
      this.addFlag=false;
      this.userId=user.user_id;
     console.log(user);
      for(let i=0;i<user.role_ids.length;i++)
      {
        for(let j=0;j<this.options.length;j++)
        {
          if(user.role_ids[i] == this.options[j].role_id)
          {
            this.permissionValue.push(this.options[j]);
          }
        }
      }
      this.$modals.myModal.$show();
    },
    hideEntry(){
      this.permissionValue=[];
      this.user.username='';
      this.user.password='';
      this.user.cnf_password='';
      this.user.email='';
      this.state=true;
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
              this.options.push({
                role_name: data[i].name,
                role_id:data[i]._id,
                role_description:data[i].description
              });
            }
          // this.options=this.allRoles;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    }
    ,
    getAllUsers()
    {
      this.loaderFlag=true;
      
      this.allusers=[];
      fetch(constant.APIURL + "api/v1/info/members/get-all-user-by-group" , {
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
              this.loaderFlag=true;
              let roles='';
              let role_ids=[];
              fetch(constant.APIURL + "api/v1/info/members/get-all-roles-by-user?user_id="+data[i].user_id , {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const roleData = text && JSON.parse(text);
            if(roleData.length>0)
            {

          roles=roleData[0].name;
          role_ids.push(roleData[0]._id);
            for (let i = 1; i < roleData.length; i++) {
              this.loaderFlag=true;
              roles=roles+','+roleData[i].name;
              role_ids.push(roleData[i]._id);
            }
            }   
            console.log(role_ids);
            this.allusers.push({
                email: data[i].email,
                roles:roles,
                user_id:data[i].user_id,
                role_ids:role_ids
              });   
              this.loaderFlag=false;
             
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
        console.log('okok',roles  );
               
              
            }
            
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
