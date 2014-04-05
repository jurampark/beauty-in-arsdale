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
            url = "/addProductToInterest";
        else
            url = '/delProductToInterest';

        $.ajax({
				  url: url,
				  dataType: 'json',
				  async : true,
				  type:'POST',
                  data : {product_key : productKey},
				  success: function(data){
                      console.log(data);
					  if(!data.success && data.message == 'login required'){
                          if(confirm('로그인이 필요 합니다. 로그인 하시겠습니까?'))
                            location.href= url_for_login_next;
                      }else if(!data.success){
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }else{
                          if(!done){
                            btn.addClass('disable');
                          }else{
                              btn.removeClass('disable');
                          }
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

        if(!confirm('장바구니에 추가 하시겠습니까?'))
            return;

        $.ajax({
				  url: "/addProductToCart",
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  data:{product_key : productKey},
				  success: function(data){
					  if(!data.success && data.message == 'login required'){
                          if(confirm('로그인이 필요 합니다. 로그인 하시겠습니까?'))
                            location.href= url_for_login_next;
                      }else if(!data.success){
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }else{
                          alert('장바구니에 추가되었습니다.');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
		});
	});

});