// Ligmol namespace
var Ligmol = {};

/* Table filter 1 
$(document).ready(function(){
    $("#tableSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#compoundTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });*/

(function($){
    var namespace
    namespace = { 
        updateTbl: function(){
            // Reset Table
            $("#compoundTable td.complexcol").parent().show();

            var filtersNo = [];

            if($(complexfilter).val() && $(complexfilter).val() != "none")
            {
                // Complex filter
                filtersNo.push("#compoundTable td.complexcol:not(:contains('" + $(complexfilter).val() + "'))");
            }

            if($(hostfilter).val() && $(hostfilter).val() != "none")
            {
                // Host filter
                filtersNo.push("#compoundTable td.hostcol:not(:contains('" + $(hostfilter).val() + "'))");
            }

            if($(guestfilter).val() && $(guestfilter).val() != "none")
            {
                // Guest filter
                filtersNo.push("#compoundTable td.guestcol:not(:contains('" + $(guestfilter).val() + "'))");
            }

            if($(averagefilter).val() && $(averagefilter).val() != "none")
            {
                // challenge filter
                filtersNo.push("#compoundTable td.averagecol:not(:contains('" + $(averagefilter).val() + "'))");
            }

            if($(challengefilter).val() && $(challengefilter).val() != "none")
            {
                // Challenge filter
                filtersNo.push("#compoundTable td.challengecol:not(:contains('" + $(challengefilter).val() + "'))");
            }

            $(filtersNo.join(", ")).parent().hide();


            $('#compoundTable tbody tr').each(function() {
                function hideShow(object, element, innerElement, isInt){
                    isInt = isInt || false;
                    
                    if(isInt){
                        var value = parseInt( $(element, innerElement).text(), 10 ) || 0; 
                        var min = parseInt( $(object).val().split(';')[0], 10 );
                        var max = parseInt( $(object).val().split(';')[1], 10 );
                    }
                    else{
                        var value = parseFloat( $(element, innerElement).text(), 10 ) || 0; 
                        var min = parseFloat( $(object).val().split(';')[0], 10 );
                        var max = parseFloat( $(object).val().split(';')[1], 10 );
                    }

                    if(min == max){
                        return;
                    }

                    if ( min > value || max < value ) {
                        $(innerElement).hide()
                    }
                };
                hideShow(gbmodelfilter, 'td.gbmodelcol', this, isInt=true);
                hideShow(intdielfilter, 'td.intdielcol', this, isInt=true);
                hideShow(saltcomfilter, 'td.saltcomcol', this);
                hideShow(mmgbsafilter, 'td.mmgbsacol', this);
                hideShow(nmafilter, 'td.nmacol', this);
                hideShow(delta_gfilter, 'td.delta_gcol', this);
                hideShow(expfilter, 'td.expcol', this);
            });
        }
    };
    window.ligmol = namespace;
})(this.jQuery);

function updateSelects()
{
    var dict = {
        "complexcol" : [],
        "hostcol" : [],
        "guestcol" : [],
        "averagecol" : [],
        "challengecol" : []
    };

    // $('#compoundTable tbody tr').each(function() {
    function fillDict(element)
    {
        this.contained = [];
        var self = this;
        $('#compoundTable tr td.' + element).each(function() {
            var value = $(this).html();
            if(jQuery.inArray(value, self.contained) == -1)
            {
                self.contained.push(value);
                $('#' + element.slice(0, -3) + 'filter').append('<option value="' + value + '">' + value + '</option>');
            }
         });
    };

    fillDict('complexcol');
    fillDict('hostcol');
    fillDict('guestcol');
    fillDict('averagecol');
    fillDict('challengecol');
}

/* Table filter 2 */
$(document).ready(function() {

    updateSelects();

    // PersonalFilterNum Filter
    $(".personalFilterNum").on("change", function () {
        updateTbl();
    });

    // PersonalFilterStr Filter
    $(".personalFilterStr").on("change", function () {
        ligmol.updateTbl();
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