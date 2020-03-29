$(document).ready(function(){
	$('#like_photo1_btn').click(function(){
		var photoIdVar;
		photoIdVar = $(this).attr('data-photoid');
		
		$.get('/fooodie/like_photo/', 
			{'photo_id' : photoIdVar}, 
			function(data){
				$('#photo1_likes').html(data);
				$('#like_photo1_btn').hide();
			})
	});
	
	$('#like_photo2_btn').click(function(){
		var photoIdVar;
		photoIdVar = $(this).attr('data-photoid');
		
		$.get('/fooodie/like_photo/', 
			{'photo_id' : photoIdVar}, 
			function(data){
				$('#photo2_likes').html(data);
				$('#like_photo2_btn').hide();
			})
	});
});