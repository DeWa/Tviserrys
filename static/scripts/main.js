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
          alert('success');
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
          alert('success');
      }
    } );

});

$(".reply-tviit-button").click(function () {
    $(this).parent().parent().parent().parent().next(".reply-tviit").toggle();
    if($(this).html() == 'Reply') {
        $(this).html('Hide');
    } else {
        $(this).html('Reply');
    }

});