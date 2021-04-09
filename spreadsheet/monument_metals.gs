function onOpen() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{
    name : "Refresh",
    functionName : "refreshLastUpdate"
  }];
  sheet.addMenu("Monument Metals", entries);
};

function refreshLastUpdate() {
  // Unless a value changes the sheet won't update the functions automatically. 
  SpreadsheetApp.getActiveSpreadsheet().getRange('$Z$1').setValue(Math.random());
}

function ProductItemCalc(sku, $Z$1) {
  function get_by_name(name) {
    var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
    for (var i = 0; i < sheets.length; i++) {
      if (sheets[i].getName() == name) {
          return sheets[i];
      }
    }
  }
  
  function find_product_val(sheet, sku) {
    var vals = sheet.getSheetValues(1,1,10000,3); 
    for (var i = 0; i < vals.length; i++) {
      if (vals[i][1] == sku) {
        return vals[i][2];
      }
    }
    throw new Error( "No weight could be found for the sku." );
  }
  
  if (sku == "") {
    throw new Error( "Blank SKU." );
  }
  weights = get_by_name("Weight");
  SpreadsheetApp.flush();
  return find_product_val(weights, sku);
}
