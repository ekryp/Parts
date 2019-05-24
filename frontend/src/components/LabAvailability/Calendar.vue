<template>
<div>
<headernav msg="Dashboard"/>
    <side-nav/>


    <Loading :active="isLoading" 
        :can-cancel="false" 
        color=#15ba9a
        :is-full-page="fullPage"></Loading>

    <div>
    <div class="custom-container" style="paddingTop: 4%" align="center">
    <p>This is new page</p>
    <div class="row">
    <div class="col-lg-4">
    <br>
    <br>
    <br>
        <div class="row" align="left">
            <label class="col-lg-3" for="usrname">Title :</label>
            <input class="col-lg-9"  type="password" id="usrname" required>
        </div>
    <br>
        <div class="row" align="left">
                <label class="col-lg-3" for="usrname">Start Time :</label>
                <input class="col-lg-9"  type="password" id="usrname" required>
        </div>
    <br>
        <div class="row" align="left">
                <label class="col-lg-3" for="usrname">End Time :</label>
                <input class="col-lg-9"  type="password" id="usrname" required>
        </div>
     <br>
        <div class="row" align="left">
                <label class="col-lg-3" for="usrname">Participants :</label>
                <input class="col-lg-9"  type="password" id="usrname" required>
        </div>
        <br>
         <br>
                <input type="submit" value="Submit"  class="btn btn-success">
                &nbsp&nbsp&nbsp&nbsp  
                <input type="submit" value="Cancel" class="btn btn-danger">
   </div>
    <div class="col-lg-8">
    <iframe src="https://calendar.google.com/calendar/embed?src=nageshwara.vijay%40ekryp.com&ctz=Asia%2FKolkata" style="border: 0" width="90%" height="600" frameborder="0" scrolling="no"></iframe>
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
import FullCalendar from 'vue-fullcalendar';

export default {
     props: ['events'],
    
  name: "ChangePassword",
  components: {
    SideNav,
    headernav,
    Loading,
      FullCalendar
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
    
   
  }
};
</script>
<style>

</style>
