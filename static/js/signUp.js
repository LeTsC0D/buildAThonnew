$(function(){
	$('#btnSignUp').click(function(){

		$.ajax({
			url: '/status',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){

			  console.log(response,response['url'])
				window.location.href = response['url']
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


$(function(){
	$('#mapping').click(function(){

		$.ajax({
			url: '/createmapping',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){

				// print("redirect reached")
				// window.location.href = response['url'];
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
