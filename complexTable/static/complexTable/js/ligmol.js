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
$(document).ready(function() {
    $(".personalFilter").on("change", function () {
        // var $inp = $(this);
        // var fromVal = $inp.prop("from"); // reading input from value
        // var toVal = $inp.prop("to"); // reading input to value

        // Reset
        $("#compoundTable td").parent().show();

        console.log($(complexfilter).val())
        console.log($(hostfilter).val())
        console.log($(guestfilter).val())
        console.log($(averagefilter).val())
        console.log($(delta_gfilter).val())
        console.log($(challengefilter).val())

        if($(complexfilter).val())
        {
            // Complex filter
            $("#compoundTable td.complexcol:contains('" + $(complexfilter).val() + "')").parent().show();
            $("#compoundTable td.complexcol:not(:contains('" + $(complexfilter).val() + "'))").parent().hide();
        }

        if($(hostfilter).val())
        {
            // Host filter
            $("#compoundTable td.hostcol:contains('" + $(hostfilter).val() + "')").parent().show();
            $("#compoundTable td.hostcol:not(:contains('" + $(hostfilter).val() + "'))").parent().hide();
        }

        if($(guestfilter).val())
        {
            // Guest filter
            $("#compoundTable td.guestcol:contains('" + $(guestfilter).val() + "')").parent().show();
            $("#compoundTable td.guestcol:not(:contains('" + $(guestfilter).val() + "'))").parent().hide();
        }

        if($(averagefilter).val())
        {
            // challenge filter
            $("#compoundTable td.averagecol:contains('" + $(averagefilter).val() + "')").parent().show();
            $("#compoundTable td.averagecol:not(:contains('" + $(averagefilter).val() + "'))").parent().hide();
        }

        if($(delta_gfilter).val())
        {
            // DeltaG filter
            $("#compoundTable td.deltagcol:contains('" + $(delta_gfilter).val() + "')").parent().show();
            $("#compoundTable td.deltagcol:not(:contains('" + $(delta_gfilter).val() + "'))").parent().hide();
        }

        if($(challengefilter).val())
        {
            // Challenge filter
            $("#compoundTable td.challengecol:contains('" + $(challengefilter).val() + "')").parent().show();
            $("#compoundTable td.challengecol:not(:contains('" + $(challengefilter).val() + "'))").parent().hide();
        }
    });
} );

/* crsftoken function */
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