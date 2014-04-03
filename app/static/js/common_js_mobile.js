/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function(){
    $('.btn-for-interest').click(function(e){
        e.preventDefault();

        var btn = $(this);
        var productKey = btn.attr('data-product');
        var url = '';
        var done = btn.hasClass('disable');

        if(!done)
            url = "/add_product_to_interest/"+productKey;
        else
            url = '/';

        $.ajax({
				  url: url,
				  dataType: 'text/xml',
				  async : true,
				  type:'GET',
				  success: function(data){
					  console.log(data);
                      if(data == 'success' && !done){
                         btn.addClass('disable');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
		});
	});

    $('.btn-for-cart').click(function(e){
        e.preventDefault();
        var productKey = $(this).attr('data-product');
        $.ajax({
				  url: "/add_product_to_cart",
				  dataType: 'text/xml',
				  async : true,
				  type:'GET',
				  data:{product_key : productKey},
				  success: function(data){
					  console.log(data);
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
		});
	});

});