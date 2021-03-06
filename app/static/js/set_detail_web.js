/**
 * Created by Park-Kunbae on 14. 4. 3.
 */


$(function(){

    $('.product-info-btn').click(function(e){
        e.preventDefault();
        $('#product-detail-modal').modal('show');
    });


    $('.product-gallery').magnificPopup({
		delegate: 'a',
		type: 'image',
		tLoading: 'Loading image #%curr%...',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		},
		image: {
			tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
		}
	});

    $('.belong-to-set-item').hover(function(e){
       $(this).children('.belong-item-hover-menu').show();
    },function(e){
       $(this).children('.belong-item-hover-menu').hide();
    });
});