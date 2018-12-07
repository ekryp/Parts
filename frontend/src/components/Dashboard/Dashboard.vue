<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 2%">
      <div class="container">
        <div class="row-one">
          <div class="row text-center">
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Total Customer</span>
                  <br>
                  <span class="text-middle">1</span>
                </div>
                <div class="vertical"></div>
              </div>
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Critical PONs</span>
                  <br>
                  <span class="text-middle" style="color:red">6</span>
                </div>
                <div class="vertical"></div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Critical Customers</span>
                  <br>
                  <span class="text-middle" style="color:red">1</span>
                </div>
                <div class="vertical"></div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Critical Depots</span>
                  <br>
                  <span class="text-middle" style="color:red">7</span>
                </div>
                <div class="vertical"></div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Total PON types</span>
                  <br>
                  <span class="text-middle">4</span>
                </div>
                <div class="vertical"></div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Total Depots</span>
                  <br>
                  <span class="text-middle">7</span>
                </div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
          </div>
        </div>
        <div class="row-two">
          <div class="row">
            <div class="col-lg-4">
              <div class="card">
                <div class="card-header">
                  <h5>Top PONs</h5>
                </div>
                <div class="card-body">
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">PONS</th>
                        <th scope="col">Depots</th>
                        <th scope="col">Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in data.topPONs" :key="item.id">
                        <td>{{item.part_name}}</td>
                        <td>{{item.depot_name}}</td>
                        <td>{{item.count}}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-header">
                  <h5>Top Depots</h5>
                </div>
                <div class="card-body">
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">Depot</th>
                        <th scope="col">PONs Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in data.topDeptos" :key="item.id">
                        <td>{{item.depot_name}}</td>
                        <td>{{item.critical_pon_count}}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-header">
                  <h5>Top Customers</h5>
                </div>
                <div class="card-body">
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">Customer</th>
                        <th scope="col">PONs Count</th>
                        <th scope="col">Depots Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>bestel</td>
                        <td>6</td>
                        <td>7</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row-two">
          <div class="row">
            <div class="col-lg-4">
              <div class="card">
                <div class="card-body">
                  <div id="container" style="height:250px"></div>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-body">
                  <div id="container2" style="height:250px"></div>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-body">
                  <GmapMap :center="gmap.center" :zoom="2" style="width: 300px; height: 36vh"></GmapMap>
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
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import piechart from "../../utilies/piechart.json";
import linechart from "../../utilies/linechart.json";
import * as data from "../../utilies/dumpdata.json";
import Vue from "vue";
import * as VueGoogleMaps from "vue2-google-maps";
import VueGeolocation from "vue-browser-geolocation";
Vue.use(VueGeolocation);

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyAk2MMMJwyvyiAYzxIGzjIEmjWVB0Z6Vv0"
  }
});

export default {
  name: "Dashboard",
  components: {
    SideNav,
    headernav
  },
  mounted() {
    this.chartone();
    this.charttwo();
    // $(document).ready(function() {
    //   $("#example").DataTable();
    // });
  },
  created() {
    this.$getLocation({ enableHighAccuracy: true }).then(coordinates => {
      console.log("coordinates ----->", coordinates);
    });
  },
  data() {
    console.log("dashboard", this.data);
    return {
      gmap: {
        center: { lat: 16.1304, lng: 86.3468 }
      },
      data: data
    };
  },
  methods: {
    chartone() {
      Highcharts.chart("container", piechart);
    },
    charttwo() {
      Highcharts.chart("container2", linechart);
    }
  }
};
</script>
<style>
.text-top {
  font-size: 1vw;
}
.text-middle {
  font-size: 2vw;
}
.text-bottom {
  font-size: 1vw;
}
.row-one {
  padding-top: 5%;
}
.row-two {
  margin-top: 5%;
}
.vertical {
  width: 1%;
  height: 60px;
  background-color: #adb2b5;
}
.container {
  width: 100% !important;
  height: 100%;
}
.card {
  position: relative;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
  max-height: 42vh;
  min-height: 42vh;
}
.card-body {
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  padding: 1.25rem;
  overflow: auto;
}
.card-header {
  padding: 0.75rem 1.25rem;
  margin-bottom: 0;
  background-color: rgb(237, 237, 237);
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}
</style>
