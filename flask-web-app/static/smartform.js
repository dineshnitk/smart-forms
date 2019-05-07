var maxfieldId = 1

// Dinesh AWS Account
var api_endpoint_url = 'https://8a0e9lvnhk.execute-api.us-east-1.amazonaws.com/default/getRecommendationsFunc'

// Dustin AWS acccount
// var api_endpoint_url = 'https://8eupdg6gm2.execute-api.us-east-1.amazonaws.com/default/getRecommendationsFunc'

document.getElementById("myspinner").style.visibility = "hidden";

function showAlert(message) {
  $('#alertuser').html("<div class='alert alert-danger'>" + message + "</div>");
  $('#alertuser').show();
}

function clear_form() {
  var typeObj = document.getElementById('typeInputState')
  if (typeObj.value != 'Select request type...') {
    $('#alertuser').hide()
  }

  for (i = 1; i <= maxfieldId; i++) {
    remove_smartform_field(i);
  }
  maxfieldId = 1;
}

// $('.btn').on('click', function() {
//   console.log("Get recommendations clicked")
//   var $this = $(this);
//   $this.button('loading');
//   get_recommendations();
//   $this.button('reset');
// });

function get_recommendations() {
  var typeObj = document.getElementById('typeInputState')
  if (typeObj.value == 'Select request type...') {
    showAlert("Must select the request type to get recommendations. Please select request type and try again.")
    return
  }
  $('#alertuser').hide()
  document.getElementById("myspinner").style.visibility = "visible";
  $('#recommendationbutton').prop('disabled', true);

  type = typeObj.value;
  fields = 'type';
  var obj = $('input[name="fieldname[]"]');
  $.each(obj, function(index, myelement) {
    var field = myelement.value;
    if (field != '' && field != 'type') {
      fields = fields + "," + myelement.value;
    }
  });
  console.log("fields = " + fields);
  url = api_endpoint_url + '?type=' + type + '&fields=' + fields;
  console.log(url);

  $.getJSON(url, function(result) {
    console.log("result = " + result)
    fieldstr = result['result'];
    console.log('fieldstr = ' + fieldstr)
    if (fieldstr == '') {
      console.log("showAlert : No recommendations for current set of fields")
      showAlert("No recommendations for current set of fields");
    }
    console.log(fieldstr);
    if (fieldstr != '') {
      var newfields = fieldstr.split(',');
      var len = newfields.length;
      for (var i = 0; i < len; i++) {
        console.log(" New field @ index " + i + " = " + newfields[i]);
        create_smartform_field(newfields[i]);
      }
    }
  })
  $('#recommendationbutton').prop('disabled', false);
  document.getElementById("myspinner").style.visibility = "hidden";
}

function create_smartform_field(newfieldname) {
  maxfieldId++;
  var objTo = document.getElementById('smartform_fields')
  var divtest = document.createElement("div");
  divtest.setAttribute("class", "form-group removeclass" + maxfieldId);
  divtest.setAttribute("id", "removeclass" + maxfieldId);
  var rdiv = 'removeclass' + maxfieldId;
  divtest.innerHTML =
    '<div class="form-row">' +
    '<div class="form-group col-md-4">' +
    '<input type="text" class="form-control" id="fieldname" name="fieldname[]" value="' + newfieldname + '" placeholder="Enter field name" required>' +
    '</div>' +
    '<div class="form-group col-md-4">' +
    '<input type="text" class="form-control" id="value" name="value[]" value="" placeholder="Enter value">' +
    '</div>' +
    '<div class="form-group col-md-2">' +
    '<button class="btn btn-success" type="button" onclick="create_smartform_field(\'\');"> + </button>&nbsp' +
    '<button class="btn btn-danger" type="button" onclick="remove_smartform_field(' + maxfieldId + ');"> - </button>' +
    '</div>' +
    '</div>';
  objTo.appendChild(divtest)
}

function remove_smartform_field(rid) {
  $('.removeclass' + rid).remove();
}