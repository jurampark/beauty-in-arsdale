/**
 * Created by Park-Kunbae on 14. 4. 10.
 */
$(function(){
   $('select.product-num').change(function(e){
       var productPrice = 0;
       var deliveryPrice = 0;
       var totalProductPrice =  $('#totalProductPrice');
       var totalPurchasePrice = $('#totalPurchasePrice');

       $('select.product-num').each(function(i, v){
           var num = parseInt($(this).val());
           var isSet = $(this).attr('data-isSet');
           var key = $(this).attr('data-attr');
           var price = 0;
           if(isSet=='true'){
               price = parseInt($('#setPrice-'+key).text());
               productPrice += (price * num);
           }else{
               price = parseInt($('#productPrice-'+key).text());
               productPrice += (price * num);
           }
       });

       totalProductPrice.text(productPrice);
       totalPurchasePrice.text(productPrice + deliveryPrice);
   });

   var fixDiv = function() {
        var b = $(window).scrollTop();
        var d = $("#cartPageWrapper").offset().top;
        var c = $("#puchaseInfoBox");
        if (b > d-50) {
            c.css({position:"fixed",top:"70px"})
        } else {
            c.css({position:"absolute",top:"20px"})
        }
    };
   $(window).scroll(fixDiv);
   fixDiv();

   $('#setAllCheck').click(function(e){
      var isChecked = $(this).is(':checked');
      if(!isChecked)
        $('.set-checkbox').attr('checked',false);
      else
        $('.set-checkbox').attr('checked',true);
   });

   $('#productAllCheck').click(function(){
      var isChecked = $(this).is(':checked');
      if(!isChecked)
        $('.product-checkbox').attr('checked',false);
      else
        $('.product-checkbox').attr('checked',true);
   });
});