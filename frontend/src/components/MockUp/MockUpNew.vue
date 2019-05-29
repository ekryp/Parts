  <template>
  <div>
    <headernav msg="SolutionScreen"/>
    <side-nav/>
    <Loading :active="isLoading" :can-cancel="false" color="#15ba9a"></Loading>

    <vudal name="myModal">
      <div class="header">
        <div class="row">
          <div class="col-lg-11">
            <h4 v-if="patchFlag">{{solutionScreenConstants.modalHeader}}</h4>
          </div>
          <div class="col-lg-1 in-progress" @click="hideModal()">
            <i class="fa fa-times fa-md pull-right" aria-hidden="true"></i>
          </div>
        </div>
      </div>
      <div class="content contentwidth">
        <div class="row">
          <div class="col-lg-5" v-if="devTrackFlag">
            <label class="labelweightIssueId">Issue Id:</label>
          </div>
          <div class="col-lg-7" v-if="devTrackFlag">
            <span class="col-lg-5 labelweightIssueId">{{devTrackContent.issueId}}</span>
          </div>
        </div>
        <nav v-if="devTrackFlag">
          <div class="nav nav-tabs" id="nav-tab" role="tablist">
            <a
              class="nav-item nav-link active navHeaderColor"
              id="nav-Details-tab"
              data-toggle="tab"
              href="#nav-Details"
              role="tab"
              aria-controls="nav-Details"
              aria-selected="true"
            >{{solutionScreenConstants.modalTabHeaders[0]}}</a>
            <a
              class="nav-item nav-link navHeaderColor"
              id="nav-Description-tab"
              data-toggle="tab"
              href="#nav-Description"
              role="tab"
              aria-controls="nav-Description"
              aria-selected="true"
            >{{solutionScreenConstants.modalTabHeaders[1]}}</a>
          </div>
        </nav>
        <div class="tab-content" id="nav-tabContent " v-if="devTrackFlag">
          <div
            class="tab-pane fade show"
            id="nav-Description"
            role="tabpanel"
            aria-labelledby="nav-Description-tab"
          >
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[0]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.title}}</span>
              </div>
            </div>
            <br>
            <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[1]}}</label>
            <br>
            <span class="textOverlay">{{devTrackContent.description}}</span>
          </div>

          <div
            class="tab-pane active show"
            id="nav-Details"
            role="tabpanel"
            aria-labelledby="nav-Details-tab"
          >
            <br>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[2]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.progressStatus}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[3]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.group}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[4]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.severity}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">Priority:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.priority}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[5]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.foundInBuild}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[6]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.tragetRelease}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[7]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.dateClosed}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[8]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.product}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[9]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.serviceAccount}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[10]}}</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.fixedinRelease}}</span>
              </div>
            </div>

            <div class="row">
              <div class="col-lg-5">
                <label class="labelweight">Found in Release:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.foundinRelease}}</span>
              </div>
            </div>

            <!-- <div class="row">
              <div class="col-lg-5">
                <label>Issue Id:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.ids}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Current Owner:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.currentOwner}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Case Reason:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.caseReason}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Current Owner:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.currentOwner}}</span>
              </div>
            </div>
            
            <div class="row">
              <div class="col-lg-5">
                <label>Date Submitted:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.dateSubmitted}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Final Test RootCause Analysis Comments:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.finalTestRootCauseAnalysisComments}}</span>
              </div>
            </div>
            
            <div class="row">
              <div class="col-lg-5">
                <label>Found In Build:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.foundInBuild}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Found On Platform:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.foundOnPlatform}}</span>
              </div>
            </div>
            
            <div class="row">
              <div class="col-lg-5">
                <label>Hw PON:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.hwPON}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Priority:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.priority}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Problem Description Impacted:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.problemDescriptionImpacted}}</span>
              </div>
            </div>
          
            
            <div class="row">
              <div class="col-lg-5">
                <label>Reporting Customer:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.reportingCustomer}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Resolution:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.resolution}}</span>
              </div>
            </div>
            
            <div class="row">
              <div class="col-lg-5">
                <label>Submitted By:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.submittedBy}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Symptoms:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.symptoms}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Title:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.title}}</span>
              </div>
            </div>
          
            <div class="row">
              <div class="col-lg-5">
                <label>Type:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.type}}</span>
              </div>
            </div>
            <div class="row">
              <div class="col-lg-5">
                <label>Workaround:</label>
              </div>
              <div class="col-lg-7">
                <span>{{devTrackContent.workaround}}</span>
              </div>
            </div>
            -->
          </div>
        </div>

        <div v-if="releaseNotesFlag">
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[0]}}</label>
            </div>
            <div class="col-lg-7">
              <span>{{releaseNoteContent.file_name}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[1]}}</label>
          <br>
          <span class="textOverlay">{{releaseNoteContent.description}}</span>
          <br>
          <div
            v-if="(releaseNoteContent.workaround !==' ') && (releaseNoteContent.workaround !=='') "
          >
            <label class="labelweight">Workaround :</label>
            <br>
            <span class="textOverlay">{{releaseNoteContent.workaround}}</span>
          </div>
        </div>

        <div v-if="testPlanFlag">
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">File Name :</label>
            </div>
            <div class="col-lg-7">
              <span>{{testPlanContent.file_name}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">Objective :</label>
          <br>
          <span class="textOverlay">{{testPlanContent.Objective}}</span>
          <br>
          <br>
          <div>
            <label class="labelweight">Procedure :</label>
            <br>
            <span class="textOverlay">{{testPlanContent.Procedure}}</span>
            <!-- <span v-for="item in testPlanContent.Procedure" :key="item" class="textOverlay">
              {{item}}
              <br>
            </span>-->
          </div>
        </div>

        <div v-if="mopFlag">
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">File Name :</label>
            </div>
            <div class="col-lg-7">
              <span>{{mopContent.file_name}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">Title :</label>
          <br>
          <span class="textOverlay">{{mopContent.title}}</span>
          <br>

          <div>
            <label class="labelweight">Introduction :</label>

            <span class="textOverlay">{{mopContent.introduction}}</span>
          </div>
        </div>

        <div v-if="techNotesFlag">
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">File Name :</label>
            </div>
            <div class="col-lg-7">
              <span>{{techNotesContent.references}}</span>
            </div>
          </div>
        </div>

        <div v-if="fsbFlag">
          <br>
          <div class="row">
            <div class="col-lg-5">
              <label class="labelweight">FSB Number</label>
            </div>
            <div class="col-lg-7">
              <span>{{fsbContent.FSBNumber}}</span>
            </div>
          </div>
          <br>
          <label class="labelweight">{{solutionScreenConstants.modalContentsLabels[1]}}</label>
          <br>
          <span class="textOverlay">{{fsbContent.description}}</span>
          <br>
          <label class="labelweight">Symptoms :</label>
          <br>
          <span class="textOverlay">{{fsbContent.symptoms}}</span>
          <br>
          <label class="labelweight">Root Cause :</label>
          <br>
          <span class="textOverlay">{{fsbContent.rootCause}}</span>
        </div>
      </div>
      <div class="actions">
        <!-- <button type="button" class="btn btn-danger" @click="hideModal()">OK</button> -->
      </div>
    </vudal>

    <div class="custom-container">
      <div class="row-one">
        <div class="myBreadCrumb">
          <p>
            <span style="font-size: 14px;">{{solutionScreenConstants.breadcrumb}}</span>
          </p>
        </div>

        <!-- Filter Section -->

        <div class="row">
          <div class="col-lg-12">
            <div class="p-3 mb-3 bg-white">
              <!-- <div class="row align">
              <div class="col-md-2">
                <label>{{solutionScreenConstants.labAvailablity}}</label>
              </div>
              <div class="col-md-2" align="left">
                <i class="fas fa-dot-circle" style="color:green" v-if="showGreen"></i>
                <i class="fas fa-dot-circle" style="color:#d62828f7" v-if="!showGreen"></i>
              </div>
              <div class="col-md-4" v-if="analyzeFlag">
                <button type="button" style="fontSize:0.75vw;" class="btn btn-success" @click="onReserve()">{{solutionScreenConstants.buttons[1]}}</button>
              </div>
              </div>-->
              <div class="row align">
                <label
                  class="col-md-6 labelweight"
                >{{solutionScreenConstants.problemDescriptionName}}</label>
                <label class="col-md-6 labelweight">{{solutionScreenConstants.tagHeader}}</label>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="row">
                    <div class="col-md-12">
                      <textarea
                        @change="problemDescriptionChange()"
                        v-model="problemDescription"
                        class="form-control"
                        rows="3"
                        id="email"
                        :placeholder="problemDescriptionPlaceholder"
                      ></textarea>
                    </div>
                  </div>
                  <!-- <div class="row">
                    <div class="col-lg-10"></div>
                    <div class="col-lg-2 alignButton">
                      <button
                        v-if="problemDescription.trim() !== ''"
                        style="fontSize:0.75vw;"
                        type="button"
                        class="btn btn-success btn-block"
                        @click="getMlKeywords()"
                      >{{solutionScreenConstants.buttons[0]}}</button>
                      <button
                        v-if="problemDescription.trim() === ''"
                        style="fontSize:0.75vw;"
                        type="button"
                        class="btn btn-success btn-block"
                        @click="getMlKeywords()"
                        disabled
                      >{{solutionScreenConstants.buttons[0]}}</button>
                    </div>
                  </div>-->
                </div>
                <div class="col-md-6">
                  <div class="row">
                    <!-- <div class="col-md-9">
                      <Multiselect
                        v-model="filterValue"
                        tag-placeholder="Add this as new tag"
                        placeholder="Problem Area"
                        label="name"
                        track-by="name"
                        :options="filterOptions"
                        :close-on-select="false"
                        :multiple="true"
                        :clear-on-select="false"
                        :hide-selected="true"
                        :taggable="true"
                      ></Multiselect>
                    </div>
                    <br>

                    <div class="col-lg-3" style="marginTop:2%">
                      <input type="checkbox" id="checkbox" v-model="checked">
                      <label for="checkbox">{{solutionScreenConstants.checkBoxLabel}}</label>
                    </div>-->

                    <!-- <label class="col-md-6 labelweight align">{{solutionScreenConstants.tagHeader}}</label> -->

                    <div class="col-md-12">
                      <Multiselect
                        v-model="tagValue"
                        tag-placeholder="Add this as new tag"
                        placeholder="Filters"
                        label="name"
                        track-by="name"
                        :options="tagOptions"
                        :close-on-select="false"
                        :multiple="true"
                        :clear-on-select="false"
                        :hide-selected="true"
                        :taggable="true"
                        @tag="addTag"
                      ></Multiselect>
                    </div>
                    <div class="col-lg-10"></div>
                    <!-- 
                      Previous Search Condition
                      v-if="searchFlag &&problemDescription.trim() !== ''"
                    v-if="!searchFlag ||problemDescription.trim() === ''  "-->
                    <div class="col-lg-2" style="paddingTop:0.35em">
                      <button
                        v-if="problemDescription.trim() !== ''"
                        style="fontSize:0.75vw;"
                        type="button"
                        class="btn btn-success btn-block"
                        @click="onAnalyze()"
                      >{{solutionScreenConstants.buttons[2]}}</button>
                      <button
                        v-if="problemDescription.trim() === ''  "
                        style="fontSize:0.75vw;"
                        type="button"
                        class="btn btn-success btn-block"
                        @click="onAnalyze()"
                        disabled
                      >{{solutionScreenConstants.buttons[2]}}</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row" style="textAlign:center" v-if="analyzeFlag">
        <div class="col-lg-12">
          <div class="row">
            <!-- <div class="col-lg-2">
              <div class="card shadow p-2 mb-5 rounded">
                <div class="card-body in-progress labelweight cardFontChange">
                  <span class="float-left">Total Hits</span>
                  <span
                    class="float-right"
                  >{{this.devTrackData.length+this.releaseNotesData.length+this.fsbData.length+this.testPlanData.length}}</span>
                </div>
              </div>
            </div>-->

            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b1color , color:textcolor1}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  @click="showDevTrack()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[0]}}</span>
                  <span class="float-right">{{this.devTrackData.length}}</span>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b2color , color:textcolor2}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  @click="showReleaseNotes()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[1]}}</span>
                  <span class="float-right">{{this.releaseNotesData.length}}</span>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b4color , color:textcolor4}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  @click="showTestPlans()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[3]}}</span>
                  <span class="float-right">{{this.testPlanData.length}}</span>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b3color , color:textcolor3}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  v-bind:style="{ backgroundColor: b3color }"
                  @click="showFSB()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[2]}}</span>
                  <span class="float-right">{{this.fsbData.length}}</span>
                </div>
              </div>
            </div>
            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b5color , color:textcolor5}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  v-bind:style="{ backgroundColor: b5color }"
                  @click="showMOP()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[4]}}</span>
                  <span class="float-right">{{this.mopData.length}}</span>
                </div>
              </div>
            </div>

            <div class="col-lg-2">
              <div
                class="card shadow p-2 mb-5 rounded"
                v-bind:style="{ backgroundColor: b6color , color:textcolor6}"
              >
                <div
                  class="card-body in-progress labelweight cardFontChange"
                  v-bind:style="{ backgroundColor: b6color }"
                  @click="showTechNotes()"
                >
                  <span class="float-left">{{solutionScreenConstants.cardLables[5]}}</span>
                  <span class="float-right">{{this.techNotesData.length}}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- FIlter Section -->
      <div class="row text-center" v-if="analyzeFlag && devTrackFlag">
        <div class="col-lg-1" v-if="!filterFLag" @click="changeFilter()" align="left">
          <i class="fas fa-filter fa-lg" style="color:#169f85"></i>
        </div>
        <div class="col-lg-1" v-if="filterFLag" @click="changeFilter()" align="left">
          <i class="fas fa-times fa-lg" style="color:#169f85"></i>
        </div>

        <div class="col"></div>
      </div>
      <br>
      <br v-if="!analyzeFlag">
      <transition name="fade" v-if="analyzeFlag && devTrackFlag">
        <div class="row" style="paddingTop:0.6em" v-if="filterFLag">
          <div class="col-lg-12">
            <div class="p-3 mb-3 bg-white">
              <div class="row">
                <div class="col-lg-12">
                  <div class="float-right">
                    <toggle-button
                      :value="state"
                      :color="{checked: 'green', unchecked: 'green'}"
                      :sync="true"
                      cssColors:true
                      :labels="{checked: 'Check Title', unchecked: 'Check All'}"
                      :width="90"
                      v-tooltip.top.hover.focus="'Click to Toggle'"
                      @change="stateChange()"
                    />
                  </div>
                </div>
              </div>

              <div class="row align">
                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[0]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('product')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="productValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Customer"
                      label="name"
                      track-by="name"
                      :options="productOptions"
                      :close-on-select="false"
                      :multiple="true"
                      :clear-on-select="false"
                      :hide-selected="true"
                      :taggable="true"
                      @close="validateProductSelect()"
                      @remove="validateProductClose()"
                    ></Multiselect>
                  </div>
                </div>

                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[1]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('group')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="groupValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Group"
                      label="name"
                      track-by="name"
                      :options="groupOptions"
                      :multiple="true"
                      :taggable="true"
                      :clear-on-select="false"
                      :close-on-select="false"
                      :hide-selected="true"
                      @close="validateGroupSelect()"
                      @remove="validateGroupClose()"
                    ></Multiselect>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[2]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('severity')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="severityValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Severity"
                      label="name"
                      track-by="name"
                      :options="severityOptions"
                      :close-on-select="false"
                      :multiple="true"
                      :clear-on-select="false"
                      :hide-selected="true"
                      :taggable="true"
                      @close="validateSeveritySelect()"
                      @remove="validateSeverityClose()"
                    ></Multiselect>
                  </div>
                </div>
              </div>
              <div class="row align">
                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[3]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('priority')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="priorityValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Priority"
                      label="name"
                      track-by="name"
                      :options="priorityOptions"
                      :multiple="true"
                      :taggable="true"
                      :clear-on-select="false"
                      :close-on-select="false"
                      :hide-selected="true"
                      @close="validatePrioritySelect()"
                      @remove="validatePriorityClose()"
                    ></Multiselect>
                  </div>
                </div>

                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-6">{{solutionScreenConstants.filterNames[6]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('foundInRelease')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="foundInReleaseValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Found In Release"
                      label="name"
                      track-by="name"
                      :options="foundInReleaseOptions"
                      :multiple="true"
                      :taggable="true"
                      :clear-on-select="false"
                      :close-on-select="false"
                      :hide-selected="true"
                      @close="validateFoundInReleaseSelect()"
                      @remove="validateFoundInReleaseClose()"
                    ></Multiselect>
                  </div>
                </div>

                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[5]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('fixedInRelease')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="fixedInReleaseValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Fixed In Release"
                      label="name"
                      track-by="name"
                      :options="fixedInReleaseOptions"
                      :close-on-select="false"
                      :multiple="true"
                      :clear-on-select="false"
                      :hide-selected="true"
                      :taggable="true"
                      @close="validateFixedInReleaseSelect()"
                      @remove="validateFixedInReleaseClose()"
                    ></Multiselect>
                  </div>
                </div>
              </div>
              <div class="row align">
                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-4">{{solutionScreenConstants.filterNames[8]}}</div>
                    <div class="col" align="right">
                      <button
                        style="fontSize:1vw;"
                        type="button"
                        class="all-success"
                        @click="clearAll('serviceAccount')"
                      >
                        <i class="fas fa-minus-circle"></i>
                        &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                      </button>
                    </div>
                  </div>
                  <div style="paddingTop:0.5em">
                    <Multiselect
                      v-model="serviceAccountValue"
                      tag-placeholder="Add this as new tag"
                      placeholder="Search Service Account"
                      label="name"
                      track-by="name"
                      :options="serviceAccountOptions"
                      :close-on-select="false"
                      :multiple="true"
                      :clear-on-select="false"
                      :hide-selected="true"
                      :taggable="true"
                      @close="validateServiceAccountSelect()"
                      @remove="validateServiceAccountClose()"
                    ></Multiselect>
                  </div>
                </div>

                <div class="col-lg-4">
                  <div class="row">
                    <div class="col-lg-12">{{solutionScreenConstants.filterNames[7]}}</div>
                  </div>
                  <div>
                    <date-picker
                      style="height:40px;paddingTop:1.1em"
                      v-model="time1"
                      lang="en"
                      value-type="format"
                      :format="format"
                      :first-day-of-week="1"
                      @change="getMlKeywords()"
                    ></date-picker>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
      <br>
      <div class="align card p-2 mb-5 rounded text-center" v-if="errorFlag"></div>
      <div class="row" v-if="devTrackFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <!-- <div class="row">
                
                  <div class="col-md-10">
                  <h5 align="left" >Dev Track</h5>
                  </div>
            </div>-->

            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>{{solutionScreenConstants.tableHeaders[0]}}</th>
                    <th style="width: 45.66%">{{solutionScreenConstants.tableHeaders[1]}}</th>
                    <th>{{solutionScreenConstants.tableHeaders[2]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[3]}}</th>
                    <th>{{solutionScreenConstants.tableHeaders[4]}}</th>
                    <th>{{solutionScreenConstants.tableHeaders[5]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[6]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[7]}}</th>
                  </thead>
                  <tbody v-if="devTrackData.length >0 && moreFlag1" class="text-center">
                    <tr v-for="item in devTrackData" :key="item.index">
                      <td
                        @click="showPatchModal(item.index,'devtrack')"
                        class="in-progress"
                      >{{item.issueId}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.title}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.severity}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.foundinRelease}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.dateSubmitted}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.dateClosed}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'devtrack')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'devtrack')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'devtrack')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody v-if="devTrackData.length >0 && !moreFlag1" class="text-center">
                    <tr v-for="item in filterDevTrackData(devTrackData)" :key="item.index">
                      <td
                        @click="showPatchModal(item.index,'devtrack')"
                        class="in-progress"
                      >{{item.issueId}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.title}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.severity}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.foundinRelease}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.dateSubmitted}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.dateClosed}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'devtrack')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span v-for="(userFlag, index)  in  item.upvotedUsers" :key="index">
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'devtrack')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'devtrack')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'devtrack')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="devTrackData.length>0 && !moreFlag1"
                  class="text-centered in-progress"
                  @click="showAll()"
                >More</div>
                <!-- <div v-if ="devTrackData.length>0 && moreFlag" class="text-centered" @click="showAbove80()">
                  Hide
                </div>-->
                <div v-if="devTrackData.length==0" class="text-centered">No Data</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row" v-if="releaseNotesFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>Issue Id</th>
                    <th>File Name</th>
                    <th>Severity</th>

                    <th style="width: 10%">Confidence (%)</th>
                    <th>Confirm</th>
                  </thead>
                  <tbody class="text-center" v-if="releaseNotesData.length >0 && moreFlag2">
                    <tr v-for="item in releaseNotesData" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.issueId}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.severity}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'releasenotes')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'releasenotes')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'releasenotes')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody class="text-center" v-if="releaseNotesData.length >0 && !moreFlag2">
                    <tr v-for="item in filterDevTrackData(releaseNotesData)" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.issueId}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.severity}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'releaseNotes')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'releasenotes')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'releasenotes')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'releasenotes')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="releaseNotesData.length>0 && !moreFlag2"
                  class="text-centered in-progress"
                  @click="showAllRl()"
                >More</div>
                <!-- <div v-if ="releaseNotesData.length>0 && moreFlag2" class="text-centered" @click="showAbove80Rl()">
                  Hide
                </div>-->
                <div v-if="releaseNotesData.length==0" class="text-centered">No Data</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--  Test Plan Flag-->

      <div class="row" v-if="testPlanFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>File Name</th>

                    <th>Objective</th>

                    <th style="width: 10%">Confidence (%)</th>
                    <th>Confirm</th>
                  </thead>
                  <tbody class="text-center" v-if="testPlanData.length >0 && moreFlag4">
                    <tr v-for="item in testPlanData" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.Objective}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'testplan')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'testplan')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'testplan')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody class="text-center" v-if="testPlanData.length >0 && !moreFlag4">
                    <tr v-for="item in filterDevTrackData(testPlanData)" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.Objective}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'testPlan')"
                      >{{item.probability}}</td>
                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'testplan')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'testplan')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'testplan')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="testPlanData.length>0 && !moreFlag4"
                  class="text-centered in-progress"
                  @click="showAllTestPlan()"
                >More</div>
                <!-- <div v-if ="releaseNotesData.length>0 && moreFlag2" class="text-centered" @click="showAbove80Rl()">
                  Hide
                </div>-->
                <div v-if="testPlanData.length==0" class="text-centered">No Data</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--  Mop Flag-->

      <div class="row" v-if="mopFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>File Name</th>

                    <th>Title</th>

                    <th style="width: 10%">Confidence (%)</th>
                    <th>Confirm</th>
                  </thead>
                  <tbody class="text-center" v-if="mopData.length >0 && moreFlag5">
                    <tr v-for="item in mopData" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.title}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'mop')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'mop')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'mop')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody class="text-center" v-if="mopData.length >0 && !moreFlag5">
                    <tr v-for="item in filterDevTrackData(mopData)" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.title}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'mop')"
                      >{{item.probability}}</td>
                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'mop')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'mop')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'mop')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="mopData.length>0 && !moreFlag5"
                  class="text-centered in-progress"
                  @click="showAllMop()"
                >More</div>
                <!-- <div v-if ="releaseNotesData.length>0 && moreFlag2" class="text-centered" @click="showAbove80Rl()">
                  Hide
                </div>-->
                <div v-if="mopData.length==0" class="text-centered">No Data</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!--  Tech Notes Flag-->

      <div class="row" v-if="techNotesFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>File Name</th>

                    <th>Description</th>

                    <th style="width: 10%">Confidence (%)</th>
                    <th>Confirm</th>
                  </thead>
                  <tbody class="text-center" v-if="techNotesData.length >0 && moreFlag6">
                    <tr v-for="item in techNotesData" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.description}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'techNotes')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'techNotes')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'techNotes')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody class="text-center" v-if="techNotesData.length >0 && !moreFlag6">
                    <tr v-for="item in filterDevTrackData(techNotesData)" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.description}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'techNotes')"
                      >{{item.probability}}</td>
                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'techNotes')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'techNotes')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'techNotes')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="techNotesData.length>0 && !moreFlag6"
                  class="text-centered in-progress"
                  @click="showAllTechNotes()"
                >More</div>
                <!-- <div v-if ="releaseNotesData.length>0 && moreFlag2" class="text-centered" @click="showAbove80Rl()">
                  Hide
                </div>-->
                <div v-if="techNotesData.length==0" class="text-centered">No Data</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row" v-if="fsbFlag" style="marginTop:-1.8%">
        <div class="col-lg-12">
          <div class="p-3 mb-3 bg-white">
            <div class="row align">
              <div class="col-md-12" align="center">
                <table class="table responsive table-hover">
                  <thead class="text-center">
                    <th>FSBNumber</th>
                    <th>Issue Id</th>
                    <th>File Name</th>
                    <th>Date Created</th>

                    <th>Title</th>
                    <th style="width: 10%">Confidence (%)</th>
                    <th>Confirm</th>
                  </thead>
                  <tbody class="text-center" v-if="fsbData.length >0 && moreFlag3">
                    <tr v-for="item in fsbData" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.FSBNumber}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.issueId}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.dateCreated}}</td>
                      <!-- <td class=" in-progress" @click="showPatchModal(item.index)">{{item.symptoms}}</td> -->
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.title}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.probability}}</td>

                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'fsb')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'fsb')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'fsb')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>

                  <tbody class="text-center" v-if="fsbData.length >0 && !moreFlag3">
                    <tr v-for="item in filterDevTrackData(fsbData)" :key="item.index">
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.FSBNumber}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.issueId}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.file_name}}</td>
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.dateCreated}}</td>
                      <!-- <td class=" in-progress" @click="showPatchModal(item.index)">{{item.symptoms}}</td> -->
                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.title}}</td>

                      <td
                        class="in-progress"
                        @click="showPatchModal(item.index,'fsb')"
                      >{{item.probability}}</td>
                      <td v-if="item.upvotedUsers.length>0">
                        <span
                          v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)"
                          :key="index"
                        >
                          <!-- <p>SSDSD {{userFlag}}</p> -->
                          <i
                            v-if="userFlag !== currentUserEMailId"
                            @click="updatedVote(item,'fsb')"
                            class="far fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          <i
                            v-if="userFlag === currentUserEMailId"
                            @click="downVote(item,'fsb')"
                            class="fas fa-thumbs-up"
                            style="cursor:pointer;color:#293f55;"
                          ></i>
                          &nbsp;{{item.upvotedUsers.length}}
                        </span>
                      </td>

                      <td v-else>
                        <i
                          class="far fa-thumbs-up"
                          @click="updatedVote(item,'fsb')"
                          style="cursor:pointer;color:#293f55;"
                        ></i>
                        &nbsp;{{item.upvotedUsers.length}}
                        <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div
                  v-if="fsbData.length>0 && !moreFlag3"
                  class="text-centered in-progress"
                  @click="showAllfsb()"
                >More</div>
                <!-- <div v-if ="fsbData.length>0 && moreFlag3" class="text-centered" @click="showAbove80fsb()">
                  Hide
                </div>-->
                <div v-if="fsbData.length==0" class="text-centered">No Data</div>
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
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import * as constant from "../constant/constant";
import swal from "sweetalert";
import Vudal from "vudal";
import accounting from "../../utilies/accounting";
import Multiselect from "vue-multiselect";
import tagsinput from "vue-tagsinput";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";
import * as solutionFilterData from "../../utilies/solutionfiltersample.json";
import DatePicker from "vue2-datepicker";
//import * as data from "../../utilies/tabledata.json";

export default {
  name: "MockUpNew",
  components: {
    SideNav,
    headernav,
    Multiselect,
    tagsinput,
    Vudal,
    DatePicker,
    Loading
  },
  created() {
    clearInterval(window.intervalObj);
    this.currentUserEMailId = localStorage.getItem("email_id");
    this.internalFlag = localStorage.getItem("internalFlag");
  },
  data() {
    console.log("dashboard", this.data);
    return {
      isLoading: false,
      tags: [],
      solutionScreenConstants: constant.SolutionScreen,
      showGreen: true,
      checked: false,
      state: false,
      filterFLag: false,
      searchFlag: false,
      devTrackData: [],
      releaseNotesData: [],
      fsbData: [],
      techNotesData: [],
      testPlanData: [],
      mopData: [],
      errorFlag: false,
      tarFileName: "",
      filterSynonym: "",
      tarFile: "",
      b1color: "",
      b2color: "",
      b3color: "",
      b4color: "",
      b5color: "",
      b6color: "",
      format: "MM/DD/YYYY",
      textcolor1: "",
      textcolor2: "",
      textcolor3: "",
      textcolor4: "",
      textcolor5: "",
      textcolor6: "",
      testPlanContent: "",
      moreFlag1: false,
      moreFlag2: false,
      moreFlag3: false,
      moreFlag4: false,
      moreFlag5: false,
      moreFlag6: false,
      currentUserEMailId: "",
      devTrackContent: "",
      releaseNoteContent: "",
      fsbContent: "",
      mopContent: "",
      techNotesContent: "",
      filterOptions: [],
      filterValue: [],
      tagValue: [],
      tagOptions: [],
      time1: "",
      productValue: [],
      productOptions: [],
      groupValue: [],
      groupOptions: [],
      severityValue: [],
      severityOptions: [],
      priorityValue: [],
      priorityOptions: [],
      foundOnPlatformValue: [],
      foundOnPlatformOptions: [],
      fixedInReleaseValue: [],
      fixedInReleaseOptions: [],
      serviceAccountValue: [],
      serviceAccountOptions: [],
      internalFlag: false,
      foundInReleaseValue: [],
      foundInReleaseOptions: [],
      problemDescriptionPlaceholder: "Enter the Problem Description",
      valueIndex: "",
      filterURL: "",
      releaseFlag: true,
      patchFlag: false,
      problemDescription: "",
      analyzeFlag: false,
      devTrackFlag: false,
      releaseNotesFlag: false,
      fsbFlag: false,
      testPlanFlag: false,
      techNotesFlag: false,
      mopFlag: false,
      errorFlag: false,
      sdfcFlag: false,
      mlKeywords: "",
      estotalhits: 0,
      filterValues: "",
      tagValues: ""
    };
  },
  methods: {
    showTime() {
      console.log(this.time1);
    },
    onReserve() {
      console.log(this.showGreen);
      if (this.showGreen) {
        this.showGreen = false;
      } else {
        this.showGreen = true;
      }
    },
    handleChange(removeIndex, tag) {
      if (this.tags.length == removeIndex) {
        console.log(removeIndex);
        this.tags.push(tag);
      } else {
        this.tags.splice(removeIndex, 1);
      }
      console.log(removeIndex);
      console.log(this.tags);
    },
    showDevTrack() {
      this.devTrackFlag = true;
      this.releaseNotesFlag = false;
      this.testPlanFlag = false;
      this.mopFlag = false;
      this.fsbFlag = false;
      this.techNotesFlag = false;
      this.b1color = "#2a629a";
      this.textcolor1 = "#f8f9fa";
      this.b2color = "";
      if (this.devTrackData.length === 0) {
        this.devTrackData = [];
      }
      this.textcolor2 = "";
      this.b3color = "";
      this.textcolor3 = "";
      this.b4color = "";
      this.textcolor4 = "";
      this.b5color = "";
      this.textcolor5 = "";
      this.b6color = "";
      this.textcolor6 = "";
    },
    stateChange() {
      this.state = !this.state;
      this.getMlKeywords();
    },
    showPatchModal(index, type) {
      if (type === "devtrack") {
        this.devTrackContent = this.devTrackData[index];
      } else if (type === "releaseNotes") {
        this.releaseNoteContent = this.releaseNotesData[index];
      } else if (type === "testPlan") {
        this.testPlanContent = this.testPlanData[index];
      } else if (type === "fsb") {
        this.fsbContent = this.fsbData[index];
      } else if (type === "mop") {
        this.mopContent = this.mopData[index];
      } else if (type === "techNotes") {
        this.techNotesContent = this.techNotesData[index];
      }
      this.patchFlag = true;

      console.log(index);

      this.$modals.myModal.$show();
    },
    showReleaseNotes() {
      console.log("Release Notes", this.releaseNotesData);
      this.devTrackFlag = false;
      this.releaseNotesFlag = true;
      this.testPlanFlag = false;
      this.fsbFlag = false;
      this.techNotesFlag = false;
      this.mopFlag = false;

      if (this.releaseNotesData.length === 0) {
        this.releaseNotesData = [];
      }
      this.b2color = "#2a629a";
      this.textcolor2 = "#f8f9fa";
      this.b1color = "";
      this.textcolor1 = "";
      this.b3color = "";
      this.textcolor3 = "";
      this.b4color = "";
      this.textcolor4 = "";
      this.b5color = "";
      this.textcolor5 = "";
      this.b6color = "";
      this.textcolor6 = "";
    },
    showTestPlans() {
      console.log("Test Plan", this.testPlanData);
      this.devTrackFlag = false;
      this.releaseNotesFlag = false;
      this.testPlanFlag = true;
      this.fsbFlag = false;
      this.mopFlag = false;
      this.techNotesFlag = false;
      if (this.testPlanData.length === 0) {
        this.testPlanData = [];
      }
      this.b2color = "";
      this.textcolor2 = "";
      this.b1color = "";
      this.textcolor1 = "";
      this.b3color = "";
      this.textcolor3 = "";
      this.b4color = "#2a629a";
      this.textcolor4 = "#f8f9fa";
      this.b5color = "";
      this.textcolor5 = "";
      this.b6color = "";
      this.textcolor6 = "";
    },
    showFSB() {
      console.log("this.sfs", this.fsb);
      this.devTrackFlag = false;
      this.releaseNotesFlag = false;
      this.testPlanFlag = false;
      this.fsbFlag = true;
      this.mopFlag = false;
      this.techNotesFlag = false;
      this.b3color = "#2a629a";
      this.textcolor3 = "#f8f9fa";
      this.b2color = "";
      this.textcolor2 = "";
      if (this.fsbData.length === 0) {
        this.fsbData = [];
      }
      this.b1color = "";
      this.textcolor1 = "";
      this.b4color = "";
      this.textcolor4 = "";
      this.b5color = "";
      this.textcolor5 = "";
      this.b6color = "";
      this.textcolor6 = "";
    },
    showMOP() {
      this.devTrackFlag = false;
      this.releaseNotesFlag = false;
      this.testPlanFlag = false;
      this.techNotesFlag = false;
      this.fsbFlag = false;
      this.mopFlag = true;
      this.b5color = "#2a629a";
      this.textcolor5 = "#f8f9fa";
      this.b2color = "";
      this.textcolor2 = "";
      this.b3color = "";
      this.textcolor3 = "";
      if (this.mopData.length === 0) {
        this.mopData = [];
      }
      this.b1color = "";
      this.textcolor1 = "";
      this.b4color = "";
      this.textcolor4 = "";
      this.b6color = "";
      this.textcolor6 = "";
    },
    showTechNotes() {
      this.devTrackFlag = false;
      this.releaseNotesFlag = false;
      this.testPlanFlag = false;
      this.fsbFlag = false;
      this.techNotesFlag = true;
      this.mopFlag = false;
      this.b6color = "#2a629a";
      this.textcolor6 = "#f8f9fa";
      this.b5color = "";
      this.textcolor5 = "";
      this.b2color = "";
      this.textcolor2 = "";
      this.b3color = "";
      this.textcolor3 = "";
      if (this.techNotesData.length === 0) {
        this.techNotesData = [];
      }
      this.b1color = "";
      this.textcolor1 = "";
      this.b4color = "";
      this.textcolor4 = "";
    },
    onAnalyze() {
      this.isLoading = true;
      this.errorFlag = false;
      this.devTrackData = [];
      this.releaseNotesData = [];
      this.fsbData = [];
      this.tagValues = "";

      this.filterURL = "";
      for (var i = 0; i < this.productValue.length; i++) {
        this.filterURL =
          this.filterURL + `&product_filter=` + this.productValue[i].name;
      }

      for (var i = 0; i < this.groupValue.length; i++) {
        this.filterURL =
          this.filterURL + `&group_filter=` + this.groupValue[i].name;
      }
      for (var i = 0; i < this.foundInReleaseValue.length; i++) {
        this.filterURL =
          this.filterURL +
          `&found_in_release_filter=` +
          this.foundInReleaseValue[i].name;
      }
      for (var i = 0; i < this.fixedInReleaseValue.length; i++) {
        this.filterURL =
          this.filterURL +
          `&fixed_in_release_filter=` +
          this.fixedInReleaseValue[i].name;
      }
      for (var i = 0; i < this.serviceAccountValue.length; i++) {
        this.filterURL =
          this.filterURL +
          `&service_account_filter=` +
          this.serviceAccountValue[i].name;
      }
      for (var i = 0; i < this.severityValue.length; i++) {
        this.filterURL =
          this.filterURL + `&severity_filter=` + this.severityValue[i].name;
      }
      for (var i = 0; i < this.priorityValue.length; i++) {
        this.filterURL =
          this.filterURL + `&priority_filter=` + this.priorityValue[i].name;
      }
      for (var i = 0; i < this.foundOnPlatformValue.length; i++) {
        this.filterURL =
          this.filterURL +
          `&found_on_platform_filter=` +
          this.foundOnPlatformValue[i].name;
      }
      if (this.time1 !== "") {
        this.filterURL = this.filterURL + `&date_filter=` + this.time1;
      }
      console.log("Tag Values", this.tagValue);
      for (var i = 0; i < this.tagValue.length; i++) {
        this.tagValues = this.tagValues + " " + this.tagValue[i].value;
      }

      this.problemDescription = this.problemDescription.replace(
        /^\s+|\s+$/g,
        ""
      );
      // if (this.filterValue.length > 0) {
      //   if (this.checked) {
      //     this.mlKeywords = " AND";
      //   } else {
      //     this.mlKeywords = " OR";
      //   }
      // } else {
      this.mlKeywords = "";
      // }
      // for (var i = 0; i < this.filterValue.length; i++) {
      //   if (this.checked) {
      //     this.mlKeywords =
      //       this.mlKeywords + " AND " + this.filterValue[i].name;
      //   } else {
      //     this.mlKeywords = this.mlKeywords + " OR " + this.filterValue[i].name;
      //   }
      // }
      console.log("Filter Values", this.filterValues);
      fetch(
        constant.ELKURL +
          "api/getDevTrackData?search_param=" +
          this.problemDescription +
          this.mlKeywords +
          this.filterSynonym +
          this.tagValues +
          this.filterURL +
          "&internal=" +
          this.internalFlag +
          "&check_title=" +
          this.state,
        {
          headers: {
            "Content-Type": "application/json"
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.http_status_code === 200) {
              this.isLoading = false;
              this.estotalhits = data.data.totalhits;
              console.log("estotal hits ----->", this.estotalhits);
              // if (data.data.devTrack.devtrack.length < 0) {
              //   this.analyzeFlag = true;
              // }
              var upvotedUsers = [];
              this.productOptions = data.data.devTrack.devtrackFilters.product;
              this.groupOptions = data.data.devTrack.devtrackFilters.group;
              this.severityOptions =
                data.data.devTrack.devtrackFilters.severity;
              this.priorityOptions =
                data.data.devTrack.devtrackFilters.priority;
              this.foundOnPlatformOptions =
                data.data.devTrack.devtrackFilters.foundOnPlatform;
              this.fixedInReleaseOptions =
                data.data.devTrack.devtrackFilters.fixedinRelease;
              this.foundInReleaseOptions =
                data.data.devTrack.devtrackFilters.foundinRelease;
              for (var i = 0; i < data.data.devTrack.devtrack.length; i++) {
                let upvotedUserFlag = false;
                if (data.data.devTrack.devtrack[i].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.devTrack.devtrack[i].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }

                this.devTrackData.push({
                  issueId: data.data.devTrack.devtrack[i].issueId,
                  index: i,
                  description: data.data.devTrack.devtrack[i].description,
                  severity: data.data.devTrack.devtrack[i].severity,
                  caseReason: data.data.devTrack.devtrack[i].caseReason,
                  currentOwner: data.data.devTrack.devtrack[i].currentOwner,
                  dateClosed: data.data.devTrack.devtrack[i].dateClosed,
                  dateSubmitted: data.data.devTrack.devtrack[i].dateSubmitted,
                  finalTestRootCauseAnalysisComments:
                    data.data.devTrack.devtrack[i]
                      .finalTestRootCauseAnalysisComments,
                  foundinRelease: data.data.devTrack.devtrack[i].foundinRelease,
                  fixedinRelease: data.data.devTrack.devtrack[i].fixedinRelease,
                  foundInBuild: data.data.devTrack.devtrack[i].foundInBuild,
                  foundOnPlatform:
                    data.data.devTrack.devtrack[i].foundOnPlatform,
                  group: data.data.devTrack.devtrack[i].group,
                  product: data.data.devTrack.devtrack[i].product,
                  probability: data.data.devTrack.devtrack[i].probability,
                  progressStatus: data.data.devTrack.devtrack[i].progressStatus,
                  reportingCustomer:
                    data.data.devTrack.devtrack[i].reportingCustomer,
                  priority: data.data.devTrack.devtrack[i].priority,
                  resolution: data.data.devTrack.devtrack[i].resolution,
                  serviceAccount: data.data.devTrack.devtrack[i].serviceAccount,
                  submittedBy: data.data.devTrack.devtrack[i].submittedBy,
                  symptoms: data.data.devTrack.devtrack[i].symptoms,
                  title: data.data.devTrack.devtrack[i].title,
                  tragetRelease: data.data.devTrack.devtrack[i].tragetRelease,
                  type: data.data.devTrack.devtrack[i].type,
                  workaround: data.data.devTrack.devtrack[i].workaround,
                  upvotedUsers: upvotedUsers
                });
                this.moreFlag1 = false;
                this.moreFlag2 = false;
                this.moreFlag3 = false;
                this.moreFlag4 = false;
              }
              this.showDevTrack();
              for (var j = 0; j < data.data.releaseNotes.length; j++) {
                if (data.data.releaseNotes[j].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.releaseNotes[j].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }
                this.releaseNotesData.push({
                  description: data.data.releaseNotes[j].description,
                  index: j,
                  file_name: data.data.releaseNotes[j].file_name,
                  issueId: data.data.releaseNotes[j].issueId,
                  probability: data.data.releaseNotes[j].probability,
                  severity: data.data.releaseNotes[j].severity,
                  workaround: data.data.releaseNotes[j].workaround,
                  key: data.data.releaseNotes[j].key,
                  upvotedUsers: upvotedUsers
                });
              }

              for (var k = 0; k < data.data.fsb.length; k++) {
                if (data.data.fsb[k].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.fsb[k].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }
                this.fsbData.push({
                  FSBNumber: data.data.fsb[k].FSBNumber,
                  index: k,
                  dateCreated: data.data.fsb[k].dateCreated,
                  dateRevised: data.data.fsb[k].dateRevised,
                  issueId: data.data.fsb[k].issueId,
                  description: data.data.fsb[k].description,
                  file_name: data.data.fsb[k].file_name,
                  probability: data.data.fsb[k].probability,
                  rootCause: data.data.fsb[k].rootCause,
                  symptoms: data.data.fsb[k].symptoms,
                  title: data.data.fsb[k].title,
                  key: data.data.fsb[k].key,
                  upvotedUsers: upvotedUsers
                });
              }
              console.log("asdasd", this.devTrackData);
              if (data.data.devTrack.length > 0) {
                this.analyzeFlag = true;
              } else {
                this.analyzeFlag = true;
                this.devTrackFlag = true;
              }
              this.getTestPlan();
              this.getMopPlan();
              this.getTechNotes();
            } else {
              this.isLoading = false;
              swal({
                title: "Error",
                text: "Some Network Issues.Please Try After Sometime ",
                icon: "error"
              });
            }
            console.log("data -- response-->", data);
            this.mlKeywords = "";
            this.filterSynonym = "";
          });
        })
        .catch(handleError => {
          this.isLoading = false;
          if (
            handleError.message === "Failed to fetch" ||
            handleError.message === "Internal Server Error"
          ) {
            swal({
              title: "Error",
              text: "Something Went Wrong.Please Try After Sometime ",
              icon: "error"
            });
          }
          console.log(" Error Response ------->", handleError);
        });
    },

    getTestPlan() {
      this.isLoading = true;
      this.testPlanData = [];
      this.problemDescription = this.problemDescription.replace(
        /^\s+|\s+$/g,
        ""
      );
      fetch(
        constant.ELKURL +
          "api/get_test_plan?search_param=" +
          this.problemDescription,
        {
          method: "GET",
          headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
              let array = [];
              var upvotedUsers = [];
              for (let i = 0; i < data.data.test_plan.length; i++) {
                if (data.data.test_plan[i].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.test_plan[i].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }

                let tempJson = {
                  Objective: data.data.test_plan[i].Objective,
                  index: i,
                  Procedure: data.data.test_plan[i].Procedure,
                  file_name: data.data.test_plan[i].file_name,
                  probability: data.data.test_plan[i].probability,
                  key: data.data.test_plan[i].key,
                  upvotedUsers: upvotedUsers
                };

                if (typeof data.data.test_plan[i].setup !== "undefined") {
                  tempJson["setup"] = data.data.test_plan[i].setup;
                }
                if (
                  typeof data.data.test_plan[i].expectedResult !== "undefined"
                ) {
                  tempJson["expectedResult"] =
                    data.data.test_plan[i].expectedResult;
                }

                this.testPlanData.push(tempJson);
                tempJson = {};
              }
              this.isLoading = false;
            } else {
              this.isLoading = false;
              swal({
              title: "Error",
              text: "Something Went Wrong.Please Try After Sometime ",
              icon: "error"
            });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    getMopPlan() {
      this.isLoading = true;
      this.mopData = [];
      this.problemDescription = this.problemDescription.replace(
        /^\s+|\s+$/g,
        ""
      );
      fetch(
        constant.ELKURL + "api/get_mop?search_param=" + this.problemDescription,
        {
          method: "GET",
          headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
              let array = [];
              var upvotedUsers = [];
              for (let i = 0; i < data.data.mop.length; i++) {
                if (data.data.mop[i].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.mop[i].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }

                let tempJson = {
                  introduction: data.data.mop[i].introduction,
                  index: i,
                  title: data.data.mop[i].title,
                  file_name: data.data.mop[i].file_name,
                  probability: data.data.mop[i].probability,
                  key: data.data.mop[i].key,
                  upvotedUsers: upvotedUsers
                };
                this.mopData.push(tempJson);
                tempJson = {};
              }
              this.isLoading = false;
            } else {
              this.isLoading = false;
              swal({
              title: "Error",
              text: "Something Went Wrong.Please Try After Sometime ",
              icon: "error"
            });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    getTechNotes() {
      this.isLoading = true;
      this.techNotesData = [];
      this.problemDescription = this.problemDescription.replace(
        /^\s+|\s+$/g,
        ""
      );
      fetch(
        constant.ELKURL +
          "api/get_technotes?search_param=" +
          this.problemDescription,
        {
          method: "GET",
          headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
              let array = [];
              var upvotedUsers = [];
              for (let i = 0; i < data.data.technotes.length; i++) {
                if (data.data.technotes[i].upvotedUsers !== undefined) {
                  upvotedUsers = data.data.technotes[i].upvotedUsers;
                } else {
                  upvotedUsers = [];
                }

                let tempJson = {
                  description: data.data.technotes[i].description,
                  index: i,
                  file_name: data.data.technotes[i].file_name,
                  issueId: data.data.technotes[i].issueId,
                  probability: data.data.technotes[i].probability,
                  references: data.data.technotes[i].references,
                  key: data.data.technotes[i].key,
                  upvotedUsers: upvotedUsers
                };
                this.techNotesData.push(tempJson);
                tempJson = {};
              }

              this.isLoading = false;
            } else {
              this.isLoading = false;
              swal({
              title: "Error",
              text: "Something Went Wrong.Please Try After Sometime ",
              icon: "error"
            });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },

    changeFilter() {
      this.filterFLag = !this.filterFLag;
    },
    getMlKeywords() {
      this.isLoading = true;
      this.mlKeywords = "";
      this.filterSynonym = "";
      this.filterOptions = [];
      this.filterValue = [];
      //this.tagValue = [];
      this.tagOptions = [];
      fetch(
        constant.ELKURL +
          "api/get_ml_keywords?search_param=" +
          this.problemDescription,
        {
          headers: {
            Authorization:
              "Bearer " + localStorage.getItem("auth0_access_token")
          }
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
              this.isLoading = false;
              let count = 0;
              for (var i = 0; i < data.ml_keywords.length; i++) {
                this.filterOptions.push({
                  name: data.ml_keywords[i]
                });
                this.filterValue.push({
                  name: data.ml_keywords[i]
                });
                console.log("count ----->", count);
              }
              for (var j = 0; j < data.ml_synonym.length; j++) {
                if (this.checked) {
                  this.filterSynonym =
                    this.filterSynonym + " AND " + data.ml_synonym[j];
                } else {
                  this.filterSynonym =
                    this.filterSynonym + " OR " + data.ml_synonym[j];
                }
              }
              this.onAnalyze();
              this.searchFlag = true;
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    getCurrentUser(userList) {
      var localList = [];
      var userFlag = false;
      for (var i = 0; i < userList.length; i++) {
        if (userList[i] === this.currentUserEMailId) {
          localList.push(this.currentUserEMailId);
          userFlag = true;
        }
      }
      if (!userFlag) {
        localList.push(userList[0]);
      }
      return localList;
    },
    addTag(newTag) {
      const tag = {
        name: newTag,
        value: newTag
      };
      this.tagOptions.push(tag);
      this.tagValue.push(tag);
    },
    hideModal() {
      this.$modals.myModal.$hide();
    },

    logout() {
      console.log("logout");
      router.push("/");
      localStorage.clear();
    },
    routeDashboard() {
      router.push("/");
    },
    updatedVote(item, type) {
      console.log("-----------------", item);
      // item.updatedUsers = []
      item.upvotedUsers.push(this.currentUserEMailId);
      console.log("dev track", item);
      if (type === "devtrack") {
        this.postDevTrackData(item);
      } else if (type === "releasenotes") {
        this.postReleaseNotesData(item);
      } else if (type === "testplan") {
        this.postTestPlanData(item);
      } else if (type === "fsb") {
        this.postFsbData(item);
      } else if (type === "mop") {
        this.postMopData(item);
      } else if (type === "techNotes") {
        this.postTechNotesData(item);
      }
    },
    downVote(item, type) {
      // item.upvotedUsers.push(this.userName);

      item.upvotedUsers.pop(this.currentUserEMailId);
      console.log(item);
      if (type === "devtrack") {
        this.postDevTrackData(item);
      } else if (type === "releasenotes") {
        this.postReleaseNotesData(item);
      } else if (type === "testplan") {
        this.postTestPlanData(item);
      } else if (type === "fsb") {
        this.postFsbData(item);
      } else if (type === "mop") {
        this.postMopData(item);
      } else if (type === "techNotes") {
        this.postTechNotesData(item);
      }
    },

    filterDevTrackData(devTrackList) {
      console.log(devTrackList);
      var tempList = [];
      for (var i = 0; i < devTrackList.length; i++) {
        if (devTrackList[i].probability > 80) {
          tempList.push(devTrackList[i]);
        }
      }
      return tempList;
    },

    postDevTrackData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/getDevTrackData", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    postReleaseNotesData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/get_release_notes", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    postFsbData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/get_fsb", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    postTestPlanData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/get_test_plan", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          this.isLoading = false;
          if (handleError.message === "Failed to fetch") {
            swal({
              title: "Error",
              text: "Something Went Wrong.Please Try After Sometime ",
              icon: "error"
            });
          }
          console.log(" Error Response ------->", handleError);
        });
    },
    postMopData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/get_mop", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    postTechNotesData(item) {
      let formData = new FormData();
      formData.append("data", JSON.stringify(item));
      fetch(constant.ELKURL + "api/get_technotes", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            if (data.code === "token_expired") {
              this.logout();
            }
            if (data.http_status_code === 200) {
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
    },
    clearAll(param) {
      if (param === "product") {
        this.productValue = [];
      } else if (param === "group") {
        this.groupValue = [];
      } else if (param === "foundInRelease") {
        this.foundInReleaseValue = [];
      } else if (param === "fixedInRelease") {
        this.fixedInReleaseValue = [];
      } else if (param === "severity") {
        this.severityValue = [];
      } else if (param === "priority") {
        this.priorityValue = [];
      } else if (param === "foundOnPlatform") {
        this.foundOnPlatformValue = [];
      }
      this.getMlKeywords();
    },
    selectAll(param) {
      if (param === "product") {
        this.productValue = this.productOptions;
      } else if (param === "group") {
        this.groupValue = this.groupOptions;
      } else if (param === "foundInRelease") {
        this.foundInReleaseValue = this.foundInReleaseOptions;
      } else if (param === "fixedInRelease") {
        this.fixedInReleaseValue = this.fixedInReleaseOptions;
      } else if (param === "severity") {
        this.severityValue = this.severityOptions;
      } else if (param === "priority") {
        this.priorityValue = this.priorityOptions;
      } else if (param === "foundOnPlatform") {
        this.foundOnPlatformValue = this.foundOnPlatformOptions;
      }
    },
    showAll() {
      this.moreFlag1 = true;
    },
    showAbove80() {
      this.moreFlag1 = false;
    },
    showAllRl() {
      this.moreFlag2 = true;
    },
    showAbove80Rl() {
      this.moreFlag2 = false;
    },
    showAllTestPlan() {
      this.moreFlag4 = true;
    },
    showAllTechNotes() {
      this.moreFlag6 = true;
    },
    showAllMop() {
      this.moreFlag5 = true;
    },
    showAbove80TestPlan() {
      this.moreFlag4 = false;
    },
    showAbove80Mop() {
      this.moreFlag5 = false;
    },
    validateProductSelect() {
      if (this.productValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateProductClose() {
      this.isLoading = true;
      setTimeout(() => this.onAnalyze(), 1000);
    },
    validateGroupSelect() {
      if (this.groupValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateGroupClose() {
      this.isLoading = true;

      setTimeout(() => this.onAnalyze(), 1000);
    },
    validateSeveritySelect() {
      if (this.severityValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateSeverityClose() {
      this.isLoading = true;

      setTimeout(() => this.onAnalyze(), 1000);
    },
    validatePrioritySelect() {
      if (this.priorityValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validatePriorityClose() {
      setTimeout(() => this.onAnalyze(), 1000);
    },
    validateFoundInReleaseSelect() {
      //setTimeout(() => this.onAnalyze(), 1000);
      if (this.foundInReleaseValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateFoundInReleaseClose() {
      setTimeout(() => this.onAnalyze(), 1000);
    },
    validateFixedInReleaseSelect() {
      if (this.fixedInReleaseValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateFixedInReleaseClose() {
      setTimeout(() => this.onAnalyze(), 1000);
    },
    validateServiceAccountSelect() {
      if (this.fixedInReleaseValue.length !== 0) {
        this.onAnalyze();
      }
    },
    validateServiceAccountClose() {
      setTimeout(() => this.onAnalyze(), 1000);
    },
    showAllfsb() {
      this.moreFlag3 = true;
    },
    showAbove80fsb() {
      this.moreFlag3 = false;
    },
    problemDescriptionChange() {
      if (this.problemDescription.trim() === "") {
        this.searchFlag = false;
      }
    }
  }
};
0;
</script>
  <style>
.container {
  width: 100% !important;
  height: 100%;
}

/* For cursor Pointer Change to Hand Icon */

.align {
  padding: 0.75em;
}
.alignButton {
  padding: 1.5em;
}
.myBreadCrumb {
  margin-top: -2%;
}
.align-rl {
  padding-left: 8em;
}

.align-margin {
  margin-left: 3em;
  margin-right: 3em;
}
.tags {
  color: #495057 !important;
  font-size: 1rem !important;
  border: 1px solid #ced4da !important;
  border-radius: 0.25rem !important;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out !important;
}

::input-placeholder {
  opacity: 10;
  color: brown;
  font-weight: lighter;
}

.in-progress {
  cursor: pointer;
}
.vue-tooltip {
  background-color: white;
  color: #71869e;
}
.contentwidth {
  width: 80%;
}
.vudal {
  width: 950px !important;
  text-align: left !important;
}
.textOverlay {
  word-break: break-all;
  white-space: pre-wrap;
  text-align: left;
}

.all-success {
  font-size: 0.63em !important;
  color: #169f85;
  letter-spacing: 0.063em;

  border: 0.125em solid #169f85;
  border-radius: 2.5em;
  background: transparent;
  transition: all 0.3s ease 0s;
}
.textWithSpace {
  white-space: pre-wrap;
}
.all-success:hover {
  color: #fff;
  background: #169f85;
  border: 2px solid #169f85;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to
/* .fade-leave-active in <2.1.8 */
 {
  opacity: 0;
}

.navHeaderColor {
  color: #495057;
}

.labelweight {
  font-weight: 600;
}
.labelweightIssueId {
  font-weight: 900;
}
.row-one {
  padding-top: 5%;
}
</style>
