$(document).ready(function(){
	$('#like_photo1_btn').click(function(){
		var photoIdVar;
		photoIdVar = $(this).attr('data-photoid');
		
		$.get('/fooodie/like_photo/', 
			{'photo_id' : photoIdVar}, 
			function(data){
				$('#photo1pic').attr('href', data.photo1.url);
				$('#photo1pic').attr('style', "background-image: url("+data.photo1.url+");");
				$('#photo1name').html(data.photo1.name);
				$('#photo1author').html("Author: "+data.photo1.username);
				$('#photo1_likes').html("Number of votes: "+data.photo1.votes);
				$('#like_photo1_btn').attr('data-photoid', data.photo1.id);
				
				$('#photo2pic').attr('href', data.photo2.url);
				$('#photo2pic').attr('style', "background-image: url("+data.photo2.url+");");
				$('#photo2name').html(data.photo2.name);
				$('#photo2author').html("Author: "+data.photo2.username);
				$('#photo2_likes').html("Number of votes: "+data.photo2.votes);
				$('#like_photo2_btn').attr('data-photoid', data.photo2.id);
			})
	});
	
	$('#like_photo2_btn').click(function(){
		var photoIdVar;
		photoIdVar = $(this).attr('data-photoid');
		
		$.get('/fooodie/like_photo/', 
			{'photo_id' : photoIdVar}, 
			function(data){
				$('#photo1pic').attr('href', data.photo1.url);
				$('#photo1pic').attr('style', "background-image: url("+data.photo1.url+");");
				$('#photo1name').html(data.photo1.name);
				$('#photo1author').html("Author: "+data.photo1.username);
				$('#photo1_likes').html("Number of votes: "+data.photo1.votes);
				$('#like_photo1_btn').attr('data-photoid', data.photo1.id);
				
				$('#photo2pic').attr('href', data.photo2.url);
				$('#photo2pic').attr('style', "background-image: url("+data.photo2.url+");");
				$('#photo2name').html(data.photo2.name);
				$('#photo2author').html("Author: "+data.photo2.username);
				$('#photo2_likes').html("Number of votes: "+data.photo2.votes);
				$('#like_photo2_btn').attr('data-photoid', data.photo2.id);
			})
	});
});