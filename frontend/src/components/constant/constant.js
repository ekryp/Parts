export let APIURL = "";
export let APPURL = "";
export let ELKURL = "";
if (process.env.NODE_ENV === 'local') {
  APIURL = "https://staging-ib-services.ekryp.com/";
  ELKURL = "http://localhost:5002/";
  APPURL = "http://localhost:2323/";
  //ELKURL = "https://staging-elk.ekryp.com/"
} else if (process.env.NODE_ENV === 'uat') {
  APIURL = "https://staging-ib-services.ekryp.com/";
  APPURL = "https://staging-ib.ekryp.com/";
  ELKURL = "https://staging-elk.ekryp.com/"
} else if (process.env.NODE_ENV === 'prod') {
  APIURL = "https://infinera-services.ekryp.com/";
  APPURL = "https://infinera.ekryp.com/";
  ELKURL = "https://infinera-elk.ekryp.com/"
}

export const PERMISSIONS = ['Dashboard', 'CreateAnalysis', 'ViewAnalysis', 'ViewReference', 'EditReference', 'ViewAnalysisDetails', 'ManageRole', 'ManageUser', 'SolutionPrediction', 'knowledgeMap', 'internal']


export const Dashboard = {
  breadcrumb: "Dashboard",
  filterButtons: ["All", "Clear"],
  filterNames: ["Customer", "Depot"],
  dashboardDetails: ["Total Customer", "Critical PONs", "Critical Customers", "Critical Depots", "Total PON types", "Total Depots"],
  table1: {
    tableName: "Top PONs",
    tableHeaders: ["PONs", "Count"]
  },
  table2: {
    tableName: "Top Depots",
    tableHeaders: ["Depot", "PONs  Count"]
  },
  table3: {
    tableName: "Top Customers",
    tableHeaders: ["Customer", "PONs Count"]
  }
}

export const RoleManagementScreen = {
  pageHeader: "Role Management",
  PopUpHeaders: ["Create Role", "Edit Role"],
  popUpFields: ["Name", "Description", "Permissions"],
  popUpButtons: ["Create", "Update", "Cancel"],
  table: {
    tableName: "Role",
    tableHeaders: ["Name", "Description", "Action"]
  },
  addButton: "Add Role"

}

export const UserManagementScreen = {
  pageHeader: "User Management",
  PopUpHeaders: ["Create Role", "Edit Role"],
  popUpFields: ["Name", "Description", "Permissions"],
  popUpButtons: ["Create", "Update", "Cancel"],
  table: {
    tableName: "Users",
    tableHeaders: ["User Mail Id", "Username", "Roles", "Manage Roles"]
  },
  addButton: "Add User"

}

export const ChangePasswordScreen = {
  table: {
    tableName: "Change Password",
    tableHeaders: ["New Password :", "Confirm Password :"]
  },
}

export const AnalysisDashboardScreen = {
  breadcrumb: "Analysis",

  analysisDetails: ["Total Analysis Request", "Completed Request", "Completed Request with Error", "Completed Request Successfully", "Request In Progress", "Requests To Be Submitted "],
  exportButton: "Export",
  createAnalysisButton: "Create Analysis"
}

export const CreateAnalysisScreen = {
  breadcrumbs: ["Analysis", "Analysis Create"],
  createAnalysisLabels: ["Analysis Name :", "Customer Name :", "Date :", "Analysis Type :", "Replenish Time :", "File Type:", "SAP Current Inventory File :", "BOM File :", "Is MTBF?", "DNA File :"],
  createAnalysisPlaceHolders: ["Enter Analysis Name ", "Select Customer ", " Select Analysis Type", "Select Replenish Time ", "no file selected"],
  buttons: ["Back", "Submit For Analysis", "ReSubmit For Analysis", "Uploading"]
}


export const ViewAnalysisScreen = {
  breadcrumbs: ["Analysis >", "Analysis Update"],
  createAnalysisLabels: ["Analysis Name :", "Customer Name :", "Date :", "Analysis Type :", "Replenish Time :", "Input File :", "SAP Current Inventory File :", "BOM File :"],
  createAnalysisPlaceHolders: ["Enter Analysis Name ", "Select Customer ", " Select Analysis Type", "Select Replenish Time ", "no file selected"],
  buttons: ["Back", "View Details", "Error Details"]
}

export const SpareSummaryScreen = {
  breadcrumbs: ["Analysis >", "Analysis Summary"],
  analysisDetails: ["Total Depot", "Critical Depot", "Total PON Type", "Critical PON"],
  navHeader: ["Summary", "Summary-PON/Depot", "Current Inventory", "Install Base Quantity", "Gross", "Net", "Error"],
  exportButton: "Export",
}

export const ReferenceViewScreen = {
  breadcrumb: "Reference",
  tableHeader: "Reference File Information :",
  fileNames: ["Part File", "High Spare File", "Node File", "Depot File", "Misnomer File", "Ratio of PON - 2Day File", "Ratio of PON - 7Day File", "Ratio of PON - 30Day File", "Ratio of PON - 60Day File", "Customer File"],
  filesDownloadText: ["Download Sample_Parts.csv",
    "Download Sample_High_Spare.csv",
    "Download Sample_Node.csv",
    "Download Sample_Depot.csv",
    "Download Sample_Minsomer.csv",
    "Download Sample_Ratio_2Day.csv",
    "Download Sample_Ratio_7Day.csv",
    "Download Sample_Ratio_30Day.csv",
    "Download Sample_Ratio_60Day.csv",
    "Download Sample_Customer.csv"
  ]
}
export const SolutionScreen = {
  breadcrumb: "Solution",
  modalHeader: "Patches",
  modalTabHeaders: ["Details", "Description"],
  modalContentsLabels: ["Title:", "Description:", "Progress Status:", "Group:", "Severity:", "Found In Build:", "Traget Release:", "Date Closed:", "Product:", "Service Account:", "Fixed In Release:"],
  problemDescriptionName: "Problem Description",
  problemAreaHeader: "Problem Area",
  checkBoxLabel: "Exact Match",
  tableHeaders: ["Issue Id", "Title", "Severity", "Found In Release", "Date Submitted", "Date Closed", "Confidence (%)", "Confirm"],
  cardLables: ["Dev Track", "Release Notes", "FSB", "Test Plan"],
  logInfo: "Log Info",
  tags: "Tags",
  filterButtons: ["All", "Clear"],
  filterNames: ["Product", "Group", " Severity", "Priority", "Found on Platform", "Fixed in Release", "Found in Release", "Date Closed"],
  tarBall: "TAR Ball",
  labAvailablity: "Lab Availablity",
  buttons: ["Predict", "Reserve", "Refine"],
  potentialSolutionHeader: "Potential Solutions",
  tagHeader: "Further Refine Based On",
  errorMessage: "No Data Found ",
  suggestionsHeader: "Solution Links",
}


export const Sidenav = {
  dashboardText: "Dashboard",
  analysis: "Analysis",
  createAnalysisRequest: "Create Analysis Request",
  referenceData: "Reference Data",
  solutionPrediction: "Solution Prediction",
  knowledgeMap: "Knowledge Map"


}


export const editReferenceScreen = {
  breadcrumbs: ["Reference >", "Reference View"],
  addButton: "Add",
  exportButton: "Export",
  cancelButton: "Cancel",
  updateButton: "Update",
  backButton: "Back",
  createButton: "Create"
}

export const testPlanScreen = {
  breadcrumbs: ["Knowledge Map > Test Plan"],
  PopUpHeaders: ["Test Plan Details"],
  popUpFields: ["File Name :", "Objective :", "Procedure :", "Expected Result :", "Setup :"],
  addButton: "Create Test Plan",
  exportButton: "Export",
  cancelButton: "Cancel",
  updateButton: "Update",
  tableName: "Test Plan Details",
  backButton: "Back",
  createButton: "Create"
}


// export const  partsFileData={
//     title:"Parts Details",
//     partsColumnList:[
//         {
//           columnName: "Part Name",
//           formName: "part_name",
//           value: "",
//           placeHolder: "AAM-B2"
//         },
//         {
//           columnName: "Material Number",
//           formName: "material_number",
//           value: "",
//           placeHolder: "1000009"
//         },
//         {
//           columnName: "Part Reliability Class",
//           formName: "part_reliability_class",
//           value: "",
//           placeHolder: "AAM"
//         },
//         {
//           columnName: "Spared Attribute",
//           formName: "spared_attribute",
//           value: "",
//           placeHolder: "1"
//         },
//         {
//           columnName: "Standard Cost ($)",
//           formName: "standard_cost",
//           value: "",
//           placeHolder: "2,108.94"
//         }
//       ],
//       partsColumnDefs:[
//         {
//           headerName: "Part Name",
//           field: "part_name",
//           width: 250
//         },
//         {
//           headerName: "Material Number",
//           field: "material_number",
//           width: 150,
//           cellStyle: { "text-align": "right" }
//         },
//         {
//           headerName: "Part Number",
//           field: "part_number",
//           width: 150,
//           cellStyle: { "text-align": "right" }
//         },
//         {
//           headerName: "Part Reliability Class",
//           field: "part_reliability_class",
//           width: 150
//         },
//         {
//           headerName: "Spared Attribute",
//           field: "spared_attribute",
//           width: 150,
//           filter: "date"
//         },
//         {
//           headerName: "Standard Cost ($)",
//           field: "standard_cost",
//           width: 150,
//           filter: "date",
//           cellStyle: { "text-align": "right" }
//         }
//       ]

// }
