/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){
   $('.carousel').carousel();

    var setSetItemWidth = function(){
        var width = $('#setGrid').width();
        $('#setGrid .service-list').css({width : parseInt((width - 6)/2)});
    };

     var setItemWidth = function(){
        var width = $('#productGrid').width();
        $('#productGrid .service-list').css({width : parseInt((width - 6)/3)});
    };

    var container = document.querySelector('#productGrid');
    var setContainer = document.querySelector('#setGrid');
    var msnry, setMsnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width();
        setItemWidth();
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: parseInt(width/ 3),
          gutter : 0,
          itemSelector: '.service-list'
        });
    });

    imagesLoaded(setContainer, function(){	//when all images are loaded, it is triggered
        var width = $('#setGrid').width();
        setSetItemWidth();
        setMsnry = new Masonry( setContainer, {	// api for displaying images as a grid
          // options
          columnWidth: parseInt(width/ 2),
          gutter : 0,
          itemSelector: '.service-list'
        });
    });
});