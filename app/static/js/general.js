


$( "#contact-form" ).submit(function( event ) {

  // Stop form from submitting normally
  event.preventDefault();

  //Get all data from inputs
  data = {};
  for(var inp in $form.find("input")){
    data[inp.name] = inp.val();
  }
  console.log(data);
  return false;

  // Get some values from elements on the page:
  var $form = $( this ),
    term = $form.find( "input[name='s']" ).val(),
    url = $form.attr( "action" );

  // Send the data using post
  var posting = $.post( url, { s: term } );

  // Put the results in a div
  posting.done(function( data ) {
    var content = $( data ).find( "#content" );
    $( "#result" ).empty().append( content );
  });
});
