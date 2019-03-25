<template>
  <!-- Footer -->
  <footer class="footer fixed-bottom font-small blue">
    <!-- Copyright -->
    <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
    <!-- Copyright -->
  </footer>
  <!-- Footer -->
</template>

<script>
export default {
  name: "footernav",
  created() {},
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
  methods: {}
};
</script>
<style>
</style>
