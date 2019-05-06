  <template>
    <div>
      <headernav msg="SolutionScreen"/>
      <side-nav/>
<Loading :active="isLoading" 
        :can-cancel="false" 
        color=#15ba9a
        ></Loading>

      <vudal name="myModal">
        <div class="header">
          <div class="row">
            <div class="col-lg-11">
              <h4 v-if="patchFlag">{{solutionScreenConstants.modalHeader}}</h4>
            </div>
            <div class="col-lg-1 in-progress" @click="hideModal()">
              <i class="fa fa-times fa-md pull-right"  aria-hidden="true" ></i>
            </div>
          </div>
          
        
        
        </div>
        <div class="content contentwidth">
          <div class="row">
              <div class="col-lg-5 " v-if="devTrackFlag">
                <label class="labelweightIssueId"> Issue Id:</label>
              </div>
              <div class="col-lg-7 "  v-if="devTrackFlag">
                <span class="col-lg-5 labelweightIssueId">{{devTrackContent.issueId}}</span>
              </div>
            </div>
          <nav  v-if="devTrackFlag"> 
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
          <div class="tab-content" id="nav-tabContent "  v-if="devTrackFlag">

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

          <div v-if="releaseNotesFlag"
            >
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
             <div v-if="releaseNoteContent.workaround !==' ' ">
            <label class="labelweight">Workaround :</label>
            <br>
            <span class="textOverlay">{{releaseNoteContent.workaround}}</span>
            </div>
          </div>

          <div v-if="fsbFlag"
            >
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

      <div class="custom-container" >
        <div class="row-one" >
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
            </div> -->
                <div class="row align">
                  <label class="col-md-6 labelweight">{{solutionScreenConstants.problemDescriptionName}}</label>
                  <label class="col-md-6 labelweight">{{solutionScreenConstants.problemAreaHeader}}</label>
                </div>

                <div class="row ">
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
                    <div class="row">
                      <div class="col-lg-10"></div>
                    <div class="col-lg-2 alignButton" >
                    <button
                      v-if="problemDescription !== ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="getMlKeywords()"
                    >{{solutionScreenConstants.buttons[0]}}</button>
                    <button
                      v-if="problemDescription === ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="getMlKeywords()"
                      disabled
                    >{{solutionScreenConstants.buttons[0]}}</button>
                  </div>
                    </div>
                  </div>
                  <div class="col-md-6"> 
                  <div class="row">
                    <div class="col-md-9">
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
                    <br/>
                    
                    <div class="col-lg-3" style="marginTop:2%">
                        <input type="checkbox" id="checkbox" v-model="checked">
                        <label for="checkbox" >{{solutionScreenConstants.checkBoxLabel}}</label>
                    </div>
                   
                    <label class="col-md-6 labelweight align">{{solutionScreenConstants.tagHeader}}</label>
                    
                    <div class="col-md-10 ">
                      
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
                    <div class="col-lg-2" style="paddingTop:0.35em" >
                    <button
                      v-if="searchFlag "
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="onAnalyze()"
                    >{{solutionScreenConstants.buttons[2]}}</button>
                    <button
                      v-if="!searchFlag "
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
                    <!-- <div class="row" style="paddingTop:0.45em"> 
                      <div class="col-lg-5"></div>
                      <div class="col-lg-1" >
                    <button
                      v-if="problemDescription !== ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="getMlKeywords()"
                    >{{solutionScreenConstants.buttons[0]}}</button>
                    <button
                      v-if="problemDescription === ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="getMlKeywords()"
                      disabled
                    >{{solutionScreenConstants.buttons[0]}}</button>
                  </div>
                  <div class="col-lg-5"></div>
                  <div class="col-lg-1" >
                    <button
                      v-if="searchFlag "
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="onAnalyze()"
                    >{{solutionScreenConstants.buttons[2]}}</button>
                    <button
                      v-if="!searchFlag "
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="onAnalyze()"
                      disabled
                    >{{solutionScreenConstants.buttons[2]}}</button>
                  </div>
                  </div> -->
                   
                
                  
                
                <!-- <div class="row">
                  <div class="col-lg-10"></div>
                  <div class="col-lg-2">
                    <button
                      v-if="problemDescription !== ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="onAnalyze()"
                    >{{solutionScreenConstants.buttons[0]}}</button>
                    <button
                      v-if="problemDescription === ''"
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block"
                      @click="onAnalyze()"
                      disabled
                    >{{solutionScreenConstants.buttons[0]}}</button>
                  </div>
                </div> -->
              </div>
            </div>
          </div>
        </div>




        <div class="row" style="textAlign:center" v-if="analyzeFlag">
          <div class="col-lg-12">
            <div class="row  ">
            
            <!-- <div class="col-lg-3" >
                <div class="card  shadow p-2 mb-5  rounded" >
                  <div class="card-body in-progress labelweight cardFontChange"
                  > <span class="float-left">Total Hits</span>
                  <span class="float-right">{{estotalhits}}</span> </div>
                </div>
              </div> -->

              <div class="col-lg-4" >
                <div class="card  shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b1color , color:textcolor1}">
                  <div class="card-body in-progress labelweight cardFontChange"
                  @click="showDevTrack()"> <span class="float-left">{{solutionScreenConstants.cardLables[0]}}</span>
                  <span class="float-right">{{this.devTrackData.length}}</span> </div>
                </div>
              </div>
              
              <div class="col-lg-4">
                <div class="card shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b2color , color:textcolor2}">
                  <div class="card-body in-progress labelweight cardFontChange"
                  @click="showReleaseNotes()">
                  <span class="float-left">{{solutionScreenConstants.cardLables[1]}}</span>
                  <span class="float-right">{{this.releaseNotesData.length}}</span> </div>
                </div>
              </div>
              
              <div class="col-lg-4">
                <div class="card shadow p-2 mb-5  rounded" v-bind:style="{ backgroundColor: b3color , color:textcolor3}">
                  <div class="card-body in-progress labelweight cardFontChange"
                  v-bind:style="{ backgroundColor: b3color }"
                  @click="showFSB()"><span class="float-left">{{solutionScreenConstants.cardLables[2]}}</span>
                  <span class="float-right">{{this.fsbData.length}}</span> </div>
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
                <div class="row align">
                  <div class="col-lg-4">
                    <div class="row">
                      <div class="col-lg-4">{{solutionScreenConstants.filterNames[0]}}</div>
                      <div class="col" align="right">
                        <button
                          style="fontSize:1vw;"
                          type="button"
                          class="all-success"
                          @click="selectAll('product')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                      ></Multiselect>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    <div class="row ">
                      <div class="col-lg-4">{{solutionScreenConstants.filterNames[1]}}</div>
                      <div class="col" align="right">
                        <button
                          style="fontSize:1vw;"
                          type="button"
                          class="all-success"
                          @click="selectAll('group')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                          @click="selectAll('severity')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                          @click="selectAll('priority')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                      ></Multiselect>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    <div class="row">
                      <div class="col-lg-5">{{solutionScreenConstants.filterNames[4]}}</div>
                      <div class="col" align="right">
                        <button
                          style="fontSize:1vw;"
                          type="button"
                          class="all-success"
                          @click="selectAll('foundOnPlatform')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

                        <button
                          style="fontSize:1vw;"
                          type="button"
                          class="all-success"
                          @click="clearAll('foundOnPlatform')"
                        >
                          <i class="fas fa-minus-circle"></i>
                          &nbsp; {{solutionScreenConstants.filterButtons[1]}}
                        </button>
                      </div>
                    </div>
                    <div style="paddingTop:0.5em">
                       <Multiselect
                        v-model="foundOnPlatformValue"
                        tag-placeholder="Add this as new tag"
                        placeholder="Search Found On Platform"
                        label="name"
                        track-by="name"
                        :options="foundOnPlatformOptions"
                        :multiple="true"
                        :taggable="true"
                        :clear-on-select="false"
                        :close-on-select="false"
                        :hide-selected="true"
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
                          @click="selectAll('fixedInRelease')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                      ></Multiselect>
                    </div>
                  </div>
                </div>
                <div class="row align">
                  <div class="col-lg-4">
                    <div class="row">
                      <div class="col-lg-6">{{solutionScreenConstants.filterNames[6]}}</div>
                      <div class="col" align="right">
                        <button
                          style="fontSize:1vw;"
                          type="button"
                          class="all-success"
                          @click="selectAll('foundInRelease')"
                        >
                          <i class="fas fa-check-circle"></i>
                          &nbsp;{{solutionScreenConstants.filterButtons[0]}}
                        </button>

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
                      ></Multiselect>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    <div class="row">
                      <div class="col-lg-12">{{solutionScreenConstants.filterNames[7]}}</div>
                    
                    </div>
                    <div >
                      <date-picker style="height:40px;paddingTop:1.1em" v-model="time1" lang="en" valueType="format" :format="format" :first-day-of-week="1"  @change="showTime()"></date-picker>
                    </div>
                  </div>
                  <div class="col-lg-4">
                    
                    <div class="row">
                      
                      <div class="col-lg-9"></div>
                      <div class="col-lg-3" style="marginTop:8%">
                      <button
                      v-if="searchFlag "
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block pull-right"
                      @click="onAnalyze()"
                    >{{solutionScreenConstants.buttons[2]}}</button>
                    <button
                      v-if="!searchFlag "
                      style="fontSize:0.75vw;"
                      type="button"
                      class="btn btn-success btn-block pull-right"
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
        </transition>
        <br>
        <div class=" align card   p-2 mb-5  rounded text-center" v-if="errorFlag" >
         
        </div>
        <div class="row" v-if="devTrackFlag" style="marginTop:-1.8%">
            <div class="col-lg-12">
              <div class="p-3 mb-3 bg-white">
                <!-- <div class="row">
                
                  <div class="col-md-10">
                  <h5 align="left" >Dev Track</h5>
                  </div>
              </div> -->

                <div class="row align">
                  <div class="col-md-12" align="center">
                <table  class="table responsive table-hover">
                  <thead class="text-center">
                    <th >{{solutionScreenConstants.tableHeaders[0]}}</th>
                    <th style="width: 45.66%">{{solutionScreenConstants.tableHeaders[1]}}</th>
                    <th >{{solutionScreenConstants.tableHeaders[2]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[3]}}</th>
                    <th>{{solutionScreenConstants.tableHeaders[4]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[5]}}</th>
                    <th style="width: 10%">{{solutionScreenConstants.tableHeaders[6]}}</th>
                  </thead>
                  <tbody v-if ="devTrackData.length >0 && moreFlag1" class="text-center">
                    <tr v-for="item in devTrackData" :key="item.index"
                    >
                    <td @click="showPatchModal(item.index)" class=" in-progress">
                      {{item.issueId}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.title}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.severity}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.fixedinRelease}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.dateSubmitted}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        <td v-if="item.upvotedUsers.length>0" >
                          
                          <span  v-for="(userFlag, index)  in  getCurrentUser(item.upvotedUsers)" :key="index" >
                            <!-- <p>SSDSD {{userFlag}}</p> -->
                             <i  v-if="userFlag !== currentUserEMailId" @click="updatedVote(item)" class="far fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i>
                             <i  v-if="userFlag === currentUserEMailId" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> 
                             &nbsp;{{item.upvotedUsers.length}}
                          </span>
                        </td>

                        <td v-else>
                          
                          <i class="far fa-thumbs-up " @click="updatedVote(item)" style="cursor:pointer;color:#293f55;"></i>&nbsp;{{item.upvotedUsers.length}}
                          <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                        </td>
                      </tr>
                  </tbody>

                   <tbody v-if ="devTrackData.length >0 && !moreFlag1" class="text-center">
                    <tr v-for="item in filterDevTrackData(devTrackData)" :key="item.index"
                    >
                    <td @click="showPatchModal(item.index)" class=" in-progress">
                      {{item.issueId}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.title}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.severity}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.fixedinRelease}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.dateSubmitted}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        <td v-if="item.upvotedUsers.length>0" >
                          
                          <span  v-for="(userFlag, index)  in  item.upvotedUsers" :key="index" >
                            <!-- <p>SSDSD {{userFlag}}</p> -->
                             <i  v-if="userFlag !== currentUserEMailId" @click="updatedVote(item)" class="far fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i>
                             <i  v-if="userFlag === currentUserEMailId" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> 
                             &nbsp;{{item.upvotedUsers.length}}
                          </span>
                        </td>

                        <td v-else>
                          
                          <i class="far fa-thumbs-up " @click="updatedVote(item)" style="cursor:pointer;color:#293f55;"></i>&nbsp;{{item.upvotedUsers.length}}
                          <!-- <i  v-if="item.voteFlag" @click="downVote(item)" class="fas fa-thumbs-up " style="cursor:pointer;color:#293f55;"></i> -->
                        </td>
                      </tr>
                  </tbody>
                </table>
                 <div v-if ="devTrackData.length>0 && !moreFlag1" class="text-centered in-progress" @click="showAll()">
                  More
                </div>
                <!-- <div v-if ="devTrackData.length>0 && moreFlag" class="text-centered" @click="showAbove80()">
                  Hide
                </div> -->
                <div v-if ="devTrackData.length==0" class="text-centered">
                  No Data
                </div>
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
                <table  class="table responsive table-hover">
                  <thead class="text-center">
                    <th >Issue Id</th>
                    <th >File Name</th>
                    <th >Severity</th>
                    
                     <th style="width: 10%">Confidence (%)</th>
                    
                   
                  </thead>
                  <tbody  class="text-center" v-if ="releaseNotesData.length >0 && moreFlag2">
                    <tr v-for="item in releaseNotesData" :key="item.index"
                    >
                    <td  class=" in-progress" @click="showPatchModal(item.index)">
                      {{item.issueId}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.file_name}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.severity}}</td>
                        
                        
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        
                      </tr>
                  </tbody>

                  <tbody  class="text-center" v-if ="releaseNotesData.length >0 && !moreFlag2">
                    <tr v-for="item in filterDevTrackData(releaseNotesData)" :key="item.index"
                    >
                    <td  class=" in-progress" @click="showPatchModal(item.index)">
                      {{item.issueId}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.file_name}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.severity}}</td>
                        
                        
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        
                      </tr>
                  </tbody>

                   
                </table>
                  <div v-if ="releaseNotesData.length>0 && !moreFlag2" class="text-centered in-progress" @click="showAllRl()">
                  More
                </div> 
                 <!-- <div v-if ="releaseNotesData.length>0 && moreFlag2" class="text-centered" @click="showAbove80Rl()">
                  Hide
                </div>  -->
                <div v-if ="releaseNotesData.length==0" class="text-centered">
                  No Data
                </div> 
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
                <table  class="table responsive table-hover">
                  <thead class="text-center">
                    <th >FSBNumber</th>
                    <th >Issue Id</th>
                    <th >File Name</th>
                    <th >Date Created</th>
                    
                     <th >Title</th>
                      <th style="width: 10%">Confidence (%)</th>
                
                    
                   
                  </thead>
                  <tbody  class="text-center" v-if ="fsbData.length >0 && moreFlag3">
                    <tr v-for="item in fsbData" :key="item.index"
                    >
                    <td  class=" in-progress" @click="showPatchModal(item.index)">
                      {{item.FSBNumber}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.issueId}}</td>
                       
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.file_name}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.dateCreated}}</td>
                        <!-- <td class=" in-progress" @click="showPatchModal(item.index)">{{item.symptoms}}</td> -->
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.title}}</td>

                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        
                      </tr>
                  </tbody>

                  <tbody  class="text-center" v-if ="fsbData.length >0 && !moreFlag3">
                    <tr v-for="item in filterDevTrackData(fsbData)" :key="item.index"
                    >
                    <td  class=" in-progress" @click="showPatchModal(item.index)">
                      {{item.FSBNumber}}</td>
                      <td class=" in-progress" @click="showPatchModal(item.index)">{{item.issueId}}</td>
                       
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.file_name}}</td>
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.dateCreated}}</td>
                        <!-- <td class=" in-progress" @click="showPatchModal(item.index)">{{item.symptoms}}</td> -->
                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.title}}</td>

                        <td class=" in-progress" @click="showPatchModal(item.index)">{{item.probability}}</td>

                        
                      </tr>
                  </tbody>

                   
                </table>
                  <div v-if ="fsbData.length>0 && !moreFlag3" class="text-centered in-progress" @click="showAllfsb()">
                  More
                </div> 
                 <!-- <div v-if ="fsbData.length>0 && moreFlag3" class="text-centered" @click="showAbove80fsb()">
                  Hide
                </div>  -->
                <div v-if ="fsbData.length==0" class="text-centered">
                  No Data
                </div> 
              </div>
                  </div>

                  
                
              
              </div>
            </div>
          </div>

        </div>




        
        <div>
          <!-- Footer -->
        <footer class="footer  font-small blue">
          <!-- Copyright -->
          <div class="footer-copyright text-center py-3">Powered By Ekryp</div>
          <!-- Copyright -->
        </footer>
          <!-- Footer -->
        </div>
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
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  import * as solutionFilterData from "../../utilies/solutionfiltersample.json";
  import DatePicker from 'vue2-datepicker'
  //import * as data from "../../utilies/tabledata.json";

  export default {
    name: "MockUpNew",
    components: {
      SideNav,
      headernav,
      Multiselect,
      tagsinput,
      Vudal,
      DatePicker ,
      Loading
    },
    created() {
      clearInterval(window.intervalObj);
      this.currentUserEMailId=localStorage.getItem("email_id");
      // this.tagOptions.push({name:'Issue ID',value:'issueId'});
      // this.tagOptions.push({name:'Title',value:'title'});
      // this.tagOptions.push({name:'Current Owner',value:'currentOwner'});
      // this.tagOptions.push({name:'Progress Status',value:'progressStatus'});
      // this.tagOptions.push({name:'Group',value:'group'});
      // this.tagOptions.push({value:'severity',name:'Severity'});
      // this.tagOptions.push({value:'dateSubmitted',name:'Date Submitted'});
      // this.tagOptions.push({value:'submittedBy',name:'Submitted By'});
      // this.tagOptions.push({value:'description',name:'Description'});
      // this.tagOptions.push({value:'foundInBuild',name:'Found in Build'});
      // this.tagOptions.push({value:'tragetRelease',name:'Target Release'});
      // this.tagOptions.push({value:'dateClosed',name:'Date Closed'});
      // this.tagOptions.push({value:'hwPON',name:'HW PON'});
      // this.tagOptions.push({value:'caseReason',name:'Case Reason'});
      // this.tagOptions.push({value:'finalTestRootCauseAnalysisComments',name:'Final Test Root Cause Analysis Comments'});
      // this.tagOptions.push({name:'Priority',value:'priority'});
      // this.tagOptions.push({name:'Found on Platform',value:'foundOnPlatform'});
      // this.tagOptions.push({name:'Problem Description/Systems Impacted',value:'problemDescriptionImpacted'});
      // this.tagOptions.push({name:'Workaround',value:'workaround'});
      // this.tagOptions.push({name:'Symptoms',value:'symptoms'});
      // this.tagOptions.push({name:'Reporting Customer',value:'reportingCustomer'});
      // this.tagOptions.push({name:'Service Account',value:'serviceAccount'});
      // this.tagOptions.push({name:'Fixed in Release',value:'fixedinRelease'});
      // this.tagOptions.push({name:'Found in Release',value:'Found in Release'});
      // this.tagOptions.push({name:'Resolution',value:'resolution'});  
      // this.tagOptions.push({name:'Product',value:'product'});
    },
    data() {
      console.log("dashboard", this.data);
      return {
        isLoading: false,
        tags: [],
        solutionScreenConstants: constant.SolutionScreen,
        showGreen: true,
        checked:false,
        filterFLag:false,
        searchFlag:false,
        devTrackData: [],
        releaseNotesData:[],
        fsbData:[],
        errorFlag: false,
        tarFileName: "",
        tarFile: "",
        b1color: "",
        b2color: "",
        b3color: "",
        format:"DD-MM-YYYY",
        textcolor1:"",
        textcolor2:"",
        textcolor3:"",
        rl1color: "",
        rl2color: "",
        moreFlag1:false,
        moreFlag2:false,
        moreFlag3:false,
        currentUserEMailId:"",
        devTrackContent: "",
        releaseNoteContent: "",
        fsbContent: "",
        filterOptions:[],
        filterValue:[],
        tagValue:[],
        tagOptions:[],
        productValue: [],
        
        time1:"",
        productOptions: solutionFilterData.productValues,
        groupValue: [],
        groupOptions: solutionFilterData.group,
        severityValue: [],
        severityOptions: solutionFilterData.severity,
        priorityValue: [],
        priorityOptions: solutionFilterData.priority,
        foundOnPlatformValue:[],
        foundOnPlatformOptions: solutionFilterData.foundOnPlatform,
        fixedInReleaseValue: [],
        fixedInReleaseOptions: solutionFilterData.fixedInRelease,
        foundInReleaseValue: [],
        foundInReleaseOptions: solutionFilterData.foundInRelease,
        problemDescriptionPlaceholder: "Enter the Problem Description",
        valueIndex: "",
        filterURL:"",
        releaseFlag: true,
        patchFlag: false,
        problemDescription: "",
        analyzeFlag: false,
        devTrackFlag: false,
        releaseNotesFlag: false,
        fsbFlag: false,
        errorFlag:false,
        sdfcFlag: false,
        mlKeywords:"",
        estotalhits: 0,
        filterValues:""
      };
    },
    methods: {
      showTime()
      {
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
        showDevTrack(){
            this.devTrackFlag=true;
            this.releaseNotesFlag=false;
          this.fsbFlag=false;
            this.b1color="#2a629a";
            this.textcolor1="#f8f9fa";
            this.b2color="";
            this.textcolor2="";
            this.b3color="";
            this.textcolor3="";

        },
        showPatchModal(index) {
        this.patchFlag = true;
        
        this.devTrackContent=this.devTrackData[index];
        console.log(index)
         this.releaseNoteContent=this.releaseNotesData[index];
          this.fsbContent=this.fsbData[index];
       
        this.$modals.myModal.$show();
      },
        showReleaseNotes(){
          this.devTrackFlag=false;
          this.releaseNotesFlag=true;
          this.fsbFlag=false;
          this.b2color="#2a629a";
          this.textcolor2="#f8f9fa";
          this.b1color="";
          this.textcolor1="";
          this.b3color="";
          this.textcolor3="";
        },
        showFSB(){
          this.devTrackFlag=false;
          this.releaseNotesFlag=false;
            this.fsbFlag=true;
            this.b3color="#2a629a";
            this.textcolor3="#f8f9fa";
            this.b2color="";
            this.textcolor2="";
            this.b1color="";
            this.textcolor1="";
        },
        onAnalyze() {
        this.isLoading=true;
        this.errorFlag=false;
        this.devTrackData=[];
        this.releaseNotesData=[];
        this.fsbData=[];
        this.filterValues='';

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
          this.filterURL + `&found_in_release_filter=` + this.foundInReleaseValue[i].name;
      }
       for (var i = 0; i < this.fixedInReleaseValue.length; i++) {
        this.filterURL =
          this.filterURL + `&fixed_in_release_filter=` + this.fixedInReleaseValue[i].name;
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
          this.filterURL + `&found_on_platform_filter=` + this.foundOnPlatformValue[i].name;
      }
      if(this.time1 !=="")
      {
         this.filterURL =
          this.filterURL + `&date_filter=` + this.time1;
      }


        for(var i=0;i<this.tagValue.length;i++)
        {
          this.filterValues=this.filterValues+" AND "+this.tagValue[i].value;
        }
         if(this.filterValue.length>0)
         {
           if(this.checked)
           {
             this.mlKeywords="AND";
           }else{
              this.mlKeywords="OR";
           }
        
         }else{
           this.mlKeywords="";
         }
         for(var i=0;i<this.filterValue.length;i++)
         {
           this.mlKeywords=this.mlKeywords+" "+this.filterValue[i].name;
         }
      
        fetch(constant.ELKURL+"api/getDevTrackData?search_param="+this.problemDescription+" "+this.mlKeywords+this.filterValues+this.filterURL, {
        
        headers: {
          'Content-Type': 'application/json'
        }
        })
          .then(response => {
            response.text().then(text => {
              const data = text && JSON.parse(text);
              if (data.http_status_code === 200) {
                this.isLoading=false;
                this.estotalhits = data.data.totalhits
                console.log('estotal hits ----->',this.estotalhits)
                if(data.data.devTrack.length < 0){
                  this.analyzeFlag = true;
                }
                var upvotedUsers=[];
                for(var i=0;i<data.data.devTrack.length;i++)
                {
                  let upvotedUserFlag=false;
                  if(data.data.devTrack[i].upvotedUsers !== undefined)
                  {
                    upvotedUsers=data.data.devTrack[i].upvotedUsers;

                  }else{
                    upvotedUsers=[];
                  }
                  
                  
                this.devTrackData.push({issueId:data.data.devTrack[i].issueId,index:i,
                  description:data.data.devTrack[i].description,
                  severity:data.data.devTrack[i].severity,
                  caseReason:data.data.devTrack[i].caseReason,
                  currentOwner:data.data.devTrack[i].currentOwner,
                  dateClosed:data.data.devTrack[i].dateClosed,
                  dateSubmitted:data.data.devTrack[i].dateSubmitted,
                  finalTestRootCauseAnalysisComments:data.data.devTrack[i].finalTestRootCauseAnalysisComments,
                  fixedinRelease:data.data.devTrack[i].fixedinRelease,
                  foundInBuild:data.data.devTrack[i].foundInBuild,
                  foundOnPlatform:data.data.devTrack[i].foundOnPlatform,
                  group:data.data.devTrack[i].group,
                  product:data.data.devTrack[i].product,
                  probability:data.data.devTrack[i].probability,
                  progressStatus:data.data.devTrack[i].progressStatus,
                  reportingCustomer:data.data.devTrack[i].reportingCustomer,
                  resolution:data.data.devTrack[i].resolution,
                  serviceAccount:data.data.devTrack[i].serviceAccount,
                  submittedBy:data.data.devTrack[i].submittedBy,
                  symptoms:data.data.devTrack[i].symptoms,
                  title:data.data.devTrack[i].title,
                  tragetRelease:data.data.devTrack[i].tragetRelease,
                  type:data.data.devTrack[i].type,
                  workaround:data.data.devTrack[i].workaround,
                  upvotedUsers:upvotedUsers});
                  this.moreFlag1=false;
                  this.devTrackFlag=true;
                  this.b1color="#2a629a";
                  this.textcolor1="#f8f9fa";
                  this.b2color="";
                  this.textcolor2="";
                  this.b3color="";
                  this.textcolor3="";
                }

                for(var j=0;j<data.data.releaseNotes.length;j++)
                {
                  this.releaseNotesData.push({description:data.data.releaseNotes[j].description,
                  index:j,
                  file_name:data.data.releaseNotes[j].file_name,
                  issueId:data.data.releaseNotes[j].issueId,
                  probability:data.data.releaseNotes[j].probability,
                  severity:data.data.releaseNotes[j].severity,
                  workaround:data.data.releaseNotes[j].workaround
                  });
                }

                for(var k=0;k<data.data.fsb.length;k++)
                {
                  this.fsbData.push({FSBNumber:data.data.fsb[k].FSBNumber,
                  index:k,
                  dateCreated:data.data.fsb[k].dateCreated,
                  dateRevised:data.data.fsb[k].dateRevised,
                  issueId:data.data.fsb[k].issueId,
                  description:data.data.fsb[k].description,
                  file_name:data.data.fsb[k].file_name,
                  probability:data.data.fsb[k].probability,
                  rootCause:data.data.fsb[k].rootCause,
                  symptoms:data.data.fsb[k].symptoms,
                  title:data.data.fsb[k].title
                  });
                }
                console.log('asdasd',this.devTrackData);
                if(data.data.devTrack.length>0)
                {
                  this.analyzeFlag = true;
                }
                else{
                  

                  this.analyzeFlag = true;
                  this.devTrackFlag=true;
                
                  
                }
                
              } else {
                  this.isLoading=false;
              }
              console.log("data -- response-->", data);
              this.mlKeywords = "";
            });
          })
          .catch(handleError => {
            console.log(" Error Response ------->", handleError);
          });
      },

      changeFilter() {
        this.filterFLag = !this.filterFLag;
      },
      getMlKeywords()
      {
        this.isLoading = true;
        this.mlKeywords = '';
        this.filterOptions=[];
        this.filterValue=[];
        this.tagValue=[];
        this.tagOptions=[];
        fetch(constant.ELKURL + "api/get_ml_keywords?search_param="+this.problemDescription, {
          
          headers: {
            Authorization: "Bearer " + localStorage.getItem("auth0_access_token")
          }
        })
          .then(response => {
            response.text().then(text => {
              const data = text && JSON.parse(text);
              if(data.code === "token_expired")
              {
                this.logout();
              }
              if (data.http_status_code === 200) {
                this.isLoading=false;
                let count = 0
                for(var i=0;i<data.ml_keywords.length;i++)
                {
                  this.filterOptions.push({
                    name:data.ml_keywords[i]
                  });
                  this.filterValue.push({
                    name:data.ml_keywords[i]
                  });
                  console.log("count ----->",count)
                }
                for(var j=0;j<data.ml_synonym.length;j++)
                {
                  if(this.checked)
                  {
                    this.mlKeywords=this.mlKeywords+" AND "+data.ml_synonym[j];
                  }else{
                    this.mlKeywords=this.mlKeywords+" OR "+data.ml_synonym[j];
                  }
                  
                }
                this.onAnalyze();
                this.searchFlag=true;
              }
              
            });
          })
          .catch(handleError => {
            console.log(" Error Response ------->", handleError);
          });
      },
      getCurrentUser(userList)
      {
        var localList=[];
        var userFlag=false;
        for(var i=0;i<userList.length;i++)
        {
         if(userList[i]=== this.currentUserEMailId)
         {
           localList.push(this.currentUserEMailId);
           userFlag=true;
         }
        }
        if(!userFlag)
        {
          localList.push(userList[0]);
        }
        return localList;
      },
      addTag (newTag) {
        const tag = {
          name: newTag,
          value: newTag
        }
        this.tagOptions.push(tag)
        this.tagValue.push(tag)
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
      updatedVote(item){
        console.log("-----------------",item);
       // item.updatedUsers = []
        item.upvotedUsers.push(this.currentUserEMailId);
        console.log('dev track',item)
        this.postDevTrackData(item);
      },
      downVote(item)
      {
        
       // item.upvotedUsers.push(this.userName);
        
        item.upvotedUsers.pop(this.currentUserEMailId);
        console.log(item);
        this.postDevTrackData(item);

      },
      filterDevTrackData(devTrackList)
      {
        console.log(devTrackList);
        var tempList=[]
        for(var i=0;i<devTrackList.length;i++)
        {
          if(devTrackList[i].probability>80)
          {
            tempList.push(devTrackList[i]);
          }
        }
        return tempList;
      },
      
      postDevTrackData(item)
      {
         let formData = new FormData();
         formData.append("data",JSON.stringify(item));
         fetch(constant.ELKURL + "api/getDevTrackData", {
           method: 'PUT',
          body: formData
         }).then(response => {
             response.text().then(text => {
               const data = text && JSON.parse(text);
               if(data.code === "token_expired")
               {
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
      }
      else if (param === "foundInRelease") {
        this.foundInReleaseValue = [];
      }
      else if (param === "fixedInRelease") {
        this.fixedInReleaseValue = [];
      }
      else if (param === "severity") {
        this.severityValue = [];
      }
      else if (param === "priority") {
        this.priorityValue = [];
      }
      else if (param === "foundOnPlatform") {
        this.foundOnPlatformValue = [];
      }
    },
    selectAll(param) {

      if (param === "product") {
        this.productValue = this.productOptions;
      } else if (param === "group") {
        this.groupValue = this.groupOptions;
      }
      else if (param === "foundInRelease") {
        this.foundInReleaseValue = this.foundInReleaseOptions;
      }
      else if (param === "fixedInRelease") {
        this.fixedInReleaseValue = this.fixedInReleaseOptions;
      }
      else if (param === "severity") {
        this.severityValue = this.severityOptions;
      }
      else if (param === "priority") {
        this.priorityValue = this.priorityOptions;
      }
      else if (param === "foundOnPlatform") {
        this.foundOnPlatformValue = this.foundOnPlatformOptions;
      }
      
    },
      showAll(){
        this.moreFlag1=true;
      },
      showAbove80()
      {
        this.moreFlag1=false;
      },
       showAllRl(){
        this.moreFlag2=true;
      },
      showAbove80Rl()
      {
        this.moreFlag2=false;
      },
       showAllfsb(){
        this.moreFlag3=true;
      },
      showAbove80fsb()
      {
        this.moreFlag3=false;
      },
      problemDescriptionChange()
      {
        if(this.problemDescription === "")
        {
          this.searchFlag=false;
        }
      }
    }
  };
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
  .vudal{
        width: 950px !important;
  }
  .textOverlay {
    word-break: break-all;
    white-space:pre-wrap;
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
   .labelweightIssueId{
    font-weight: 900;
  }
  .row-one {
  padding-top: 5%;
}
  </style>
