/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){

    var setItemWidth = function(){
        var width = $('#productGrid').width();
        $('.product-item').css({width : 460});//parseInt((width - 6)/3)});
    };

    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width()-2;
        setItemWidth();
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: 470,//parseInt(width/ 3),
          gutter : 0,
          itemSelector: '.product-item'
        });
    });
});