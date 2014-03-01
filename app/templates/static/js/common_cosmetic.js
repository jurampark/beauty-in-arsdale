$(function(){
	

	$( "a" ).on( "click", function( event ) {
	
		event.preventDefault();
		$.mobile.navigate( $(this).attr( "href" ), {
			foo: $(this).attr("data-foo")
		});
	
		// Hypothetical content alteration based on the url. E.g, make
		// an Ajax request for JSON data and render a template into the page.
		//alterContent( $(this).attr("href") );
	});
	
	
	$( window ).on( "navigate", function( event, data ){
		console.log(data.state.foo);
		console.log(data);
		if ( data.state.foo ) {
			// Make use of the arbitrary data stored
			console.log('foo ! ' + data.state.foo);
		}
	
		if ( data.state.direction == "back" ) {
			// Make use of the directional information
			console.log('back is clikced');
		}
	
		// reset the content based on the url
		//alterContent( data.state.url );
	});

});