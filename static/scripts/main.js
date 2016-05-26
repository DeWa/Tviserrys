$( document ).ready(function() {
    $(".reply-tviit").hide();
});

$( "#submitTviit" ).click(function() {
    var data = new FormData($('#tviitForm').get(0));
    var form = $('#tviitForm');

    $.ajax( {
      type: "POST",
      url: form.attr( 'action' ),
      data: data,
      cache: false,
      processData: false,
      contentType: false,
      success: function( response ) {
          form[0].reset();
          location.reload();
      }
    } );

});

$( ".submitReply" ).click(function() {
    var form = $(this).parent();
    var data = new FormData(form.get(0));

    $.ajax( {
      type: "POST",
      url: form.attr( 'action' ),
      data: data,
      cache: false,
      processData: false,
      contentType: false,
      success: function( response ) {
          form[0].reset();
          location.reload();
      }
    } );

});

$(".reply-tviit-button").click(function () {
    $(this).parent().parent().parent().parent().next(".reply-tviit").toggle();
});

$(".follow-button").click(function () {
    var username = $(this).attr('data-user');
    var csrftoken = $.cookie("csrftoken");
     $.ajax({
         type: "POST",
         data: {
            csrfmiddlewaretoken: csrftoken
         },
         url: "/profile/follow/" + username + "/",
         success: function (response) {
             console.log("success");
         }
     });
});