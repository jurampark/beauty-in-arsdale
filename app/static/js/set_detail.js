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
      location.href='/changeproductinset';
   });



});