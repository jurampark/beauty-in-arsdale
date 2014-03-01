$(function(){
		$('div.color-section').click(function(e){
			e.preventDefault();
			var color = $(this).attr('data-attribute');
			$('div.color-section').removeClass('selected-color');
			$(this).addClass('selected-color');
			$('#skin_color').val(color);
		});
	});