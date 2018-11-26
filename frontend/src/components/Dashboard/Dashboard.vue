<template>
  <div>
    <headernav msg="Dashboard"/>
    <side-nav />
    <div class="custom-container" style="paddingTop: 2%">
      <div class="container">
        <div class="row-one">
          <div class="row">
            <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
             <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
             <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
             <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
             <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
             <div class="col-lg-2">
              <span class="text-top">Active Assets Added</span>
              <span class="text-middle">78</span><br/>
              <span class="text-bottom">+76.00 Mar-Apr</span>
            </div>
          </div>
        </div>
        <div class="row-two">
          <div class="row">
            <div class="col-lg-6">
          <div class="card">
  <div class="card-body">
    <canvas id="myChart" width="400" height="400"></canvas>
  </div>
</div>
</div>
  <div class="col-lg-6">
          <div class="card">
  <div class="card-body">
    <canvas id="myChart2" width="400" height="400"></canvas>
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
    <!-- <canvas id="myChart" width="400" height="400"></canvas> -->
  </div>
</div>
</div>
  <div class="col-lg-6">
          <div class="card">
  <div class="card-body">
   <!-- <canvas id="myChart" width="400" height="400"></canvas> -->
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

export default {
  name: "Dashboard",
  components: {
    SideNav,
    headernav
  },
  mounted() {
    this.chartone();
  },
  data() {
    console.log("dashboard");
    return {};
  },
  methods: {
    chartone() {
      var ctx = document.getElementById("myChart").getContext("2d");
      var ctx2 = document.getElementById("myChart2").getContext("2d");
      var myChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
          datasets: [
            {
              label: "# of Votes",
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)"
              ],
              borderColor: [
                "rgba(255,99,132,1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)"
              ],
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true
                }
              }
            ]
          }
        }
      });
      var myChart = new Chart(ctx2, {
        type: "bar",
        data: {
          labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
          datasets: [
            {
              label: "# of Votes",
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)"
              ],
              borderColor: [
                "rgba(255,99,132,1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)"
              ],
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true
                }
              }
            ]
          }
        }
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
</style>
