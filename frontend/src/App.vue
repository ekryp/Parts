<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {};
  }
};
</script>

<style>
body {
  font-family: "Helvetica Neue", Roboto, Arial, "Droid Sans", sans-serif;
  color: #72879d;
  background-color: #f7f7f7;
  font-size: 1vw;
}
.custom-container {
  margin-left: 20%;
  /* padding-top: 5%; */
}
.btn-success {
  background-color: #26b99a;
}
.btn-success:hover {
  background-color: #169f85;
}
</style>
