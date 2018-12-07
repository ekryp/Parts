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
                  <span class="text-middle">3</span>
                </div>
                <div class="vertical"></div>
              </div>
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Critical PONs</span>
                  <br>
                  <span class="text-middle">0</span>
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
                  <span class="text-middle">0</span>
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
                  <span class="text-middle">0</span>
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
                  <span class="text-middle">5</span>
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
                <div class="card-body">
                  <h5>Top PONs</h5>
                  <br>
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">PONS</th>
                        <th scope="col">Unit</th>
                        <th scope="col">Depots</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">1</th>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@mdo</td>
                      </tr>
                      <tr>
                        <th scope="row">2</th>
                        <td>Jacob</td>
                        <td>Thornton</td>
                        <td>@fat</td>
                      </tr>
                      <tr>
                        <th scope="row">3</th>
                        <td>Larry</td>
                        <td>the Bird</td>
                        <td>@twitter</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h5>Top Depots</h5>
                  <br>
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Depots</th>
                        <th scope="col">Unit</th>
                        <th scope="col">PONs</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">1</th>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@mdo</td>
                      </tr>
                      <tr>
                        <th scope="row">2</th>
                        <td>Jacob</td>
                        <td>Thornton</td>
                        <td>@fat</td>
                      </tr>
                      <tr>
                        <th scope="row">3</th>
                        <td>Larry</td>
                        <td>the Bird</td>
                        <td>@twitter</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="card">
                <div class="card-body">
                  <h5>Top Customers</h5>
                  <br>
                  <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Customer</th>
                        <th scope="col">Unit</th>
                        <th scope="col">Depots</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">1</th>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@mdo</td>
                      </tr>
                      <tr>
                        <th scope="row">2</th>
                        <td>Jacob</td>
                        <td>Thornton</td>
                        <td>@fat</td>
                      </tr>
                      <tr>
                        <th scope="row">3</th>
                        <td>Larry</td>
                        <td>the Bird</td>
                        <td>@twitter</td>
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
  },
  created() {
    this.$getLocation({ enableHighAccuracy: true }).then(coordinates => {
      console.log("coordinates ----->", coordinates);
    });
  },
  data() {
    console.log("dashboard");
    return {
      gmap: {
        center: { lat: 16.1304, lng: 86.3468 }
      }
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
</style>
