<template>
    <div>
        <headernav/>
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
      
        <div class="shadow p-3 mb-5 bg-white rounded" >
    
    <vudal name="myModal">
  <div class="header">
    <i class="close icon"></i>
    Title
  </div>
  <div class="content">
    <div class="form-group">
      <span v-for="(item,index) in columnList" :key="item.columnName">

          <div class="row" >
            <div class="col-lg-5">
              <label>{{item.columnName}}</label>
            </div>
            <div class="col-lg-6">
              <input
                type="text"
                class="form-control"
                v-model="formDatas[index]"
              >
            </div>
          </div>
          <br>
            </span>
        </div>
      
  </div>
  <div class="actions">
    <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" @click="addData()">
                    ADD
                </button>
                <button
                type="button"
                class="btn btn-danger"
                @click="hideEntry()"
                v-tooltip.top.hover.focus="'Move to Analysis Dashboard'"
              >Back</button>
  </div>
</vudal> 


    <div class="float-right" style="paddingBottom:1%">
      <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'">
        <download-excel :data="referenceFileData" type="csv">
          <i class="fas fa-file-excel"></i>
          &nbsp;
          Export
        </download-excel>
      </button>
    </div>
   <br>
   <br>
    <br>
        <div id="referenceBox">
    <ag-grid-vue
              style="width: 100%; height: 345px;"
              class="ag-theme-balham"
              :columnDefs="referenceColumnDefs"
              :rowData="referenceRowData"
              :gridOptions="referenceGridOptions"
              :enableColResize="true"
              :enableSorting="true"
              :enableFilter="true"
              :groupHeaders="true"
              rowSelection="multiple"
              pagination="true"
              :paginationPageSize="10"
              :cellClicked="onCellClicked"
              :gridReady="OnRefReady"
              :gridSizeChanged="OnRefReady"

            ></ag-grid-vue> 
            </div>
            <div class="float-right" style="paddingBottom:1%">
              
                <button type="button" class="btn btn-success" v-tooltip.top.hover.focus="'Click to Download'" @click="addEntry()">
                    Add
                </button>
                &nbsp; &nbsp;
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
    else if(this.fileType === 'minsomer')
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
          referenceGridOptions: {
            rowStyle: {
              color: "#72879d",
              align: "center"
              // fontSize: "13.7px",
            },
            columnStyle: {
              color: "#72879d"
              // fontSize: "11.05px"
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
        this.columnList=[{columnName:"Part Name",formName:"part_name"},{columnName:"Material Number",formName:"material_number"},{columnName:"Part Reliability Class",formName:"part_reliability_class"},{columnName:"Spared Attribute",formName:"spared_attribute"},{columnName:"Standard Cost",formName:"standard_cost"}];
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
          field: "hub",
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
         this.referenceColumnDefs = [
        {
          headerName: "Product Family",
          field: "product_family",
          width: 250
        },
        {
          headerName: "Number of Spares",
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
      addData()
      {
          if(this.fileType === 'parts')
          {
            
            this.addParts();
          }
          else if(this.fileType === 'highspare')
          {
            
            this.addHighSpare();
          }
          else if(this.fileType === 'node')
          {
           
            this.addNode();
          }
          else if(this.fileType === 'depot')
          {
            
            this.addDepot();
          }
          else if(this.fileType === 'minsomer')
          {
            
            this.addMisnomer();
          }
          else{
            
            this.addRatioPON(this.fileType);
          }

      },
      addParts()
      {
        let formData = new FormData();
        for(let i = 0;i<this.columnList.length;i++)
        {
          formData.append(this.columnList[i].formName, this.formDatas[i]);
        }
      console.log("formdata ----->", formData.get("part_reliability_class"));
      fetch(constant.APIURL + "api/v1/get_all_parts", {
        method: "PUT",
        body: formData
      })
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("Response from backend data ---->", data);
            if (data.http_status_code === 200) {
              this.routeToView(data);
            } else {
              swal("Hello world!");
              
              swal({
                title: "Error",
                text: data.msg,
                icon: "error"
              });
              $(document).ready(function() {
                $("#loader-2").hide();
              });
            }
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getParts()
      {
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
            }
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getHighSpare()
      {
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
                editFlag:this.referenceList[i].high_spare_part_id,
                deleteFlag:this.referenceList[i].high_spare_part_id
              });
            }
            
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
            }
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getDepot()
      {
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
            }
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getMisnomer()
      {
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
                CorrectPON: this.referenceList[i].CorrectPON,
                MisnomerPON: this.referenceList[i].MisnomerPON,
                editFlag:this.referenceList[i].reference_tabel_id,
                deleteFlag:this.referenceList[i].reference_tabel_id
              });
            }
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      getRatioPON(fileType)
      {
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
            }
            
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });
      },
      
      OnRefReady(event) {
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
            console.dir(event.colDef.field);
            let requestId = event.value;
            if(event.colDef.field === 'deleteFlag')
            {
              console.log(event.value);
              if(this.fileType === 'parts')
              {
                let part_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_parts?parts_id="+part_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getParts();
              }
              else if(this.fileType === 'highspare')
              {
                let high_spare_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_high_spare?high_spare_id="+high_spare_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      
                      console.log("data -getallrequest--->", text);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getHighSpare();
              }
              else if(this.fileType === 'node')
              {
               let node_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_node?node_id="+node_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getNode();
              }
              else if(this.fileType === 'depot')
              {
                let depot_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_depot?depot_id="+depot_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getDepot();
              }
              else if(this.fileType === 'minsomer')
              {
                let reference_tabel_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_misnomer?reference_tabel_id="+reference_tabel_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getMisnomer();
              }
              else{
                let reliability_id=event.value;
                fetch(constant.APIURL + "api/v1/get_all_ratio?pon_type="+this.fileType+"&reliability_id="+reliability_id, {
                  method: "DELETE"
                  })
                  .then(response => {
                    response.text().then(text => {
                      const data = text && JSON.parse(text);
                      console.log("data -getallrequest--->", data);
                    });
                  })
                  .catch(handleError => {
                    console.log(" Error Response ------->", handleError);
                  });
                this.getRatioPON(this.fileType);
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
</style>
