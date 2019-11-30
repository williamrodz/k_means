
var value = 1 

$(document).ready(function(){

	$("#goButton").click(function(){

		$.ajax({

		method: "GET",
		url: "k_means.py",
		data: {"place" : value},
		dataType: "text",
		success: function(result){

		var data=JSON.parse(result);
		console.log(result);
		}

		});

	});
});
