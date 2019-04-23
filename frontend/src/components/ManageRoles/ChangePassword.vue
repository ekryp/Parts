<template>
<div>
<headernav msg="Dashboard"/>
    <side-nav/>


    <Loading :active="isLoading" 
        :can-cancel="false" 
        color=#15ba9a
        :is-full-page="fullPage"></Loading>

    <div>
    <div class="custom-container" style="paddingTop: 15%" align="center">


        <div class="card col-lg-6" align="center">
              <div class="card-header">
                <div class="row">
                  
                    <h5>{{changePasswordConstant.table.tableName}} </h5>
                  
                </div>
              </div>
              <div class="card-body">
                
                <div class="row" align="">
                <label class="col" for="usrname">{{changePasswordConstant.table.tableHeaders[0]}}</label>
                <input class="col"  type="password" id="usrname" v-model="new_password" required>
                </div>
                <div class="row" style="text-align:left">
                  <div class="col"></div>
                  <div class="col">
                   <p style="font-size: 11px;"> *Password Constraints
                  <br>Allowed special characters (!@#$%^&*)
                  <br>Lower case (a-z), upper case (A-Z) and numbers (0-9)
                  <br>Length should be greater than 8 
                </p>
                </div>
                </div>
                
                <div class="row">
                <label for="psw" class="col">{{changePasswordConstant.table.tableHeaders[1]}} </label>
                <input class="col" type="password" id="psw" name="psw" v-model="cnrf_password"  required>
                
                </div>
                <br>
                <input type="submit" value="Submit" @click="changePass()" class="btn btn-success">
                &nbsp&nbsp&nbsp&nbsp  
                <input type="submit" value="Cancel" @click="routeDashboard()" class="btn btn-danger">
              </div>
            </div>
        </div>
      
  </div>
  <div>
      <!-- Footer -->
      <footer class="footer fixed-bottom font-small blue">
        <!-- Copyright -->
        <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
        <!-- Copyright -->
      </footer>
      <!-- Footer -->
    </div>
</div>
</div>
</template>
<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";
import swal from "sweetalert";
//import * as data from "../../utilies/tabledata.json";
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: "ChangePassword",
  components: {
    SideNav,
    headernav,
    Loading
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
    isLoading: false,
     cnrf_password:"",
     new_password:"",
     changePasswordConstant:constant.ChangePasswordScreen
    };
  },
  methods: {
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    routeDashboard(){
      router.push("/");
    },
    changePass()
    {
      this.isLoading=true;
      var isSocial=localStorage.getItem('isSocial');
      if((this.new_password !== '' )&&(this.cnrf_password !== ''))
      {
      if(isSocial=='false')
      {
      var user_id=localStorage.getItem('user_id');
      let formData = new FormData();
      if(this.new_password === this.cnrf_password)
      {
        formData.append("user_id", user_id);
        formData.append("new_password", this.new_password);
        console.log(formData);
        fetch(constant.APIURL + "api/v1/reset_password", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
        }
      })
        .then(response => {
          response.text().then(text => {
            this.isLoading=false;
            const data = text && JSON.parse(text);
            if(data.code === "token_expired")
            {
              this.logout();
            }
           if (data.http_status_code === 200) {
              this.cnrf_password="";
              this.new_password="";
              swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              }).then(ok => {
                if (ok) {
                 router.push("/dashboard");
                  }
              });
            } else {
              this.cnrf_password="";
            this.new_password="";
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
      }else
      {
        this.isLoading=false;
        swal({
              title: "Info",
              text: "Password Entered in Both the Fields are Different",
              icon: "error"
            });
            this.cnrf_password="";
            this.new_password="";
      }
    }
    else{
      this.isLoading=false;
      swal({
              title: "Info",
              text: "You logged in through social account ,We can't change your password",
              icon: "error"
            });
            this.cnrf_password="";
            this.new_password="";
    }
    }
    else{
       swal({
              title: "Info",
              text: "New Password and Confirm Password can't be empty",
              icon: "error"
            });
    }
    }
  }
};
</script>
<style>

</style>
