<template>
  <div style="position:fixed;marginLeft:0%;width:100%;z-index:99999;">
    <nav class="navbar navbar-expand-sm navbar-light bg-light">
      <div class="row" style="width:10%;height:3%">
        <div>
          <img :src="image" style="height:1.5em;width:7.25em;marginLeft:1em">
        </div>
      </div>
      <div class="loader" id="loader-2" style="margin-left:35%;" v-if="loaderFlag">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdownMenuLink"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              style="color:#515356; fontWeight:500"
            >
              <i class="fas fa-user"></i>
              &nbsp;{{firstName}}
            </a>

            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
              <!-- <a class="dropdown-item" href="#">Action</a>
              <a class="dropdown-item" href="#">Another action</a>-->
              <a
                v-if="changePasswordFlag"
                class="dropdown-item"
                @click="redirectChangePassword()"
                style="cursor:pointer"
              >
                <i class="fas fa-key"></i>&nbsp;Change password
              </a>
              <a
                v-if="manageRoleFlag"
                class="dropdown-item"
                @click="redirectRole()"
                style="cursor:pointer"
              >
                <i class="fas fa-users-cog"></i>&nbsp;Manage Role
              </a>
              <a
                v-if="manageUserFlag"
                class="dropdown-item"
                @click="redirectUser()"
                style="cursor:pointer"
              >
                <i class="fas fa-users"></i>&nbsp;Manage User
              </a>
              <a class="dropdown-item" @click="logout()" style="cursor:pointer">
                <i class="fas fa-sign-out-alt"></i>&nbsp;Logout
              </a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import router from "../../router";
import * as constant from "../constant/constant";
const img = require("../../assets/InfineraLogo.png");
export default {
  name: "headernav",
  props: ["msg", "loaderFlag"],
  created() {
    this.image = img;
    this.firstName = localStorage.getItem("first_name");
    this.username = localStorage.getItem("username");
    var authorization = localStorage.getItem("authorization");

    var permissions = authorization.split(",");

    var isSocial = localStorage.getItem("isSocial");
    if (isSocial !== "false") {
      this.changePasswordFlag = false;
    }

    for (var i = 0; i < permissions.length; i++) {
      if (permissions[i] === constant.PERMISSIONS[6]) {
        this.manageRoleFlag = true;
      } else if (permissions[i] === constant.PERMISSIONS[7]) {
        this.manageUserFlag = true;
      }
    }
  },
  data() {
    console.log("header");
    return {
      firstName: "",
      username: "",
      image: "",
      manageRoleFlag: false,
      manageUserFlag: false,
      changePasswordFlag: true
    };
  },

  beforeMount() {},
  methods: {
    redirectUser() {
      router.push("/user");
    },
    redirectRole() {
      router.push("/role");
    },
    redirectChangePassword() {
      router.push("/password");
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
.dropdown-menu {
  font-size: 0.75em !important;
}
.bg-light {
  background-color: #ededed !important;
}
.text {
  font-family: "Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif;
  color: #72879d !important;
  font-size: 1.563em;
}
a {
  text-decoration: none;
}

.main-wrap {
  background: #000;
  text-align: center;
}
.main-wrap h1 {
  color: #fff;
  margin-top: 3.125em;
  margin-bottom: 2.25em;
}
.col-md-3 {
  display: block;
  float: left;
  margin: 1% 0 1% 1.6%;
  background-color: #eee;
  padding: 3.125em 0;
}

.col:first-of-type {
  margin-left: 0;
}

/* ALL LOADERS */

.loader {
  width: 50;
  height: 3.125em;
  border-radius: 100%;
  position: center;
  margin: 0 auto;
}

/* LOADER 1 */

#loader-2 span {
  display: inline-block;
  width: 0.938em;
  height: 0.938em;
  border-radius: 100%;
  background-color: #26b89a;
  margin: 1.25em 0.625em;
}

#loader-2 span:nth-child(1) {
  animation: bounce 1s ease-in-out infinite;
}

#loader-2 span:nth-child(2) {
  animation: bounce 1s ease-in-out 0.33s infinite;
}

#loader-2 span:nth-child(3) {
  animation: bounce 1s ease-in-out 0.66s infinite;
}

@keyframes bounce {
  0%,
  75%,
  100% {
    -webkit-transform: translateY(0);
    -ms-transform: translateY(0);
    -o-transform: translateY(0);
    transform: translateY(0);
  }

  25% {
    -webkit-transform: translateY(-20px);
    -ms-transform: translateY(-20px);
    -o-transform: translateY(-20px);
    transform: translateY(-20px);
  }
}
</style>
