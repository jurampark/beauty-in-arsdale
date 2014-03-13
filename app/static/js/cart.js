/**
 * Created by Park-Kunbae on 14. 3. 13.
 */

$(function(){
    var updateTotalCost = function(cost){
        $('#total-cost span').text(cost);
    };

    var updatePrice = function(){
       var totalCost = 0;
       $('select.product-cnt-selectbox').each(function(i, val){
           var id=  $(this).attr('data-id');
           var cnt = $(this).val();

           var price = parseInt($('#'+id+'-price').text())
           totalCost += price * cnt;
        });
        updateTotalCost(totalCost);
    };

    var deleteProduct = function(id){
        $('#'+id+' select.product-cnt-selectbox').off('change');
        $('#'+id+' .product-del-btn').off('click');
        $('#'+id).remove();
        updatePrice();
    };


    $('select.product-cnt-selectbox').change(function(){
        updatePrice();
    });

    $('.product-del-btn').click(function(){
       deleteProduct($(this).attr('data-id'));
    });

    updatePrice();
});
