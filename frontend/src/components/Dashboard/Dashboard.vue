<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 2%">
      <div class="container">
        <div class="row-one">
          <div class="row">
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Total Customer</span>
                  <br>
                  <span class="text-middle">78</span>
                </div>
                <div class="vertical"></div>
              </div>
            </div>
            <div class="col-lg-2">
              <div class="row">
                <div class="col-lg-10">
                  <span class="text-top">Critical PONs</span>
                  <br>
                  <span class="text-middle">78</span>
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
                  <span class="text-middle">78</span>
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
                  <span class="text-middle">78</span>
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
                  <span class="text-middle">78</span>
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
                  <span class="text-middle">78</span>
                </div>
              </div>
              <!-- <span class="text-bottom">+76.00 Mar-Apr</span> -->
            </div>
          </div>
        </div>
        <div class="row-two">
          <div class="row">
            <div class="col-lg-6">
              <div class="card">
                <div class="card-body">
                  <div id="container" style="height:250px"></div>
                </div>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="card">
                <div class="card-body">
                  <div id="container2" style="height:250px"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row-two">
          <div class="row">
            <div class="col-lg-6">
              <div class="card">
                <div class="card-body">
                  <div id="container3" style="height:250px"></div>
                </div>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="card">
                <div class="card-body">
                  <div id="container4" style="height:250px"></div>
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

export default {
  name: "Dashboard",
  components: {
    SideNav,
    headernav
  },
  mounted() {
    this.chartone();
    this.charttwo();
    this.chartthree();
  },
  data() {
    console.log("dashboard");
    return {};
  },
  methods: {
    chartone() {
      Highcharts.chart("container", piechart);
    },
    charttwo() {
      Highcharts.chart("container2", linechart);
    },
    chartthree() {
      Highcharts.chart("container3", {
        chart: {
          type: "spline",
          animation: Highcharts.svg, // don't animate in old IE
          marginRight: 10,
          events: {
            load: function() {
              // set up the updating of the chart each second
              var series = this.series[0];
              setInterval(function() {
                var x = new Date().getTime(), // current time
                  y = Math.random();
                series.addPoint([x, y], true, true);
              }, 1000);
            }
          }
        },

        time: {
          useUTC: false
        },

        title: {
          text: ""
        },
        xAxis: {
          type: "datetime",
          tickPixelInterval: 150
        },
        yAxis: {
          title: {
            text: "Value"
          },
          plotLines: [
            {
              value: 0,
              width: 1,
              color: "#808080"
            }
          ]
        },
        tooltip: {
          headerFormat: "<b>{series.name}</b><br/>",
          pointFormat: "{point.x:%Y-%m-%d %H:%M:%S}<br/>{point.y:.2f}"
        },
        legend: {
          enabled: false
        },
        exporting: {
          enabled: false
        },
        series: [
          {
            name: "Random data",
            data: (function() {
              // generate an array of random data
              var data = [],
                time = new Date().getTime(),
                i;

              for (i = -19; i <= 0; i += 1) {
                data.push({
                  x: time + i * 1000,
                  y: Math.random()
                });
              }
              return data;
            })()
          }
        ]
      });
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
</style>
