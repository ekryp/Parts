<template>
  <div class="container">
    <nav id="sidebar">
      <ul class="list-unstyled components">
        <li class="active nav-custom" style="margin-top: 40px;cursor:pointer " v-if="dashboardFlag">
          <div class="text-center" v-if="!diasableFlag" @click="dashboard()">
            <i class="fas fa-home" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.dashboardText}}</p>
          </div>
          <div class="text-center" v-if="diasableFlag">
            <i class="fas fa-home" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.dashboardText}}</p>
          </div>
        </li>
        <hr v-if="analysisFlag">
        <!-- <li class="nav-custom" style="cursor:pointer">
          <div class="text-center" @click="reference()">
            <i class="fas fa-swatchbook" style="fontSize:20px"></i>
            <br>
            <p class="upload-text">Reference</p>
          </div>
        </li>
        <hr>-->
        <li class="nav-custom" style="cursor:pointer" v-if="analysisFlag">
          <div class="text-center" v-if="!diasableFlag" @click="parts_analysis()">
            <i class="fas fa-list-ul" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.analysis}}</p>
          </div>
          <div class="text-center" v-if="diasableFlag">
            <i class="fas fa-list-ul" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.analysis}}</p>
          </div>
        </li>
        <hr v-if="createAnalysisFlag">
        <li class="nav-custom" style="cursor:pointer" v-if="createAnalysisFlag">
          <div class="text-center" @click="createPartsRequest()">
            <i class="fas fa-plus" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.createAnalysisRequest}}</p>
          </div>
        </li>
        <hr v-if="referenceDataFlag">
        <li class="nav-custom" style="cursor:pointer" v-if="referenceDataFlag">
          <div class="text-center" v-if="!diasableFlag" @click="reference()">
            <i class="fas fa-file-alt" style="fontSize:2em"></i>

            <br>
            <p class="upload-text">{{sidanavConstants.referenceData}}</p>
          </div>
          <div class="text-center" v-if="diasableFlag">
            <i class="fas fa-file-alt" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.referenceData}}</p>
          </div>
        </li>
        <hr v-if="solutionFlag">
        <li class="nav-custom" style="cursor:pointer" v-if="solutionFlag">
          <div class="text-center" v-if="!diasableFlag" @click="mockup()">
            <i class="fa fa-puzzle-piece" style="fontSize:2em"></i>

            <br>
            <p class="upload-text">{{sidanavConstants.solutionPrediction}}</p>
          </div>
          <div class="text-center" v-if="diasableFlag">
            <i class="fa fa-puzzle-piece" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.solutionPrediction}}</p>
          </div>
        </li>
         <hr v-if="knowledgeMapFlag">
        <li class="nav-custom" style="cursor:pointer" v-if="knowledgeMapFlag">
          <div class="text-center" v-if="!diasableFlag" @click="knowledgeMap()">
            <i class="fa fa-dice-d6" style="fontSize:2em"></i>

            <br>
            <p class="upload-text">{{sidanavConstants.knowledgeMap}}</p>
          </div>
          <div class="text-center" v-if="diasableFlag">
            <i class="fa fa-dice-d6" style="fontSize:2em"></i>
            <br>
            <p class="upload-text">{{sidanavConstants.knowledgeMap}}</p>
          </div>
        </li>
        <hr>
      </ul>
    </nav>
  </div>
</template>

<script>
import router from "../../router";
import * as constant from "../constant/constant";
export default {
  name: "SideNav",
  props: ["menu", "diasableFlag"],
  data() {
    console.log("props", this.$props);
    return {
      sidanavConstants: constant.Sidenav,
      partsClose: true,
      showPartsChild: false,
      dashboardFlag: false,
      analysisFlag: false,
      createAnalysisFlag: false,
      referenceDataFlag: false,
      groupFlag: false,
      solutionFlag: false,
      knowledgeMapFlag:false
    };
  },
  created() {
    var authorization = localStorage.getItem("authorization");
    var groups = localStorage.getItem("groups");
    var groupList = groups.split(",");
    var permissions = authorization.split(",");
    localStorage.setItem("internalFlag", false);
    console.log(constant.PERMISSIONS[0]);
    for (var i = 0; i < groupList.length; i++) {
      console.log(groupList[i]);
      if (groupList[i] === "infinera") {
        this.groupFlag = true;
      }
    }
    if (!this.groupFlag) {
      localStorage.clear();
      router.push("/login");
    }
    for (var i = 0; i < permissions.length; i++) {
      if (permissions[i] === constant.PERMISSIONS[0]) {
        this.dashboardFlag = true;
      } else if (permissions[i] === constant.PERMISSIONS[1]) {
        this.createAnalysisFlag = true;
      } else if (permissions[i] === constant.PERMISSIONS[2]) {
        this.analysisFlag = true;
      } else if (
        permissions[i] === constant.PERMISSIONS[3] ||
        permissions[i] === constant.PERMISSIONS[4]
      ) {
        this.referenceDataFlag = true;
      } else if (permissions[i] === constant.PERMISSIONS[8]) {
        this.solutionFlag = true;
      }
      else if (permissions[i] === constant.PERMISSIONS[9]) {
        this.knowledgeMapFlag = true;
      }
      if (permissions[i] === "EditReference") {
        localStorage.setItem("editFlag", true);
      }
      if (permissions[i] === "internal") {
        localStorage.setItem("internalFlag", true);
      }
    }
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
      router.push("/parts/analysis/dashboard");
    },
    createPartsRequest() {
      router.push("/parts/analysis/create");
    },
    reference() {
      router.push("/reference");
    },
    mockup() {
      router.push("/solution");
    },
    knowledgeMap()
    {
      router.push("/knowledge");
    }
  }
};
</script>
<style>
.container {
  width: 70px;
  height: 100%;
}
.commonpart .flex-container {
  display: flex;
  flex-direction: column;
}
.body {
  background: #f8fafd;
  overflow: hidden;
}
.wrapper {
  display: flex;
  width: 100%;
}

#sidebar {
  width: 5%;
  position: fixed;
  top: 50px;
  left: 0;
  height: 100vh;
  z-index: 999;
  background: #293f55;
  color: #fff;
  transition: all 0.3s;
}

a {
  text-decoration: none;
  color: white;
}
.content {
  margin: 0 0 0 100px;
}

a:hover {
  text-decoration: none;
}

hr {
  width: 80%;
  border-color: #ffffff;
}

#content {
  background-color: #f8fafd;
  overflow: hidden !important;
  width: 100%;
  margin-top: 100px;
}

.nav-custom {
  padding-top: 20px rem !important;
}

.upload-text {
  font-size: 0.75vw;
  font-family: Arial;
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
