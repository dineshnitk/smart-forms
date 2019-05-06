var maxfieldId = 1;
var api_endpoint_url = 'https://8a0e9lvnhk.execute-api.us-east-1.amazonaws.com/default/getRecommendationsFunc'

$('#alertuser').hide()
console.log('maxfieldId =' + maxfieldId)

function showAlert(message) {
  $('#alertuser').html("<div class='alert alert-danger'>" + message + "</div>");
  $('#alertuser').show();
}

// function clear_form() {
//   var typeObj = document.getElementById('typeInputState')
//   if (typeObj.value != 'Select request type...') {
//     $('#alertuser').hide()
//   }
//
//   for (i = 1; i <= maxfieldId; i++) {
//     remove_smartform_field(i);
//   }
//   maxfieldId = 1;
// }

$('#getrecommendations').on('click', function() {
  console.log("Get recommendations clicked")
  var $this = $(this);
  $this.button('loading');
  setTimeout(function() {
    get_recommendations();
    $this.button('reset');
  }, 8000);
});

function get_recommendations() {
  var typeObj = document.getElementById('typeInputState')
  if (typeObj.value == 'Select request type...') {
    showAlert("Must select the request type to get recommendations. Please select request type and try again.")
    return
  }
  $('#alertuser').hide()

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
  //api_endpoint_url = 'https://8eupdg6gm2.execute-api.us-east-1.amazonaws.com/default/getRecommendationsFunc'
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
    '<button class="btn btn-danger" type="button" onclick="remove_smartform_field(' + maxfieldId + ');"> - </button>' +
    '</div>' +
    '</div>';
  objTo.appendChild(divtest)

  // var obj = $('input[name="fieldname[]"]');
  // $.each(obj, function(index, myelement) {
  //   myelement.required = true;
  // });
}

function remove_smartform_field(rid) {
  $('.removeclass' + rid).remove();
}