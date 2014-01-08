define(function(require,exports,module){
	var $ = require("libs/jquery-1.7.2");
    require('libs/jquery.cookie')($);
    var tools = require('tools');



	//login
	$(".login .loginBtn").bind("click",function(){
		tools.getToken();
		login();
	});

	//bind click event to the signup link
	$(".login .J_toSignup").bind("click",function(){
		$(".login").fadeOut();
		$(".signup").fadeIn();
	});

	function login(){
		var accounts = tools.serializeJson($("#loginForm"));
		accounts._t = $.cookie("_t");
		accounts.remember = "False";

		var option = {};//ajax option
		option.data = accounts;
		option.url = "/accounts/login/";
		option.error = displayLoginErrorInfo;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}

	function displayLoginErrorInfo(data){
		console.log("login error...");
	}

	//signup
	$(".signup .J_signupBtn").bind('click', function(event) {
	    event.stopPropagation();//阻止冒泡
	    tools.getToken();
	    signup();
	});
	function signup(){
		var accounts = tools.serializeJson($("#signupForm"));
		accounts._t = $.cookie("_t");

		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/signup/";
		option.error = displaySignupErrorInfo;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}
	function displaySignupErrorInfo(){
		console.log("sign up error ....");
	}
});