/**
 * Created by Park-Kunbae on 14. 3. 27.
 */
$(function(){
   $('.product-menu-btn').click(function(e){
       e.preventDefault();
       var el = $('#changeProductPopup');
       el.popup('open',{positionTo : 'window'});
   });

   $('#newProductBtn').click(function(e){
       e.preventDefault();
       $('#askArea').addClass('hideArea');
       $('#changeProductArea').removeClass('hideArea');
   });

   $('.change-product').click(function(e){
       e.preventDefault();
       removeSelectedBox();
       $(this).addClass('change-product-selected');
   });

   $('#selectNewBtn').click(function(e){
       e.preventDefault();
        var el = $('#changeProductPopup');
       el.popup('close');
   });

   var removeSelectedBox = function(){
       $('.change-product').removeClass('change-product-selected');
   };
/*
   $('.change-product-btn').click(function(e){
       e.preventDefault();

       var el = $('#changeProductPopup');
       console.log('haha');
       el.popup('open',{positionTo : 'window'});
   });
   */
});