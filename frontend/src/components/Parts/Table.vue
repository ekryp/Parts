<template>
    <div>
    <headernav msg="Dashboard"/>
    <side-nav/>
    <div class="custom-container" style="paddingTop: 5%">
     
      <div class="row">
          <div class="col-lg-12">
            <div class="card">
              <!-- This for the rendering of customer Table -->
              <div v-if="topTable==='true'">
              <div class="card-header">
                <div class="row" >
                  <div class="col-lg-12" >
                    <h6>Customer Table</h6>
                  </div>
                  <!-- <i class="fas fa-share-square" style="cursor:pointer"></i> -->
                </div> 
              </div>
              <div class="card-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Customer</th>
                        <th scope="col">Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in data.customer" :key="item.id">
                        <td @click="renderMidTable(item.customer_name)" class="in-progress">{{item.customer_name}}</td>
                        <td>{{item.count}}</td>
                    </tr>
                </tbody>
                </table>
                </div>
              </div>

            <!-- This for the rendering of Parts Table -->
           <div v-if="midTable==='true'">
              <div class="card-header">
                <div class="row" >
                  <div class="col-lg-11" >
                    <h6>{{customerName}}</h6>
                  </div>
                  <i @click="renderCustomerTable()" class="fas fa-share-square" style="cursor:pointer"></i>
                </div> 
              </div>
              <div class="card-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Part Name</th>
                        <th scope="col">Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in parts" :key="item.id">
                        <td @click="renderLastTable(item.part_name)" class="in-progress">{{item.part_name}}</td>
                        <td>{{item.count}}</td>
                    </tr>
                </tbody>
                </table>
              </div>
            </div> 
            <!-- This for the rendering of Depots Table -->
           <div v-if="lastTable==='true'">
              <div class="card-header">
                <div class="row" >
                  <div class="col-lg-11" >
                    <h6>{{partName}}</h6>
                  </div>
                  <i  @click="renderMidTable(null)" class="fas fa-share-square" style="cursor:pointer"></i>
                </div> 
              </div>
              <div class="card-body">
                <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Depots Name</th>
                        <th scope="col">Count</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in depots" :key="item.id">
                        <td>{{item.depot_name}}</td>
                        <td>{{item.count}}</td>
                    </tr>
                </tbody>
                </table>
              </div>
            </div> 
            </div>
          </div>
          
      </div>
      
    </div>
  </div>
</template>

<script>
import router from "../../router/";
import SideNav from "@/components/sidenav/sidenav";
import headernav from "@/components/header/header";
import Multiselect from "vue-multiselect";
import * as constant from "../constant/constant";
//import * as data from "../../utilies/tabledata.json";

export default {
    name:'DynamicTable',
    components: {
    SideNav,
    headernav
  },
    created()
    {
        this.getTopExtenededData();
        

    },
    data() {
    console.log("dashboard", this.data);
    return {
      data: [],
      topTable:'true',
      midTable:'false',
      lastTable:'false',
      customer:null,
      parts:null,
      depots:null,
      partName:'',
      customerName:''

    };
  },
  methods : {
    renderMidTable(data)
    {
        console.log('data'+data)
        console.log('custnamae'+this.customerName)
        if(data===null)
        {
            data=this.customerName;
            this.midTable='true';
            this.lastTable='false';
        }else{
            this.customerName=data;
            this.midTable='true';
            this.topTable='false';
            this.lastTable='false';
        }
        console.log('data'+data)
        
        var i;
        let x=this.data.parts;
        let tmp=[];
        
        for(i=0;i<x.length;i++)
        {
            //console.log(x[i].part_name)
            if(x[i].customer_name===data)
            {
                var parttmpobj = {
                    part_name : x[i].part_name,
                    count : x[i].count
                };
                tmp.push(parttmpobj);
               // console.log(tmp)
            }

        }
        console.dir(tmp);
        this.parts=tmp;
    },
    renderLastTable(data)
    {
        //console.log(data)
        this.partName=data;
        this.topTable='false';
        this.midTable='false';
        this.lastTable='true';
        var i;
        let x=this.data.depots;
        let tmp=[];
        for(i=0;i<x.length;i++)
        {
            if(x[i].part_name===data)
            {
                var depottmpobj = {
                    depot_name : x[i].depot_name,
                    count : x[i].count
                };
                tmp.push(depottmpobj);
            }

        }
        //console.dir(tmp);
        this.depots=tmp;
        
    },
    renderCustomerTable()
    {
        this.topTable='true';
        this.midTable='false';
        this.lastTable='false';
    },
    getTopExtenededData()
    {
        fetch(
        constant.APIURL +
          "api/v1/get_top_extended",
        {
          method: "GET"
        }
      )
        .then(response => {
          response.text().then(text => {
            const data = text && JSON.parse(text);
            console.log("data -- get_dashboard_request_count-->", data);
            this.data = data;
            var lookup = {};
            var items = this.data;
            var result = [];

            for (var item, i = 0; item = items[i++];) {
            var name = item.customer_name;

            if (!(name in lookup)) {
                lookup[name] = 1;
                result.push(name);
            }
            }
            for(var item, i = 0; item = items[i++];)
            {
                
            }
            console.log(result);
          });
        })
        .catch(handleError => {
          console.log(" Error Response ------->", handleError);
        });


    },
    createCustomerData()
    {
        var i;
        let x=this.data;
        console.log('hi');
        let tmp=[];
        for(i=0;i<x.length;i++)
        {
            if(x[i].part_name===data)
            {
                var depottmpobj = {
                    depot_name : x[i].depot_name,
                    count : x[i].count
                };
                tmp.push(depottmpobj);
            }

        }
        //console.dir(tmp);
        this.depots=tmp;
    }


  }
}
</script>

<style>

.text-top {
  font-size: 1.15vw;
  font-weight: 500;
}
.text-middle {
  font-size: 40px;
  font-weight: 600;
}
.text-bottom {
  font-size: 1vw;
}
.row-one {
  padding-top: 5%;
}
.row-two {
  margin-top: 2%;
}
.vertical {
  width: 1%;
  height: 60px;
  background-color: #adb2b5;
}
.container {
  width: 100% !important;
  height: 100%;
}
.card {
  position: relative;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
  max-height: 42vh;
  min-height: 42vh;
}
.card-body {
  -ms-flex: 1 1 auto;
  flex: 1 1 auto;
  padding: 1.25rem;
  overflow: auto;
}
.card-header {
  padding: 0.75rem 1.25rem;
  margin-bottom: 0;
  background-color: rgb(237, 237, 237);
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

/* For cursor Pointer Change to Hand Icon */

.in-progress {
  cursor: pointer;
}
</style>

