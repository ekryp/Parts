<template>
  <div>
    <headernav msg="Reference"/>
    <side-nav menu="refernce"/>
    <div class="custom-container" style="padding:3%; paddingTop:7%">
      <div class="myBreadCrumb" style="margin-bottom:1px">
        <p>
          <span style="font-size: 14px;">{{knowledgeMapConstant.breadcrumb}}</span>
        </p>
      </div>
      <div class>
        <h5 style="font-size: 1.25em;">{{knowledgeMapConstant.tableHeader}}</h5>
        <br>
        <br>
        <div>
          <div class="col-lg-12">
            <div class="row">
              <div class="table-responsive">
                <table class="table" style="width:100%">
                  <thead>
                    <tr>
                      <th width="20%">File Type</th>
                      <th width="60%">Description</th>
                      <th width="20%">Options</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <label>{{knowledgeMapConstant.docNames[0]}}</label>
                      </td>
                      <td>
                        Release Notes are documents that are delivered as part of a release and
                        contain important information about the release includeing open and closed issues.
                      </td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('releasenotes')"
                        ></i>
                      </td>
                    </tr>

                    <tr>
                      <td>
                        <label>{{knowledgeMapConstant.docNames[1]}}</label>
                      </td>
                      <td>
                        These are Field Service Bulletins (FSB) that are issues when an important issue is
                        discovered and what the customer needs to do when they encounter such issues.
                      </td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('fsb')"
                        ></i>
                      </td>
                    </tr>

                    <tr>
                      <td>
                        <label>{{knowledgeMapConstant.docNames[2]}}</label>
                      </td>
                      <td>A technical note (Tech Note) is an article giving a brief description of a technique or procedure.</td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('technotes')"
                        ></i>
                      </td>
                    </tr>

                    <tr>
                      <td>
                        <label>{{knowledgeMapConstant.docNames[3]}}</label>
                      </td>
                      <td>Test Plan are documents that provide the details on the steps to be executed to test a particular functionality.</td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('testplan')"
                        ></i>
                      </td>
                    </tr>

                    <tr>
                      <td>
                        <label>{{knowledgeMapConstant.docNames[4]}}</label>
                      </td>
                      <td>Method Of Procedure (MOP) is a step-by-step sequence for performing an operation</td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('mop')"
                        ></i>
                      </td>
                    </tr>

                    <tr v-if="this.ekrypUserFlag">
                      <td>
                        <label>{{knowledgeMapConstant.docNames[5]}}</label>
                      </td>
                      <td>Ekryp Help is a set of general queries user have about the product</td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('faq')"
                        ></i>
                      </td>
                    </tr>

                    <tr >
                      <td>
                        <label>{{knowledgeMapConstant.docNames[6]}}</label>
                      </td>
                      <td>to be added</td>
                      <td>
                        &nbsp; &nbsp; &nbsp;
                        <i
                          class="fas fa-eye"
                          style="cursor:pointer;color:#169f85;"
                          @click="routeToView('usecase')"
                        ></i>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <!-- Footer -->
      <footer class="footer font-small blue">
        <!-- Copyright -->
        <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
        <!-- Copyright -->
      </footer>
      <!-- Footer -->
    </div>
  </div>
</template>

<script>
import router from "../../router";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";

import DownloadExcel from "@/components/DownloadExcel/JsonExcel";

import swal from "sweetalert";

export default {
  name: "Reference",
  components: {
    SideNav,
    headernav,
    DownloadExcel
  },
  created() {
    this.editFlag = localStorage.getItem("editFlag");
    this.email_id = localStorage.getItem("email_id");
    this.ekrypUserFlag = localStorage.getItem("ekrypUserFlag");
  },
  data() {
    console.log("home");
    return {
      email_id: "",
      ekrypUserFlag:false,
      knowledgeMapConstant: constant.KnowledgeMapScreen,
      editFlag: false
    };
  },
  methods: {
    routeToView(fileType) {
      console.log(fileType);
      router.push({
        path: "/knowledge/" + fileType
      });
    }
  }
};
</script>
<style>
.main {
  height: 100vh;
  background-color: #293f55;
}
.content {
  padding-top: 20%;
  text-align: left;
  vertical-align: middle;
}
</style>
