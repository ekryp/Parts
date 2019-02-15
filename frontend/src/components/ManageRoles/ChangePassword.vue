<template>
<div>
<headernav msg="Dashboard"/>
    <side-nav/>

    
    <div class="custom-container" style="paddingTop: 15%" align="center">


        <div class="card col-lg-6" align="center">
              <div class="card-header">
                <div class="row">
                  
                    <h5>Change Password </h5>
                  
                </div>
              </div>
              <div class="card-body">
                
                <div class="row" align="">
                <label class="col" for="usrname">New Password :</label>
                <input class="col"  type="password" id="usrname" v-model="new_password" required>
                </div>
                <br>
                <div class="row">
                <label for="psw" class="col">Confirm Password : </label>
                <input class="col" type="password" id="psw" name="psw" v-model="cnrf_password"  required>
                </div>
                <br>
                <input type="submit" value="Cancel" @click="changePass()" class="btn btn-success">
                &nbsp&nbsp&nbsp&nbsp  
                <input type="submit" value="Submit" @click="changePass()" class="btn btn-success">
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
import * as constant from "../constant/constant";
import swal from "sweetalert";
//import * as data from "../../utilies/tabledata.json";

export default {
  name: "ChangePassword",
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
     cnrf_password:"",
     new_password:""
    };
  },
  methods: {
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    changePass()
    {
      var user_id=localStorage.getItem('user_id');
      let formData = new FormData();
      if(this.new_password === this.cnrf_password)
      {
        formData.append("user_id", user_id);
        formData.append("new_password", this.new_password);
        console.log(localStorage.getItem('user_id'));
        fetch(constant.APIURL + "api/v1/reset_password", {
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
            console.log("data -- response-->", data);
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      }else
      {
        swal({
              title: "Info",
              text: "Password Entered in Both the Fields are Different",
              icon: "error"
            });
            this.cnrf_password="";
            this.new_password="";
      }
    }
    
  }
};
</script>
<style>

</style>
