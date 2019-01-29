<template>
    <div>
        <headernav :loaderFlag="loaderFlag"/>
        <side-nav/>

        <div class="custom-container" style="padding:3%; paddingTop:7.57%;marginLeft:4%">
      
        <div>
        <div class="myBreadCrumb" style="margin-bottom:1px">
          <p>
            <span class="in-progress" @click="redirectToAnalysis()">{{postMenu}}</span>
            <span style="font-size: 14px;">{{current}}</span>
          </p>
        </div>
      </div>
      
        <div class=" " >
    
    <vudal name="myModal">
  <div class="header">
    <i class="close icon"></i>
    {{this.title}}
  </div>
  <div class="content">
    <div class="form-group text-left" >
      
      <span v-for="(item) in columnList" :key="item.columnName">

          <div class="row" >
            <div class="col-lg-5">
              <label style="{text-align}">{{item.columnName}}</label>
            </div>
            <div class="col-lg-6">
              <input
                type="text"
                class="form-control place-holder-css"
                v-model="item.value"
                :placeholder="item.placeHolder"
              >
            </div>
          </div>
          <br>
            </span>
        </div>
      
  </div>
  <div class="actions">
    <button v-if="addFlag"  type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" @click="addData()">
                    Create
                </button>
    <button v-if="editFlag" type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" @click="editData()">
                    Update
                </button>
                <button
                type="button"
                class="btn btn-danger"
                @click="hideEntry()"
                v-tooltip.top.hover.focus="'Cancel the option'"
              >Cancel</button>
  </div>
</vudal> 
<div class="float-left" style="paddingBottom:1%">
</div>
<label>{{title}}</label>
    <div class="float-right" style="paddingBottom:1%">
      <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'">
        <download-excel :data="referenceFileData" type="csv" :name="title+'.csv'">
          <i class="fas fa-file-excel"></i>
          &nbsp;
          Export
        </download-excel>
      </button>
 
       &nbsp; &nbsp;
   
              
                <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Add'" @click="addEntry()">
                    
                    <i class="fas fa-plus-square"></i>  &nbsp;Add
                </button>
    </div>
   <br>
   <br>
   
        <div id="referenceBox">
    <ag-grid-vue
              style="width: 100%; height: 486px;"
              class="ag-theme-balham"
              :columnDefs="referenceColumnDefs"
              :rowData="referenceRowData"
              :gridOptions="referenceGridOptions"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              pagination="true"
              :paginationPageSize="15"
              :cellClicked="onCellClicked"
              :gridReady="OnRefReady"
              :gridSizeChanged="OnRefReady"
              

            ></ag-grid-vue> 
            </div>
            <br>
   <br>
    
            <div class="float-right" style="paddingBottom:1%">
              
                <!-- <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" @click="addEntry()">
                    Add
                </button> -->
             
                <button
                type="button"
                class="btn btn-danger"
                @click="cancel()"
                v-tooltip.top.hover.focus="'Move to Reference Page'"
              >Back</button>
            </div>
            <br>
            <br>
            
        </div>
    </div>
</div>

</template>

<script>
import router from "../../router/";
import headernav from "@/components/header/header";
import SideNav from "@/components/sidenav/sidenav";
import * as constant from "../constant/constant";
import { AgGridVue } from "ag-grid-vue";
import Vue from "vue";
import  Vudal from 'vudal';



export default {
 name: "ReferenceView",
  components: {
    SideNav,
    headernav,
    AgGridVue,
    Vudal
  },

  created()
  {
    
    this.fileType=this.$route.query.fileType;
    console.log("File Type ->",this.fileType);
    if(this.fileType === 'parts')
    {
      this.partsColumnDef();
      this.getParts();
    }
    else if(this.fileType === 'highspare')
    {
      this.highSpareColumnDef();
      this.getHighSpare();
    }
     else if(this.fileType === 'node')
    {
      this.nodeColumnDef();
      this.getNode();
    }
    else if(this.fileType === 'depot')
    {
      this.depotColumnDef();
      this.getDepot();
    }
    else if(this.fileType === 'misnomer')
    {
      this.misnomerColumnDef();
      this.getMisnomer();
    }
    else{
      this.ratioPONColumnDef();
      this.getRatioPON(this.fileType);
    }
  },

  data()
  {
      return{
          postMenu: "Reference >",
          current: "Reference View",
          fileType:"",
          referenceFileData:[],
          referenceColumnDefs:null,
          referenceRowData:[],
          referenceList: [],
          columnList:[],
          formDatas:[],
          editFlag:false,
          addFlag:true,
          gridApi: null,
          title:"",
          uniqueId:"",
          loaderFlag:false,
          referenceGridOptions: {
            rowStyle: {
              color: "#72879d",
              align: "center"
              // fontSize: "13.7px",
            }
      }
      };
  },
  methods:
  {
      addEntry()
      {
          this.$modals.myModal.$show();
      },
      hideEntry()
      {
        this.formDatas=[];
        this.$modals.myModal.$hide();
      },
      partsColumnDef()
      {
        this.title="Parts Details";
        this.columnList=[{columnName:"Part Name",formName:"part_name",value:"",placeHolder:"AAM-B2"},
                        {columnName:"Material Number",formName:"material_number",value:"",placeHolder:"1000009"},
                        {columnName:"Part Reliability Class",formName:"part_reliability_class",value:"",placeHolder:"AAM"},
                        {columnName:"Spared Attribute",formName:"spared_attribute",value:"",placeHolder:"1"},
                        {columnName:"Standard Cost",formName:"standard_cost",value:"",placeHolder:"2108.94"}];
         this.referenceColumnDefs = [
        {
          headerName: "Part Name",
          field: "part_name",
          width: 250
        },
        {
          headerName: "Material Number",
          field: "material_number",
          width: 150
        },
        {
          headerName: "Part Number",
          field: "part_number",
          width: 150
        },
        {
          headerName: "Part Reliability Class",
          field: "part_reliability_class",
          width: 150
        },
        {
          headerName: "Spared Attribute",
          field: "spared_attribute",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Standard Cost",
          field: "standard_cost",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
       highSpareColumnDef()
      {
        this.title="High Spare Details";
        this.columnList=[{columnName:"Substitution PON",formName:"SubstitutionPON",value:"",placeHolder:"AOFX-500-T4-1-C8"},
                        {columnName:"Classic PON",formName:"ClassicPON",value:"",placeHolder:"AOFX-500-T4-1-C8"}];
         this.referenceColumnDefs = [
        {
          headerName: "Classic PON",
          field: "ClassicPON",
          width: 250
        },
        {
          headerName: "Substitution PON",
          field: "SubstitutionPON",
          width: 150
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
       nodeColumnDef()
      {
        this.title="Node Details";
        this.columnList=[{columnName:"Node Name",formName:"node_name",value:"",placeHolder:"Adjuntas_Flex_1"},
                        {columnName:"Node Depot Belongs",formName:"node_depot_belongs",value:"",placeHolder:"MZTM"},
                        {columnName:"End Customer Node Belongs",formName:"end_customer_node_belongs",value:"",placeHolder:"Bestel"}];
         this.referenceColumnDefs = [
        {
          headerName: "Node Name",
          field: "node_name",
          width: 250
        },
        {
          headerName: "Node Depot Belongs",
          field: "node_depot_belongs",
          width: 150
        },
        {
          headerName: "End Customer Node Belongs",
          field: "end_customer_node_belongs",
          width: 150
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
      depotColumnDef()
      {
        this.title="Depot Details";
        this.columnList=[{columnName:"Depot Name",formName:"depot_name",value:"",placeHolder:"BOTA"},
                        {columnName:"Partner",formName:"partner",value:"",placeHolder:"Choice Logistics"},
                        {columnName:"City",formName:"city",value:"",placeHolder:"Silverwater"},
                        {columnName:"State",formName:"state",value:"",placeHolder:"NSW"},
                        {columnName:"Region",formName:"region",value:"",placeHolder:"APACq"},
                        {columnName:"Partner Warehouse Code",formName:"partner_warehouse_code",value:"",placeHolder:"Choice Logistics"},
                        {columnName:"Depot Address",formName:"depot_address",value:"",placeHolder:"129-137 Beaconsfield Street"},
                        {columnName:"Contact",formName:"contact",value:"",placeHolder:"Choice Logistics"},
                        {columnName:"Hub",formName:"hub",value:"",placeHolder:"1"},
                        {columnName:"Latitude",formName:"lat",value:"",placeHolder:"-33"},
                        {columnName:"Longitude",formName:"long",value:"",placeHolder:"151"}];
         this.referenceColumnDefs = [
        {
          headerName: "Depot Name",
          field: "depot_name",
          width: 250
        },
        {
          headerName: "Partner",
          field: "partner",
          width: 150
        },
        {
          headerName: "City",
          field: "city",
          width: 150
        },
        {
          headerName: "State",
          field: "state",
          width: 150
        },
        {
          headerName: "Region",
          field: "region",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Partner Warehouse Code",
          field: "partner_warehouse_code",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Depot Address",
          field: "depot_address",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Contact",
          field: "contact",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Hub",
          field: "hub",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Latitude",
          field: "lat",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Longitude",
          field: "long",
          width: 150,
          filter: "date"
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
       misnomerColumnDef()
      {
        this.title="Misnomer Details";
        this.columnList=[{columnName:"Correct PON",formName:"Correct_PON",value:"",placeHolder:"D-FANTRAY-B="},
                        {columnName:"Misnomer PON",formName:"Misnomer_PON",value:"",placeHolder:"D-FANTRAY"}];
         this.referenceColumnDefs = [
        {
          headerName: "Correct PON",
          field: "CorrectPON",
          width: 250
        },
        {
          headerName: "Misnomer PON",
          field: "MisnomerPON",
          width: 150
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
      ratioPONColumnDef()
      {
        this.title="Ratio PON Details";
        this.columnList=[{columnName:"Product Family",formName:"product_family",value:"",placeHolder:"BMM"},
                        {columnName:"Number of Spares 1",formName:"number_of_spares_1",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 2",formName:"number_of_spares_2",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 3",formName:"number_of_spares_3",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 4",formName:"number_of_spares_4",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 5",formName:"number_of_spares_5",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 6",formName:"number_of_spares_6",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 7",formName:"number_of_spares_7",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 8",formName:"number_of_spares_8",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 9",formName:"number_of_spares_9",value:"",placeHolder:"10"},
                        {columnName:"Number of Spares 10",formName:"number_of_spares_10",value:"",placeHolder:"10"}];
         this.referenceColumnDefs = [
        {
          headerName: "Product Family",
          field: "product_family",
          width: 250
        },
        {
          headerName: "Number of Spares 1",
          children:[{
            headerName: "1",
            field: "number_of_spares1",
            width: 250
          },
          {
            headerName: "2",
            field: "number_of_spares2",
            width: 250
          },
          {
            headerName: "3",
            field: "number_of_spares3",
            width: 250
          },
          {
            headerName: "4",
            field: "number_of_spares4",
            width: 250
          },
          {
            headerName: "5",
            field: "number_of_spares5",
            width: 250
          },
          {
            headerName: "6",
            field: "number_of_spares6",
            width: 250
          },
          {
            headerName: "7",
            field: "number_of_spares7",
            width: 250
          },
          {
            headerName: "8",
            field: "number_of_spares8",
            width: 250
          },
          {
            headerName: "9",
            field: "number_of_spares9",
            width: 250
          },
          {
            headerName: "10",
            field: "number_of_spares10",
            width: 250
          }
          ]
        },
        {
          headerName: "Edit",
          field: "editFlag",
          width: 250,
          cellRenderer: actionEditRenderer
        },
        {
          headerName: "Delete",
          field: "deleteFlag",
          width: 250,
          cellRenderer: actionDeleteRenderer
        }
      ];
      },
      editData()
      {
        let url; 
        let formData = new FormData();
        if(this.fileType === 'parts')
          {
           // formData.append("parts_id",this.uniqueId);
             url="api/v1/get_all_parts?parts_id="+this.uniqueId;
          }
          else if(this.fileType === 'highspare')
          {
            //formData.append("high_spare_id",this.uniqueId);
           url="api/v1/get_all_high_spare?high_spare_id="+this.uniqueId;
          }
          else if(this.fileType === 'node')
          {
            //formData.append("node_id",this.uniqueId);
           url="api/v1/get_all_node?node_id="+this.uniqueId;
          }
          else if(this.fileType === 'depot')
          {
            //formData.append("depot_id",this.uniqueId);
           url="api/v1/get_all_depot?depot_id="+this.uniqueId;
          }
          else if(this.fileType === 'misnomer')
          {
            //formData.append("reference_table_id",this.uniqueId);
           url="api/v1/get_all_misnomer?reference_table_id="+this.uniqueId;
          }
          else{
            formData.append("reliability_id",this.uniqueId);
           url="api/v1/get_all_ratio?pon_type="+this.fileType+"&reliability_id="+this.uniqueId;
          }
        for(let i = 0;i<this.columnList.length;i++)
        {
          formData.append(this.columnList[i].formName, this.columnList[i].value);
        }
      console.dir("formdata ----->", formData);
      fetch(constant.APIURL + url, {
        method: "PATCH",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("Response from backend data ---->", data);
            if (data.http_status_code === 200) {
               swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              });
            } else {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
              
            }
            this.$modals.myModal.$hide();
            if(this.fileType === 'parts')
              {
                this.getParts();
              }
              else if(this.fileType === 'highspare')
              {
                this.getHighSpare();
              }
              else if(this.fileType === 'node')
              {
                this.getNode();
              }
              else if(this.fileType === 'depot')
              {
                this.getDepot();
              }
              else if(this.fileType === 'misnomer')
              {
                this.getMisnomer();
              }
              else{
                this.getRatioPON(this.fileType);
              }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      addData()
      {
        this.$modals.myModal.$hide();
        this.loaderFlag=true;
       let url; 
        if(this.fileType === 'parts')
          {
             url="api/v1/get_all_parts";
          }
          else if(this.fileType === 'highspare')
          {
           url="api/v1/get_all_high_spare";
          }
          else if(this.fileType === 'node')
          {
           url="api/v1/get_all_node";
          }
          else if(this.fileType === 'depot')
          {
           url="api/v1/get_all_depot";
          }
          else if(this.fileType === 'misnomer')
          {
           url="api/v1/get_all_misnomer";
          }
          else{
           url="api/v1/get_all_ratio?pon_type="+this.fileType;
          }
        let formData = new FormData();
        for(let i = 0;i<this.columnList.length;i++)
        {
          formData.append(this.columnList[i].formName, this.columnList[i].value);
        }
      console.dir("formdata ----->", formData);
      fetch(constant.APIURL + url, {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("Response from backend data ---->", data);
            if (data.http_status_code === 200) {
               swal({
                title: "SUCCESS",
                text: data.msg,
                icon: "success"
              });
            } else {
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
              
            }
            
            if(this.fileType === 'parts')
              {
                this.getParts();
              }
              else if(this.fileType === 'highspare')
              {
                this.getHighSpare();
              }
              else if(this.fileType === 'node')
              {
                this.getNode();
              }
              else if(this.fileType === 'depot')
              {
                this.getDepot();
              }
              else if(this.fileType === 'misnomer')
              {
                this.getMisnomer();
              }
              else{
                this.getRatioPON(this.fileType);
              }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getParts()
      {
        this.loaderFlag=true;
         console.log("loader show");
        this.referenceRowData=[];
        fetch(constant.APIURL + "api/v1/get_all_parts", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                material_number: this.referenceList[i].material_number,
                part_name: this.referenceList[i].part_name,
                part_number: this.referenceList[i].part_number,
                part_reliability_class: this.referenceList[i].part_reliability_class,
                spared_attribute: this.referenceList[i].spared_attribute,
                standard_cost: this.referenceList[i].standard_cost,
                editFlag:this.referenceList[i].part_id,
                deleteFlag:this.referenceList[i].part_id
              });
              this.referenceFileData.push({
                material_number: this.referenceList[i].material_number,
                part_name: this.referenceList[i].part_name,
                part_number: this.referenceList[i].part_number,
                part_reliability_class: this.referenceList[i].part_reliability_class,
                spared_attribute: this.referenceList[i].spared_attribute,
                standard_cost: this.referenceList[i].standard_cost
              });
            }
            this.loaderFlag=false;
          
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getHighSpare()
      {
        this.loaderFlag=true;
        this.referenceRowData=[];
        fetch(constant.APIURL + "api/v1/get_all_high_spare", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                ClassicPON: this.referenceList[i].ClassicPON,
                SubstitutionPON: this.referenceList[i].SubstitutionPON,
                editFlag:this.referenceList[i].high_spare_id,
                deleteFlag:this.referenceList[i].high_spare_id
              });
              this.referenceFileData.push({
                ClassicPON: this.referenceList[i].ClassicPON,
                SubstitutionPON: this.referenceList[i].SubstitutionPON
                
              });
            }
          this.loaderFlag=false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      cancel() {
      router.push("/reference");
      },
      getNode()
      {
        this.loaderFlag=true;
        this.referenceRowData=[];
        fetch(constant.APIURL + "api/v1/get_all_node", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                end_customer_node_belongs: this.referenceList[i].end_customer_node_belongs,
                node_depot_belongs: this.referenceList[i].node_depot_belongs,
                node_name: this.referenceList[i].node_name,
                editFlag:this.referenceList[i].node_id,
                deleteFlag:this.referenceList[i].node_id
              });
              this.referenceFileData.push({
                end_customer_node_belongs: this.referenceList[i].end_customer_node_belongs,
                node_depot_belongs: this.referenceList[i].node_depot_belongs,
                node_name: this.referenceList[i].node_name
              });
            }
            this.loaderFlag=false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getDepot()
      {
        this.referenceRowData=[];
        this.loaderFlag=true;
        fetch(constant.APIURL + "api/v1/get_all_depot", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                city: this.referenceList[i].city,
                contact: this.referenceList[i].contact,
                country: this.referenceList[i].country,
                depot_address: this.referenceList[i].depot_address,
                depot_name: this.referenceList[i].depot_name,
                hub: this.referenceList[i].hub,
                lat: this.referenceList[i].lat,
                long: this.referenceList[i].long,
                partner: this.referenceList[i].partner,
                partner_warehouse_code: this.referenceList[i].partner_warehouse_code,
                region: this.referenceList[i].region,
                state: this.referenceList[i].state,
                editFlag:this.referenceList[i].depot_id,
                deleteFlag:this.referenceList[i].depot_id
              });
              this.referenceFileData.push({
                city: this.referenceList[i].city,
                contact: this.referenceList[i].contact,
                country: this.referenceList[i].country,
                depot_address: this.referenceList[i].depot_address,
                depot_name: this.referenceList[i].depot_name,
                hub: this.referenceList[i].hub,
                lat: this.referenceList[i].lat,
                long: this.referenceList[i].long,
                partner: this.referenceList[i].partner,
                partner_warehouse_code: this.referenceList[i].partner_warehouse_code,
                region: this.referenceList[i].region,
                state: this.referenceList[i].state
                
              });
            }
           this.loaderFlag=false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getMisnomer()
      {
        this.loaderFlag=true;
        fetch(constant.APIURL + "api/v1/get_all_misnomer", {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                CorrectPON: this.referenceList[i].Correct_PON,
                MisnomerPON: this.referenceList[i].Misnomer_PON,
                editFlag:this.referenceList[i].reference_table_id,
                deleteFlag:this.referenceList[i].reference_table_id
              });
              this.referenceFileData.push({
                CorrectPON: this.referenceList[i].Correct_PON,
                MisnomerPON: this.referenceList[i].Misnomer_PON
              });
            }
            this.loaderFlag=false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getRatioPON(fileType)
      {
        this.loaderFlag=true;
        this.referenceRowData=[];
        console.log('file type asd',fileType);
         fetch(constant.APIURL + "api/v1/get_all_ratio?pon_type="+fileType, {
        method: "GET"
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -getallrequest--->", data);
            this.referenceList=data;
            for (let i = 0; i < this.referenceList.length; i++) {
              //console.log(this.partsAnalysisRequestList[i].analysis_name);
              this.referenceRowData.push({
                product_family: this.referenceList[i].product_family,
                number_of_spares1: this.referenceList[i].number_of_spares1,
                number_of_spares2: this.referenceList[i].number_of_spares2,
                number_of_spares3: this.referenceList[i].number_of_spares2,
                number_of_spares4: this.referenceList[i].number_of_spares4,
                number_of_spares5: this.referenceList[i].number_of_spares5,
                number_of_spares6: this.referenceList[i].number_of_spares6,
                number_of_spares7: this.referenceList[i].number_of_spares7,
                number_of_spares8: this.referenceList[i].number_of_spares8,
                number_of_spares9: this.referenceList[i].number_of_spares9,
                number_of_spares10: this.referenceList[i].number_of_spares10,
                editFlag:this.referenceList[i].reliability_id,
                deleteFlag:this.referenceList[i].reliability_id
              });
              this.referenceFileData.push({
                product_family: this.referenceList[i].product_family,
                number_of_spares1: this.referenceList[i].number_of_spares1,
                number_of_spares2: this.referenceList[i].number_of_spares2,
                number_of_spares3: this.referenceList[i].number_of_spares2,
                number_of_spares4: this.referenceList[i].number_of_spares4,
                number_of_spares5: this.referenceList[i].number_of_spares5,
                number_of_spares6: this.referenceList[i].number_of_spares6,
                number_of_spares7: this.referenceList[i].number_of_spares7,
                number_of_spares8: this.referenceList[i].number_of_spares8,
                number_of_spares9: this.referenceList[i].number_of_spares9,
                number_of_spares10: this.referenceList[i].number_of_spares10
              });
            }
            this.loaderFlag=false;
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      
      OnRefReady(event) {
        console.log(event)
        this.gridApi=event.api;
          var gridWidth = document.getElementById('referenceBox').offsetWidth;

            // keep track of which columns to hide/show
            var columnsToShow = [];
            var columnsToHide = [];

            // iterate over all columns (visible or not) and work out
            // now many columns can fit (based on their minWidth)
            var totalColsWidth = 0;
            var allColumns = event.columnApi.getAllColumns();
            for (var i = 0; i < allColumns.length; i++) {
                let column = allColumns[i];
                totalColsWidth += column.getMinWidth();
                if (totalColsWidth > gridWidth) {
                    columnsToHide.push(column.colId);
                } else {
                    columnsToShow.push(column.colId);
                }
            }

            // show/hide columns based on current grid width
            event.columnApi.setColumnsVisible(columnsToShow, true);
            event.columnApi.setColumnsVisible(columnsToHide, false);

            // fill out any available space to ensure there are no gaps
            event.api.sizeColumnsToFit();
          },
          onCellClicked(event) {
            console.dir(event);
            
            if(event.colDef.field === 'deleteFlag')
            {
              console.log(event.value);
              if(this.fileType === 'parts')
              {
              let part_id=event.value;

               swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                      fetch(constant.APIURL + "api/v1/get_all_parts?parts_id="+part_id, {
                        method: "DELETE"
                        })
                        .then(response => {
                          response.text().then(text => {
                            const data = text && JSON.parse(text);
                            console.log("data -getallrequest--->", data);
                            
                            if (data.http_status_code === 200) {
                              swal({
                                title: "Success",
                                text: data.msg,
                                icon: "success"
                              }).then(ok => {
                                if (ok) {
                                  
                                  this.getParts();
                                }
                            });
                            } else {
                              swal({
                                title: "Error",
                                text: data.msg,
                                icon: "error"
                              });
                              
                            }
                          });
                        })
                        .catch(handleError => {
                          console.log(" Error Response ------->", handleError);
                        });
                        }
                      });
              }
              else if(this.fileType === 'highspare')
              {
                 swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                let high_spare_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_high_spare?high_spare_id="+high_spare_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      
                     
                      const data = text && JSON.parse(text);
                    console.log("data -getallrequest--->", data);
                    
                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                          this.getHighSpare();
                        }
                    });
                    } else {
                      swal({
                        title: "Error",
                        text: data.msg,
                        icon: "error"
                      });
                    }
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                        }
                      });
                
              }
              else if(this.fileType === 'node')
              {
               let node_id=event.value;

                swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                fetch(constant.APIURL + "api/v1/get_all_node?node_id="+node_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    
                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                          this.getNode();
                        }
                    });
                    } else {
                      swal({
                        title: "Error",
                        text: data.msg,
                        icon: "error"
                      });
                      
                    }
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                        }
                      });
              }
              else if(this.fileType === 'depot')
              {
                let depot_id=event.value;
                 swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                fetch(constant.APIURL + "api/v1/get_all_depot?depot_id="+depot_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                          const data = text && JSON.parse(text);
                    console.log("data -getallrequest--->", data);
                    
                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                          this.getDepot();
                        }
                    });
                    } else {
                      swal({
                        title: "Error",
                        text: data.msg,
                        icon: "error"
                      });
                      
                    }
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                        }
                      });
              }
              else if(this.fileType === 'minsomer')
              {
                let reference_tabel_id=event.value;
                 swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                fetch(constant.APIURL + "api/v1/get_all_misnomer?reference_tabel_id="+reference_tabel_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                        
                    console.log("data -getallrequest--->", data);
                    
                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                          this.getMisnomer();
                        }
                    });
                    } else {
                      swal({
                        title: "Error",
                        text: data.msg,
                        icon: "error"
                      });
                      
                    }
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                        }
                      });
              }
              else{
                let reliability_id=event.value;
                 swal({
                        title: "Info",
                        text: "Do You Want to Delete the Data ?",
                        icon: "info"
                      }).then(ok => {
                        if (ok) {
                fetch(constant.APIURL + "api/v1/get_all_ratio?pon_type="+this.fileType+"&reliability_id="+reliability_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                       console.log("data -getallrequest--->", data);
                    
                    if (data.http_status_code === 200) {
                      swal({
                        title: "Success",
                        text: data.msg,
                        icon: "success"
                      }).then(ok => {
                        if (ok) {
                           this.getRatioPON(this.fileType);
                        }
                    });
                    } else {
                      swal({
                        title: "Error",
                        text: data.msg,
                        icon: "error"
                      });
                      
                    }
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                        }
                      });
              }
            }else if(event.colDef.field === 'editFlag'){
              this.editFlag=true;
              this.addFlag=false;
              if(this.fileType === 'parts')
              {
                this.uniqueId=event.value;
                this.columnList[0].value=event.data.part_name;
                      this.columnList[1].value=event.data.material_number;
                      this.columnList[2].value=event.data.part_reliability_class;
                      this.columnList[3].value=event.data.spared_attribute;
                      this.columnList[4].value=event.data.standard_cost;
                
                   this.$modals.myModal.$show();
              }
              else if(this.fileType === 'highspare')
              {
                this.uniqueId=event.value;
                this.columnList[0].value=event.data.SubstitutionPON;
                this.columnList[1].value=event.data.ClassicPON;
                
                  this.$modals.myModal.$show();
              }
              else if(this.fileType === 'node')
              {
                this.uniqueId=event.value;
                this.columnList[0].value=event.data.node_name;
                this.columnList[1].value=event.data.node_depot_belongs;
                this.columnList[2].value=event.data.end_customer_node_belongs;
                  this.$modals.myModal.$show();
              }
              else if(this.fileType === 'depot')
              {

                this.columnList[0].value=event.data.depot_name;
                      this.columnList[1].value=event.data.partner;
                      this.columnList[2].value=event.data.city;
                      this.columnList[3].value=event.data.state;
                      this.columnList[4].value=event.data.region;
                      this.columnList[5].value=event.data.partner;
                      this.columnList[6].value=event.data.depot_address;
                      this.columnList[7].value=event.data.contact;
                      this.columnList[8].value=event.data.hub;
                      this.columnList[9].value=event.data.lat;
                      this.columnList[10].value=event.data.long;
                      this.uniqueId=event.value;
                      
                  this.$modals.myModal.$show();
              }
              else if(this.fileType === 'node')
              {
                this.uniqueId=event.value;
                 this.columnList[0].value=event.data.node_name;
                      this.columnList[1].value=event.data.node_depot_belongs;
                      this.columnList[2].value=event.data.end_customer_node_belongs;
                     
                
                  this.$modals.myModal.$show();
              }
              else if(this.fileType === 'misnomer')
              {
                this.uniqueId=event.value;
                      this.columnList[0].value=event.data.CorrectPON;
                      this.columnList[1].value=event.data.MisnomerPON;
                
                  this.$modals.myModal.$show();
              }
              else{
                this.uniqueId=event.value;
                this.columnList[0].value=event.data.product_family;
                      this.columnList[1].value=event.data.number_of_spares1;
                      this.columnList[2].value=event.data.number_of_spares2;
                      this.columnList[3].value=event.data.number_of_spares3;
                      this.columnList[4].value=event.data.number_of_spares4;
                      this.columnList[5].value=event.data.number_of_spares5;
                      this.columnList[6].value=event.data.number_of_spares6;
                      this.columnList[7].value=event.data.number_of_spares7;
                      this.columnList[8].value=event.data.number_of_spares8;
                      this.columnList[9].value=event.data.number_of_spares9;
                      this.columnList[10].value=event.data.number_of_spares10;
                      
                this.$modals.myModal.$show();
                
              }
            }
          
            }
  }
};
function actionEditRenderer(params) {
  
  let skills = [];
  
  skills.push(
    '<i style="cursor:pointer" class="fas fa-edit"></i>'
  );
  
  return skills.join(" ");
}
function actionDeleteRenderer(params) {
  
  let skills = [];
  
  skills.push(
    '<i style="cursor:pointer" class="fas fa-trash-alt"></i>'
  );
  
  return skills.join(" ");
}
</script>

<style>
.myBreadCrumb {
  margin-top: -2%;
  margin-bottom: 2%;
}

::placeholder {
    opacity:10;
    font-weight: lighter;
}

.labelStyle {
 text-align: left;
}
</style>
