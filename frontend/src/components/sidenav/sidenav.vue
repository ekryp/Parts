<template>
    <div>
      <div class="header">
        <div class="sidenav">
         <div class="sidenav-header">
            <div style="marginLeft: 20%; marginTop: 10%">
             <img src="http://portal.ekryp.com/src/assets/ekryp.jpg" width="60%" />
            </div>
          </div>
          <div class="menu">
            <div class="menulist">
            <router-link  active-class="active" to="/dashboard" style="color:white" >
                <i class="fas fa-tachometer-alt" style="marginRight: 5%; marginLeft: 5%"></i> 
                <span>Dashboard</span>
            </router-link>
            </div>
               <div class="menulist" @click="Parts()">
                <span><i class="fas fa-toolbox" style="marginRight: 5%; marginLeft: 5%"></i> Parts Prediction</span>
                <span v-if="partsClose"><i class="fas fa-caret-down drop-menu "></i></span>
                <span v-if="!partsClose"><i  class="fas fa-caret-right drop-menu "></i></span>
              </div>
              <div v-if="showPartsChild" class="menulist-child">
                 <router-link  active-class="active" to="/parts/analysis/dashboard" style="color:white" >
                  <i  class="fas fa-chart-line" style="marginRight: 5%; marginLeft: 5%"></i> 
                  <span>Dashboard</span>
                </router-link><br/>
              </div>
               <div v-if="showPartsChild" class="menulist-child">
                 <router-link  active-class="active" to="/parts/analysis/create" style="color:white" >
                  <i  class="fas fa-plus" style="marginRight: 5%; marginLeft: 5%"></i> 
                  <span>Create Analysis</span>
                </router-link><br/>
              </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import router from "../../router";
export default {
  name: "SideNav",
  props: ["menu"],
  data() {
    console.log("props", this.$props);
    return {
      partsClose: true,
      showPartsChild: false
    };
  },
  beforeMount() {
    if (this.$props.menu === "analysis") {
      this.showPartsChild = true;
    }
  },
  methods: {
    Parts() {
      this.partsClose = !this.partsClose;
      this.showPartsChild = !this.showPartsChild;
    },
    dashboard() {
      router.push("/dashboard");
    },
    parts_analysis() {
      router.push("/parts/analysis");
    }
  }
};
</script>
<style>
.active {
  border-left: 5px solid green !important;
  color: white;
}
.sidenav {
  position: fixed;
  height: 700px;
  width: 20%;
  background-color: #293f55;
}
.header {
}
.sidenav-header {
}
.menu {
  margin-top: 10%;
}

.menulist:hover {
  background-color: #4d9e34;
  height: 50px;
  width: 100%;
  color: white;
  cursor: pointer;
}
.menulist {
  width: 100%;
  padding: 5%;
  color: white;
  cursor: pointer;
}
.menu-toptext {
  margin-top: 10%;
}
.drop-menu {
  font-size: 16px;
  float: right;
  margin-top: 4px;
  margin-right: 20px;
}
.menulist-child {
  padding: 5%;
  padding-left: 10%;
  font-size: 1.15vw;
  color: white;
  cursor: pointer;
}

.menulist-child:hover {
  background-color: #4d9e34;
  padding: 5%;
  padding-left: 10%;
  font-size: 1.15vw;
  color: white;
  cursor: pointer;
}

.menulist-child:active {
  background-color: #4d9e34;
  padding: 5%;
  padding-left: 10%;
  font-size: 1.15vw;
  color: white;
  cursor: pointer;
}
</style>
