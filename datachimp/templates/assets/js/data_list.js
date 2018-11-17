$(document).ready(main);

function main() {
  getData(updateMLModelHTML);
}

/**************
 ** State
 **************/
var modelListState = {
      compareMode: false,
      modelCommentedSelected: 0,
      labelNameSelected: '',
      labelModelIdSelected: 0,
      };

var dynamicColumnData = [],
    mlCompareSelected = [],
    paramFieldSelectList = [],
    mlModelTable = {},
    commentRowSelected = 0,
    dataLoadedFlag = false;

/**************
 ** FUNCTIONS
 **************/
function getData(func) {
  var url = "/api/list-data-version/",
    projectId = $('#project-heading').data('project-id');

  $.ajax({
      type: 'GET',
      url: url + projectId,
    })
    .done(function(data) {
      func(data);
    })
    .fail(function(xhr, errmsg, err) {
      console.error("There was an error while experiment data");
    });

    // Hide the loader
    $loading.hide();
}

function getParamFieldData(func){
  var url = "/api/ml-model/get-param/",
    projectId = $('#project-heading').data('project-id');

  $.ajax({
      type: 'GET',
      url: url + projectId,
    })
    .done(function(data) {
      func(data);
    })
    .fail(function(xhr, errmsg, err) {
      console.error("There was an error while retrieving param data");
    });
}

function updateMLModelHTML(data) {
    mlModelTable = $('#ml-model-table-main').DataTable({
    data: data,
    "info": false,
    "bLengthChange": false,
    "stateSave": true,
     rowId: 'id',
    "dom": '<"top"if>rt<"bottom"p><"clear">',
    columns: [
      {
        title: "Sl No",
        target: "sl_no",
        data: null,
        render: function(d, t, r, m) {
          return r.id;
        }
      },
      {
        title: "Data Version",
        target: "ml_name",
        data: "name",
        render: function(d,t,r){
          var name = '';
          if(d == null) d = '';

          // if(r.name === r.version_id){
          //   name = d.substring(0,7);
          // } else {
            name = d;
          // }

          return '<a href="/data-detail/' + r.id + '" title="'+ d +'">' +
               name + '</a>';
        }
      },
      {
        title: "Submitted On",
        target: "ml_submitted_on",
        data: "date_created_epoch",
        sortable: true,
        orderable: true,
        render: function(d, t, r) {
          if(t === "display"){
            d =  moment(d * 1000).format("Do MMM YYYY HH:mm:ss");
          }

          return d;
        }
      },
    ],
  });

}



function copyKey() {
  var copyText = document.getElementById("project-key");
  copyText.select();
  document.execCommand("Copy");
}


// Update the table data with the fresh data fetched every n seconds
function updateData(data){

  for(var i=0; i < data.length; i++){
    var rowData = data[i],
        existingRow = mlModelTable.row('#' + rowData.id);

        if(existingRow.data() === undefined){
          mlModelTable.row.add(rowData).draw(false);
          break;
        }

        existingRow.data(rowData).draw(false);
  }

  updateDynamicColumnData();

  // Check the selected input checkboxes
  for(i in mlCompareSelected){
    $('input[data-model-id="' + mlCompareSelected[i] + '"]').prop("checked", true);
  }

}


function customiseTable(){
  getParamFieldData(showParamField);

  $('#customiseTable').modal('show');
}


function showParamField(data){
  $('#param-field-list').html('');

  for (var i = 0; i < data.length; i++) {
    var html = '',
        checked_string = '';

    if(paramFieldSelectList.indexOf(data[i].parameter) > -1) checked_string = 'checked';

    html = '<li class="list-group-item">'+ data[i].parameter +
      '<span><input  class="pull-right" type="checkbox" value="' +
      data[i].parameter + '" '+ checked_string +' /></span>';

    $('#param-field-list').append(html);
  }
}


function applyCustomization(){
  // Hide dummy columns
  mlModelTable.column( 7 ).visible(false);
  mlModelTable.column( 8 ).visible(false);

  getDynamicColumnData();

  $('#customiseTable').modal('hide');
  }


function getDynamicColumnData(){
  var formData = {
    'project_id' : $('#project-heading').data('project-id'),
    'param_fields' : paramFieldSelectList
  };

  if(paramFieldSelectList.length > 0){
    csrfToAjax();
    $.ajax({
            type: 'POST',
            url: '/api/ml-model/get-param-select-data/' + formData.project_id + '/',
            data: formData,
            encode: true
        })
        .done(function(data) {
          updateDynamicColumnData(data);
          })
        .fail(function(xhr, errmsg, err) {
            console.error("Error with param selected data");
        });

        // Hide the loader
        $loading.hide();
    }
}


function updateDynamicColumnData(data){
  var dummyColumnNames = ['dummy_column1', 'dummy_column2'];

  if (data === undefined){
    data = dynamicColumnData;
  } else {
    dynamicColumnData = data;
  }

  for(var i=0; i < data.length; i++){
    var rowData = data[i],
        existingRow = mlModelTable.row('#' + data[i].id);
        //existingRowData = existingRow.data();
    if(existingRow.data() === undefined) break;

    for(var j=0; j<paramFieldSelectList.length; j++){
      if(data[i].key === paramFieldSelectList[j]){
          existingRow.cell('#' + data[i].id, 7 + j ).data(data[i].value).draw(false);
      }
    }
  }

  for(var k=0; k<paramFieldSelectList.length; k++){
    $( mlModelTable.column( 7 + k ).header() ).text( paramFieldSelectList[k] );
      mlModelTable.column( 7 + k).visible(true);
  }
}


function getLabelsData(modelId){
  $.ajax({
          type: 'GET',
          url: '/api/experiment-label/'+ modelId + '/',
          encode: true
      })
      .done(function(data) {
        showLabelsHTML(data.labels);
      })
      .fail(function(xhr, errmsg, err) {
          console.log("Error");
      });
}


function showLabelsHTML(data){
  $('#label-modal-body').html('');

  for(var i in data){
    var labelHTML = '<div class="row media" > <div class="col-10">'+
                      data[i] +
                    '</div> <div class="col-2">' +
                    '<i class="label-delete fa fa-trash" style="color:red;" ' +
                    'data-label="' + data[i] + '" ></i>' +
                    '</div> </div>';

        $('#label-modal-body').append(labelHTML);
  }
}
/**************
 ** Events
 **************/


$('table').on('change', 'input', function(d) {

  if (this.checked && mlCompareSelected.length < 2) {
    mlCompareSelected.push($(this).data('model-id'));
  } else if (this.checked && mlCompareSelected.length >= 2) {
    this.checked = false;
  } else {
    var index = mlCompareSelected.indexOf($(this).data('model-id'));
    if (index > -1) mlCompareSelected.splice(index, 1);
  }

});

// To delete the project
$('#delete-project-button').click(function() {
  var formData = {
      'project_id': $('#project-heading').data('project-id')
    },
    url = "/api/project/";

  csrfToAjax();
  $.ajax({
      type: 'DELETE',
      url: url,
      data: formData,
      encode: true
    })
    .done(function(data) {
      window.location.href = '/project';
    })
    .fail(function(xhr, errmsg, err) {
      alert("There was an error.");
    });
});


// Instantiate the copy of project key
new ClipboardJS('#project-copy');


// Get the updated data every 10 seconds
setInterval(function(){
  getData(updateData);
  getDynamicColumnData();
}, 10000);
