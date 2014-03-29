/**
 * Created by Park-Kunbae on 14. 3. 27.
 */
$(function(){


   $('.change-product').click(function(e){
       e.preventDefault();
       removeSelectedBox();
       $('#currentSetPrice').text('10만 2000원');
       $(this).addClass('change-product-selected');
   });

   $('#completeChangeBtn').click(function(e){
       e.preventDefault();
       location.href="/setdetail";
   });

   var removeSelectedBox = function(){
       $('.change-product').removeClass('change-product-selected');
   };

});