
$(function(){
		var container = document.querySelector('#interestGrid');
		var msnry;

		imagesLoaded(container, function(){	//when all images are loaded, it is triggered
			msnry = new Masonry( container, {	// api for displaying images as a grid
			  // options
			  columnWidth: 138,
			  gutter : 1,
			  itemSelector: '.service-list'
			});
		});

		/*
		$('#photo-more-btn').click(function(e){	//when the more button is clicked
			e.preventDefault();
			var count = $('div.item').length;

			if(count % 15 != 0)
				return false;

			$.ajax({	//getting images from the server
				  url: "${contextPath}/Gallery/Get/Page/"+parseInt((count-1)/15 + 2),
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  success: function(data){
					  appendPhoto(data);

				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
			});
		});

		var appendPhoto= function(data){	//appends images into the container to display them as a grid

			var elems = [];
			var fragment = document.createDocumentFragment();
			var imgPath, imgDescription, html, elem;

			for(var i = 0 ; i < data.length; i++){

				imgPath = data[i].img_name;
				imgDescription = data[i].img_description;

				html = '<div class="item"><a href="${contextPath }/Download/Gallery?fileName='+imgPath+'" title="'+imgDescription+'"><img src="${contextPath }/Download/Gallery?fileName=thumbnail.'+imgPath+'"/></a></div>';
				elem = $(html).get(0);
				fragment.appendChild(elem);
				elems.push(elem);
			}
			$('#container').append(fragment);
			imagesLoaded(container, function(){	//only when new images are loaded, it displays them as a grid.
				msnry.appended(elems);
			});
		};
		*/
	});