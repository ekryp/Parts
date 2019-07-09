<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>

    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>

    <vudal name="myModal">
      <div class="header">
        <i class="close icon"></i>
        <h4 v-if="editFlag">Manage Roles</h4>
        <h4 v-if="addFlag">Create User</h4>
      </div>
      <div class="content">
        <div class="form-group text-left">
          <Loading :active="isLoading" :can-cancel="false" color="#15ba9a" :is-full-page="fullPage"></Loading>
          <div v-if="editFlag">
            <br>
            <div class="row">
              <label for="psw" class="col-lg-3">Permissions :</label>
            </div>
            <br>
            <Multiselect
              v-model="permissionValue"
              tag-placeholder="Add this as new tag"
              placeholder="Search  a Permission"
              label="role_name"
              track-by="role_id"
              :options="options"
              :multiple="true"
              :close-on-select="false"
              :clear-on-select="false"
              :hide-selected="true"
            ></Multiselect>
          </div>
          <div v-if="addFlag">
            <div class="row align">
              <label class="col-lg-5" for="usrname">Username * :</label>
              <div class="col-lg-7">
                <input
                  class="form-control"
                  type="text"
                  id="usrname"
                  v-model="user.username"
                  placeholder="Enter the Username"
                >
              </div>
            </div>
            <div class="row align">
              <label class="col-lg-5" for="email">Email * :</label>
              <div class="col-lg-7">
                <input
                  class="form-control"
                  type="text"
                  id="email"
                  v-model="user.email"
                  placeholder="Enter the E-mail"
                >
              </div>
            </div>
            <div class="row align">
              <div class="col-lg-5">
                <p>Auto Generate Password</p>
              </div>
              <div class="col-lg-7">
                <toggle-button
                  :value="state"
                  :color="{checked: 'green', unchecked: 'grey'}"
                  :sync="true"
                  cssColors:true
                  :labels="{checked: 'On', unchecked: 'off'}"
                  :width="80"
                  v-tooltip.top.hover.focus="'Click to Toggle'"
                  @change="stateChange()"
                />
              </div>
            </div>
            <div class="row align" v-if="!state">
              <label class="col-lg-5" for="password">Password * :</label>
              <div class="col-lg-7">
                <input
                  class="form-control"
                  type="password"
                  id="password"
                  v-model="user.password"
                  placeholder="Enter the Password"
                >
              </div>
              <div class="col-lg-5"></div>
              <div class="col-lg-7" style="margin-top:6px;">
                <p style="font-size: 11px;">
                  *Password Constraints
                  <br>Allowed special characters (!@#$%^&*)
                  <br>Lower case (a-z), upper case (A-Z) and numbers (0-9)
                  <br>Length should be greater than 8
                </p>
              </div>
            </div>
            <div class="row align" v-if="!state">
              <label class="col-lg-5" for="password">Confirm Password * :</label>
              <div class="col-lg-7">
                <input
                  class="form-control"
                  type="password"
                  id="password"
                  v-model="user.cnf_password"
                  @change="checkPassword()"
                  placeholder="Re-Enter the Password"
                >
              </div>
            </div>
            <div class="row align" v-if="errorMessage !==''">
              <div class="col-lg-10 alert alert-danger" align="center">
                <strong>Warning!</strong>
                &nbsp;&nbsp;&nbsp;{{errorMessage}}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="actions">
        <button
          v-if="addFlag"
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Create'"
          @click="addUser()"
        >Create</button>

        <button
          v-if="editFlag"
          type="button"
          class="btn btn-success"
          v-tooltip.top.hover.focus="'Click to Update'"
          @click="editUserRole()"
        >Update</button>
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
          <h3>{{userConstants.pageHeader}}</h3>
        </div>
      </div>
      <br>
      <br>
      <div class="row">
        <div class="col-lg-12">
          <div class="p-3 mb-5 bg-white">
            <h5 class="gridTitle col-lg-12" style="marginLeft:-1%">{{userConstants.table.tableName}}</h5>
            <br>

            <div class="row">
              <div class="col-lg-6">
                <button
                  class="btn btn-sm btn-success"
                  style="margin-bottom: 2%;marginLeft:1%"
                  @click="showAddRole()"
                >{{userConstants.addButton}}</button>
              </div>
              <div class="col-lg-6">
                <el-col :span="12" class="float-right">
                  <el-input placeholder="Search " v-model="filters[0].value"></el-input>
                </el-col>
              </div>
            </div>

            <div class="table-responsive">
              <data-tables :data="allusers" :filters="filters">
                <el-table-column
                  v-for="title in titles"
                  :prop="title.prop"
                  :label="title.label"
                  :key="title.prop"
                  sortable="custom"
                ></el-table-column>
                <el-table-column align="right">
                  <template slot-scope="scope">
                    <el-button size="mini" @click="showEditRole(scope.row)">Edit</el-button>
                    <el-button size="mini" type="danger" @click="deleteRole(scope.row)">Delete</el-button>
                  </template>
                </el-table-column>
              </data-tables>
            </div>
          </div>
        </div>
      </div>
      <!-- </div> -->
    </div>
    <div>
      <!-- Footer -->
      <footer class="footer font-small blue">
        <!-- Copyright -->
        <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
        <!-- Copyright -->
      </footer>
      <!-- Footer -->
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
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import { DataTables, DataTablesServer } from "vue-data-tables";
import Vue from "vue";
import lang from "element-ui/lib/locale/lang/en";
import locale from "element-ui/lib/locale";

locale.use(lang);

Vue.use(DataTables);
Vue.use(DataTablesServer);
Vue.use(ElementUI);

export default {
  name: "ManageUser",
  components: {
    SideNav,
    headernav,
    Vudal,
    Multiselect,
    Loading
  },
  created() {
    clearInterval(window.intervalObj);

    this.getAllUsers();
    this.getAllRoles();
  },
  data() {
    return {
      isLoading: false,
      fullPage: true,
      userConstants: constant.UserManagementScreen,
      allusers: [],
      errorMessage: "",
      allPermissions: [],
      editFlag: false,
      addFlag: true,
      userId: "",
      loaderFlag: false,
      permissionValue: [],
      ekrypUserOptions:[],
      otherUserOptions:[],
      options: [],
      filters: [
        {
          prop: ["roles", "username", "email"],
          value: ""
        }
      ],
      state: true,
      titles: [
        {
          prop: "email",
          label: "User Mail Id."
        },
        {
          prop: "username",
          label: "Username"
        },
        {
          prop: "roles",
          label: "Roles"
        }
      ],
      user: {
        username: "",
        password: "",
        email: "",
        cnf_password: ""
      },

      regPass: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_])[A-Za-z\d@$!%*?&_]{8,}$/,
      reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
    };
  },
  methods: {
    checkPassword() {
      if (this.user.cnf_password !== this.user.password) {
        this.user.password = "";
        this.user.cnf_password = "";
        swal({
          title: "Info",
          text: "Password Doesn't Match",
          icon: "info"
        });
      }
    },
    stateChange() {
      this.state = !this.state;
    },
    addTag(newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor(Math.random() * 10000000)
      };
      console.log(tag);
      this.options.push(tag);
      this.value.push(tag);
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    showAddRole() {
      this.permissionValue = [];
      this.user.username = "";
      this.user.password = "";
      this.user.cnf_password = "";
      this.user.email = "";
      this.state = true;
      this.errorMessage = "";
      this.editFlag = false;
      this.addFlag = true;
      console.log(this.options);
      this.$modals.myModal.$show();
    },
    addUser() {
      this.isLoading = true;
      if (this.state) {
        var password = generator.generate({
          length: 8,
          numbers: true,
          symbols: true,
          strict: true
        });
        console.log("password", password);
        this.user.password = password;
      }
      // if((this.user.password!==this.user.cnf_password)){
      if (this.reg.test(this.user.email.trim()) && this.user.username !== "") {
        if (this.regPass.test(this.user.password) || this.state) {
          let userDate = {
            email: this.user.email.trim(),
            password: this.user.password,
            username: this.user.username,
            connection: "db-users"
          };
          fetch(constant.APIURL + "api/v1/info/members/create-user", {
            method: "POST",
            body: JSON.stringify(userDate),
            headers: {
              Authorization:
                "Bearer " + localStorage.getItem("auth0_access_token"),
              "Content-Type": "application/json"
            }
          })
            .then(response => {
              response.text().then(text => {
                const data = text && JSON.parse(text);
                if (data.code === "token_expired") {
                  this.logout();
                }
                if (data.http_status_code === 200) {
                  this.isLoading = false;
                  swal({
                    title: "SUCCESS",
                    text: data.msg,
                    icon: "success"
                  }).then(ok => {
                    if (ok) {
                      this.user.username = "";
                      this.user.email = "";
                      this.user.password = "";
                      this.user.cnf_password = "";
                      this.state = true;
                      this.getAllUsers();
                      this.$modals.myModal.$hide();
                    }
                  });
                } else {
                  this.isLoading = false;
                  this.errorMessage = data.msg;
                }
                console.log("data -- response-->", data);
              });
            })
            .catch(handleError => {
              console.log(" Error Response ------->", handleError);
            });
        } else {
          this.user.password = "";
          this.user.cnf_password = "";
          swal({
            title: "Info",
            text: "Password is too weak",
            icon: "info"
          });
        }
      } else {
        this.user.password = "";
        if (this.user.username === "") {
          swal({
            title: "Info",
            text: "Please Enter the UserName",
            icon: "info"
          });
        } else if (this.user.email === "") {
          swal({
            title: "Info",
            text: "Please Enter the Email-Id",
            icon: "info"
          });
        } else {
          this.user.email = "";
          swal({
            title: "Info",
            text: "Please Provide Valid Email-Id",
            icon: "info"
          });
        }
      }

      // else{

      // }
    },

    editUserRole() {
      this.isLoading = true;

      let formData = new FormData();
      formData.append("userId", this.userId);
      for (var i = 0; i < this.permissionValue.length; i++) {
        if (this.permissionValue[i].role_name === "EditReference") {
          formData.append(
            "checkedRoles",
            "b3b2d5d2-badf-4473-90b0-5e50f65f5b1a"
          );
        }
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
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
              this.isLoading = false;
              swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              }).then(ok => {
                if (ok) {
                  this.permissionValue = [];
                  this.getAllUsers();
                  this.$modals.myModal.$hide();
                }
              });
            } else {
              this.isLoading = false;
              this.errorMessage = data.msg;
            }
            console.log("data -- response-->", data);
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    deleteRole(user) {
      swal({
        title: "Info",
        text: "Do You Want to Delete the User ?",
        icon: "info"
      }).then(ok => {
        if (ok) {
          this.isLoading = true;
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
                  this.isLoading = false;
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
    showEditRole(user) {
      this.editFlag = true;
      this.addFlag = false;
      this.permissionValue=[];
      this.userId = user.user_id;
      console.log(user.email);
      this.options=[];
      if(user.email.includes('ekryp'))
      {
        console.log(user);
        this.options=this.ekrypUserOptions;
      }
      else{
        this.options=this.otherUserOptions;
      }
      console.log(this.options);
      for (let i = 0; i < user.role_ids.length; i++) {
        for (let j = 0; j < this.options.length; j++) {
          if (user.role_ids[i] == this.options[j].role_id) {
            this.permissionValue.push(this.options[j]);
          }
        }
      }
      this.$modals.myModal.$show();
    },
    hideEntry() {
      this.permissionValue = [];
      this.user.username = "";
      this.user.password = "";
      this.user.cnf_password = "";
      this.user.email = "";
      this.state = true;
      this.$modals.myModal.$hide();
    },
    showModal() {
      this.$modals.myModal.$show();
    },
    getAllRoles() {
      this.allRoles = [];
      fetch(constant.APIURL + "api/v1/info/members/all-role", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            console.log("data -- get_top_extended-->", data);
            //this.allRoles = data;
            for (let i = 0; i < data.length; i++) {
              
              if(data[i]._id === '47eca0a9-b77d-4666-85bf-93df15d5ca11' && data[i].name === 'EkrypUser')
              {
                this.ekrypUserOptions.push({
                role_name: data[i].name,
                role_id: data[i]._id,
                role_description: data[i].description
              });
              }
              else{
              this.otherUserOptions.push({
                role_name: data[i].name,
                role_id: data[i]._id,
                role_description: data[i].description
              });
              }
            }
            this.ekrypUserOptions =this.ekrypUserOptions.concat(this.otherUserOptions);
            console.log('Ekryp Users',this.ekrypUserOptions);
            console.log('Other Users',this.otherUserOptions);

            // this.options=this.allRoles;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    getAllUsers() {
      this.isLoading = true;
      fetch(constant.APIURL + "api/v1/info/members/get-all-user-by-group", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            let array = [];
            console.log("All users --length--->", this.allusers.length);
            data.forEach(function(doc) {
              let rolesString = "";
              let roleId = [];
              doc.roles.forEach(function(role) {
                rolesString += role.name + ",";
                roleId.push(role._id);
              });
              rolesString = rolesString.substring(0, rolesString.length - 1);

              let object = {
                email: doc.email,
                username: doc.username,
                user_id: doc.user_id,
                roles: rolesString,
                role_ids: roleId
              };
              array.push(object);
            });
            this.allusers = array;
            console.log("All users -- ------->", this.allusers.length);
            if (array.length > 0) {
              $(document).ready(function() {
                $("#userdata").DataTable();
              });
            }
            this.isLoading = false;
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
/* @media all and (max-width: 720px) and (min-width: 600px) {
    body{
        font-size: 13px;
    }
} */

.align {
  padding: 6px;
}
</style>
