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

    // $(".personalFilter").on("keyup change", function () {
    //     var table = $('#compoundTable').DataTable();
    //     $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    //         return parseInt(data[1]) >= parseInt($('#counter-low').val() || data[1]) 
    //             && parseInt(data[1]) <= parseInt($('#counter-high').val() || data[1])
    //     });
    //     $('#counter-low, #counter-high').on('keyup', table.draw);

    // });

    //$(".personalFilter").on("change", function () {
    $(".personalFilter").on("keyup change", function () {
        // Reset
        $("#compoundTable td").parent().show();

        // var filtersYes = [];
        var filtersNo = [];

        if($(complexfilter).val())
        {
            // Complex filter
            // filtersYes.push("#compoundTable td.complexcol:contains('" + $(complexfilter).val() + "')");
            filtersNo.push("#compoundTable td.complexcol:not(:contains('" + $(complexfilter).val() + "'))");
        }

        if($(hostfilter).val())
        {
            // Host filter
            // filtersYes.push("#compoundTable td.hostcol:contains('" + $(hostfilter).val() + "')");
            filtersNo.push("#compoundTable td.hostcol:not(:contains('" + $(hostfilter).val() + "'))");
        }

        if($(guestfilter).val())
        {
            // Guest filter
            // filtersYes.push("#compoundTable td.guestcol:contains('" + $(guestfilter).val() + "')");
            filtersNo.push("#compoundTable td.guestcol:not(:contains('" + $(guestfilter).val() + "'))");
        }

        if($(averagefilter).val())
        {
            // challenge filter
            // filtersYes.push("#compoundTable td.averagecol:contains('" + $(averagefilter).val() + "')");
            filtersNo.push("#compoundTable td.averagecol:not(:contains('" + $(averagefilter).val() + "'))");
        }

        if($(challengefilter).val())
        {
            // Challenge filter
            // filtersYes.push("#compoundTable td.challengecol:contains('" + $(challengefilter).val() + "')");
            filtersNo.push("#compoundTable td.challengecol:not(:contains('" + $(challengefilter).val() + "'))");
        }

        // GBModel filter
        // filtersYes.push("#compoundTable td.gbmodelcol:lt('" + $(gbmodelfilter).val().split(';')[1] + "')");
        // filtersYes.push("#compoundTable td.gbmodelcol:gt('" + $(gbmodelfilter).val().split(';')[0] + "')");
        // filtersNo.push("#compoundTable td.gbmodelcol:not(:lt('" + $(gbmoldefilter).val().split(';')[1] + "'))");
        // filtersNo.push("#compoundTable td.gbmodelcol:not(:gt('" + $(gbmodelfilter).val().split(';')[0] + "'))");

        // Intdiel filter
        // filtersYes.push("#compoundTable td.intdielcol:le(" + $(intdielfilter).val().split(';')[1] + ")");
        // filtersYes.push("#compoundTable td.intdielcol:ge(" + $(intdielfilter).val().split(';')[0] + ")");
        filtersNo.push("#compoundTable td.intdielcol:not(:lt(" + $(intdielfilter).val().split(';')[1] + "))");
        filtersNo.push("#compoundTable td.intdielcol:not(:gt(" + $(intdielfilter).val().split(';')[0] + "))");

        // // saltcom filter
        // filtersYes.push("#compoundTable td.saltcomcol:lt('" + $(saltcomfilter).data("to") + "')");
        // filtersYes.push("#compoundTable td.saltcomcol:gt('" + $(saltcomfilter).data("from") + "')");
        // filtersNo.push("#compoundTable td.saltcomcol:not(:lt('" + $(saltcomfilter).data("to") + "'))");
        // filtersNo.push("#compoundTable td.saltcomcol:not(:gt('" + $(saltcomfilter).data("from") + "'))");

        // // MMGBSA filter
        // filtersYes.push("#compoundTable td.mmgbsacol:lt('" + $(mmgbsafilter).data("to") + "')");
        // filtersYes.push("#compoundTable td.mmgbsacol:gt('" + $(mmgbsafilter).data("from") + "')");
        // filtersNo.push("#compoundTable td.mmgbsacol:not(:lt('" + $(mmgbsafilter).data("to") + "'))");
        // filtersNo.push("#compoundTable td.mmgbsacol:not(:gt('" + $(mmgbsafilter).data("from") + "'))");

        // // NMA filter
        // filtersYes.push("#compoundTable td.nmacol:lt('" + $(nmafilter).data("to") + "')");
        // filtersYes.push("#compoundTable td.nmacol:gt('" + $(nmafilter).data("from") + "')");
        // filtersNo.push("#compoundTable td.nmacol:not(:lt('" + $(nmafilter).data("to") + "'))");
        // filtersNo.push("#compoundTable td.nmacol:not(:gt('" + $(nmafilter).data("from") + "'))");

        // // Delta_G filter
        // filtersYes.push("#compoundTable td.delta_gcol:lt('" + $(delta_gfilter).data("to") + "')");
        // filtersYes.push("#compoundTable td.delta_gcol:gt('" + $(delta_gfilter).data("from") + "')");
        // filtersNo.push("#compoundTable td.delta_gcol:not(:lt('" + $(delta_gfilter).data("to") + "'))");
        // filtersNo.push("#compoundTable td.delta_gcol:not(:gt('" + $(delta_gfilter).data("from") + "'))");

        // // exp filter
        // filtersYes.push("#compoundTable td.expcol:lt('" + $(expfilter).data("to") + "')");
        // filtersYes.push("#compoundTable td.expcol:gt('" + $(expfilter).data("from") + "')");
        // filtersNo.push("#compoundTable td.expcol:not(:lt('" + $(expfilter).data("to") + "'))");
        // filtersNo.push("#compoundTable td.expcol:not(:gt('" + $(expfilter).data("from") + "'))");

        // $(filtersYes.join(", ")).parent().show();
        $(filtersNo.join(", ")).parent().hide();
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