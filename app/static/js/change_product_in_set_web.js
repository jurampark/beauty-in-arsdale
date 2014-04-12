$(function(){
     $('.product-info-btn').click(function(e){
        e.preventDefault();
        $('#product-detail-modal').modal('show');
    });

     $('.available-product').hover(function(e){
       $(this).children('.available-product-hover-menu').show();
    },function(e){
       $(this).children('.available-product-hover-menu').hide();
    });

    var fixDiv = function() {
        var b = $(window).scrollTop();
        var d = $("#changeProductWrapper").offset().top;
        var c = $("#originProductWrapper");
        if (b > d-50) {
            c.css({position:"fixed",top:"60px"})
        } else {
            c.css({position:"absolute",top:"0px"})
        }
    };
   $(window).scroll(fixDiv);
   fixDiv();
});