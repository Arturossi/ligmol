/* Table filter 1 
$(document).ready(function(){
    $("#tableSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#compoundTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });*/


/* Table filter 2 */
// $(document).ready(function() {
//     // Setup - add a text input to each footer cell
//     $('#compoundTable thead th').each( function () {
//         var title = $(this).text();
//         $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
//     } );

//     // DataTable
//     var table = $('#compoundTable').DataTable();

//     // Apply the search
//     table.columns().every( function () {
//         var that = this;

//         $( 'input', this.footer() ).on( 'keyup change', function () {
//             if ( that.search() !== this.value ) {
//                 that
//                     .search( this.value )
//                     .draw();
//             }
//         } );
//     } );
// } );

$(function() {
  // This function gets cookie with a given name
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  /*
  The functions below will create a header with csrftoken
  */

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          // or any other URL that isn't scheme relative or absolute i.e relative.
          !(/^(\/\/|http:|https:).*/.test(url));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
});

function checkChecks(e){
    var check = $('#compoundBody').find('input[type=checkbox]:checked').length;

    if(check <= 0)
    {
        alert("Please select at least one value to download.")
        e.preventDefault();
        return false;
    }
    return true;
}

//select all checkboxes
$("#select_all").change(function(){  //"select all" change 
    $("input[name=choices]").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".checkbox" change 
$('input[name=choices]').change(function(){ 
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#select_all").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('input[name=choices]:checked').length == $('input[name=choices]').length ){
		$("#select_all").prop('checked', true);
	}
});

// For detailed info

//select all checkboxes
$("#choicesIDdi").change(function(){  //"select all" change 
    $("input[name=choices]").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".checkbox" change 
$('input[name=choices]').change(function(){ 
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#choicesID").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('input[name=choices]:checked').length == $('input[name=choices]').length ){
		$("#choicesID").prop('checked', true);
	}
});

//select complex checkboxes
$("#choicesIDcomplex").change(function(){  //"select all" change 
    $(".complex").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".complex" change 
$('.complex').change(function(){ 
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#choicesIDcomplex").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('.complex:checked').length == $('.complex').length ){
		$("#choicesIDcomplex").prop('checked', true);
	}
});

//select guest checkboxes
$("#choicesIDguest").change(function(){  //"select all" change 
    $(".guest").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".checkbox" change 
$('.guest').change(function(){ 
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#choicesIDguest").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('.guest:checked').length == $('.guest').length ){
		$("#choicesIDguest").prop('checked', true);
	}
});

//select guest checkboxes
$("#choicesIDhost").change(function(){  //"select all" change 
    $(".host").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".checkbox" change 
$('.host').change(function(){ 
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#choicesIDhost").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('.host:checked').length == $('.host').length ){
		$("#choicesIDhost").prop('checked', true);
	}
});