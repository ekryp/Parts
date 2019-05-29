<template>
  <div>
    <headernav msg="Spare Part Analysis"/>
    <side-nav menu="analysis"/>
    <div class="custom-container" style="paddingTop:3%">
      <!-- <div class="container"> -->
      <form style="marginTop: 5%;">
        <div>
          <div class="myBreadCrumb">
            <p>
              <span style="font-size: 14px;">{{LabAnalysisConstant.breadcrumbs[0]}}</span>
            </p>
          </div>
        </div>

        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[0]}}</label>
            </div>
            <div class="col-lg-4">
              <input
                type="text"
                class="form-control"
                :placeholder="LabAnalysisConstant.labPlaceHolders[0]"
                v-model="labData.title"
              >
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[1]}}</label>
            </div>
            <div class="col-lg-4">
              <multiselect
                v-model="labData.lab_resource"
                label="name"
                :placeholder="LabAnalysisConstant.labPlaceHolders[1]"
                :options="labOptions"
                :multiple="false"
              ></multiselect>
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[2]}}</label>
            </div>
            <div class="col-lg-4">
              <date-picker
                style="height:40px;paddingTop:1.1em;width:100%"
                v-model="labData.requested_date"
                lang="en"
                value-type="format"
                format="MM/DD/YYYY"
                :first-day-of-week="1"
                confirm
              ></date-picker>
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[6]}}</label>
            </div>

            <div class="col-lg-4">
              <date-picker
                style="height:40px;paddingTop:1.1em;width:100%"
                v-model="labData.start_time"
                value-type="format"
                lang="en"
                type="time"
                format="HH:mm"
                placeholder="Select Time"
                confirm
              ></date-picker>
            </div>
          </div>
        </div>
        <br>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[3]}}</label>
            </div>

            <div class="col-lg-4">
              <date-picker
                style="height:40px;paddingTop:1.1em;width:100%"
                v-model="labData.end_time"
                value-type="format"
                lang="en"
                type="time"
                format="HH:mm"
                placeholder="Select Time"
                confirm
              ></date-picker>
            </div>
          </div>
        </div>
        <br>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[4]}}</label>
            </div>
            <div class="col-lg-4">
              <multiselect
                v-model="labData.type"
                label="name"
                :placeholder="LabAnalysisConstant.labPlaceHolders[4]"
                :options="requestTypeOptions"
                :multiple="false"
              ></multiselect>
            </div>
          </div>
        </div>
        <br>
        <div class="form-group">
          <div class="row">
            <div class="col-lg-4">
              <label>{{LabAnalysisConstant.labLabels[5]}}</label>
            </div>
            <div class="col-lg-4">
              <b-form-textarea
                id="textarea"
                class="textOverlay"
                v-model="labData.description"
                :placeholder="LabAnalysisConstant.labPlaceHolders[5]"
                rows="3"
                max-rows="10"
              ></b-form-textarea>
            </div>
          </div>
        </div>
        <div class="float-right" style="marginBottom:5%">
          <div class="row">
            <button
              type="button"
              class="btn btn-danger"
              v-tooltip.top.hover.focus="'Move to Analysis Dashboard'"
            >{{LabAnalysisConstant.buttons[0]}}</button>
            &nbsp; &nbsp;
            <button
              type="button"
              class="btn btn-success"
              v-tooltip.top.hover.focus="'Click to Submit'"
              @click="compareDates()"
            >{{LabAnalysisConstant.buttons[1]}}</button>
          </div>
        </div>
      </form>
      <!-- </div> -->
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
</template>
<script>
import Vue from "vue";
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import Multiselect from "vue-multiselect";

import { mapState, mapActions } from "vuex";
import * as constant from "../constant/constant";
import swal from "sweetalert";
import * as sampleBomData from "../../utilies/sampleBOM.txt";
import DatePicker from "vue2-datepicker";

export default {
  name: "CreateAnalysis",

  created() {
    clearInterval(window.intervalObj);
    this.labData.created_by = localStorage.getItem("email_id");
    console.log("created");
  },
  components: {
    SideNav,
    Multiselect,
    DatePicker,
    headernav
  },
  computed: {},
  data() {
    console.log("Parts-Analysis", this.$store.state);
    return {
      LabAnalysisConstant: constant.LabScreen,
      labData: {
        description: "",
        loaderFlag: false,
        requested_date: "",
        start_time: "",
        end_time: "",
        type: "",
        title: "",
        lab_resource: "",
        created_by: ""
      },

      labOptions: [
        {
          name: "Lab 1"
        },
        {
          name: "Lab 2"
        },
        {
          name: "Lab 3"
        },
        {
          name: "Lab 4"
        }
      ],
      requestTypeOptions: [
        {
          name: "Read Only"
        },
        {
          name: "Full Admin"
        }
      ]
    };
  },
  methods: {
    compareDates() {
      var x = new Date(this.labData.startDate);
      var y = new Date(this.labData.endDate);
      console.log(this.labData.lab_resource);
      if (
        this.labData.title !== "" &&
        (this.labData.lab_resource !== "" &&
          this.labData.lab_resource !== null) &&
        (this.labData.type !== "" && this.labData.type !== null) &&
        this.labData.start_time !== "" &&
        this.labData.end_time !== "" &&
        this.labData.requested_date !== ""
      ) {
        if (this.labData.startTime < this.labData.endTime) {
          this.postRequestLab();
        } else {
          swal({
            title: "info",
            text: "The End Time of Meeting is Before the Start Time",
            icon: "info"
          });
        }
      } else {
        swal({
          title: "info",
          text: "Please Fill All the Form Details.",
          icon: "info"
        });
      }
    },
    postRequestLab() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append("title", this.labData.title);
      formData.append("lab_resource", this.labData.lab_resource.name);
      formData.append("requested_date", this.labData.requested_date);
      formData.append("start_time", this.labData.start_time);
      formData.append("type", this.labData.type.name);
      formData.append("end_time", this.labData.end_time);
      formData.append("description", this.labData.description);
      formData.append("created_by", this.labData.created_by);

      console.log(this.labData);

      fetch(constant.APIURL + "api/v1/lab/request", {
        method: "POST",
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
                  this.routeToLab();
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
    routeToLab() {
      router.push("/lab");
    },
    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    }
  }
};
</script>
<style>
.file {
  cursor: pointer;
}
.nav-custom {
  padding-top: 20px rem !important;
}
.dot {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
.dot-green {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: green;
  border-radius: 50%;
  display: inline-block;
}
.line {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: #bbb;
  display: inline-block;
}
.line-green {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: green;
  display: inline-block;
}
.line-red {
  height: 10px;
  width: 84%;
  margin-bottom: 8%;
  background-color: red;
  display: inline-block;
}
.dot-red {
  height: 50px;
  width: 50px;
  margin-left: -8%;
  background-color: red;
  border-radius: 50%;
  display: inline-block;
}
.in-progress {
  cursor: pointer;
  font-size: 14px;
}
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}
.form_wizard .stepContainer {
  display: block;
  position: relative;
  margin: 0;
  padding: 0;
  border: 0 solid #ccc;
  overflow-x: hidden;
}
.wizard_horizontal ul.wizard_steps {
  display: table;
  list-style: none;
  position: relative;
  width: 100%;
  margin: 0 0 20px;
}
.wizard_horizontal ul.wizard_steps li {
  display: table-cell;
  text-align: center;
}
.wizard_horizontal ul.wizard_steps li a,
.wizard_horizontal ul.wizard_steps li:hover {
  display: block;
  position: relative;
  -moz-opacity: 1;
  filter: alpha(opacity=100);
  opacity: 1;
  color: #666;
}
.wizard_horizontal ul.wizard_steps li a:before {
  content: "";
  position: absolute;
  height: 4px;
  background: #ccc;
  top: 20px;
  width: 100%;
  z-index: 4;
  left: 0;
}
.wizard_horizontal ul.wizard_steps li a.disabled .step_no {
  background: #ccc;
}
.wizard_horizontal ul.wizard_steps li a .step_no {
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 100px;
  display: block;
  margin: 0 auto 5px;
  font-size: 16px;
  text-align: center;
  position: relative;
  z-index: 5;
}
.wizard_horizontal ul.wizard_steps li a.selected:before,
.step_no {
  background: #34495e;
  color: #fff;
}
.wizard_horizontal ul.wizard_steps li a.done:before,
.wizard_horizontal ul.wizard_steps li a.done .step_no {
  background: #1abb9c;
  color: #fff;
}
.wizard_horizontal ul.wizard_steps li:first-child a:before {
  left: 50%;
}
.wizard_horizontal ul.wizard_steps li:last-child a:before {
  right: 50%;
  width: 50%;
  left: auto;
}
.overlay {
  background-color: #efefef;
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 1000;
  top: 0px;
  left: 0px;
  opacity: 0.5; /* in FireFox */
  filter: alpha(opacity=50); /* in IE */
}
</style>
