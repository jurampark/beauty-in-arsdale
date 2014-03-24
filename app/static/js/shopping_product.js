$(function(){
   $('.carousel').carousel();

    var setItemWidth = function(){
        var width = $('#productGrid').width();
        $('.product-item').css({width : parseInt((width - 10)/2)});
    };

    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width();
        setItemWidth();
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: parseInt(width/ 2),
          gutter : 0,
          itemSelector: '.product-item'
        });
    });
});