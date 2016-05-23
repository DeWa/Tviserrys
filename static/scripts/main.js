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
        alert('success');
      }
    } );

});