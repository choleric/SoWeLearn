$(document).ready( function(){
	init();
});

function init(){
	$("#registeBtn").bind("click",signup);
}

function signup(){
	// var accounts = {};
	// accounts.email = $("#userEmail").val();
	// accounts.password1 = $("#password1").val();
	// accounts.password2 = $("#password2").val();
	// accounts.userFirstName = $("#firstName").val();
	// accounts.userLastName = $("#lastName").val();

	var accounts = $("#signupForm").serializeJson();
	sendAjaxRequest(accounts,"/accounts/signup/",function(){});
}