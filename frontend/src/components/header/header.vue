<template>
<div style="position:fixed;marginLeft:20%;width:80%;z-index:99999;">
<nav class="navbar navbar-expand-lg navbar-light bg-light">
   <a class="navbar-brand text" href="#">{{msg}}</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavDropdown">
    <ul class="navbar-nav ml-auto">
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-user"></i>&nbsp;User
        </a>
        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
          <!-- <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a> -->
          <a class="dropdown-item" href="#"><i class="fas fa-sign-out-alt"></i>&nbsp;Logout</a>
        </div>
      </li>
    </ul>
  </div>
</nav>
</div>
</template>

<script>
import router from "../../router";
export default {
  name: "headernav",
  props: ["msg"],
  data() {
    console.log("header");
    return {};
  },
  beforeMount() {},
  methods: {}
};
</script>
<style>
.dropdown-menu {
  font-size: 12px !important;
}
.bg-light {
  background-color: #ededed !important;
}
.text {
  font-family: "Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif;
  color: #72879d !important;
  font-size: 25px;
}
</style>
