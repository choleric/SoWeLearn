define(function(require,exports,module){
	var $ = require("libs/jquery-1.7.2");
    require('libs/jquery.cookie')($);
    require('libs/jquery.tipsy')($);

    var tools = require('tools');
    var validate = require('validate');
	
	tools.getToken();
	removeErrorHint();

	//login
	$(".login .loginBtn").bind("click",function(){
		event.stopPropagation();//阻止冒泡
		login();
		removeErrorHint();
		return false;
	});

	//bind click event to the signup link
	$(".login .J_toSignup").bind("click",function(){
		$(".login").fadeOut();
		$(".signup").fadeIn();
		tools.getToken();
		$(".rightUp .tooltip").tipsy("hide");
	});

	function login(){
		var accounts = $("#loginForm").serialize();
		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/login/";
		option.error = displayLoginErrorInfo;
		option.success = loginSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}

	function displayLoginErrorInfo(data){
		console.log(data.responseText);
	}
	function loginSuccess(data){
		console.log(data.location);
		if(data.location){
			window.location.href = data.location;
		}
		var errorCode = data.c;
		if(errorCode == "212"){
			var d = data.d;
			for(var i = 0, l = d.length; i < l; i++){
				if(d[i]=="0"){
					showErrorInfo($(".J_emailError"),$("#loginEmail"),"Your Email Address is incorrectly formatted.");
				}else if(d[i]=="1"){
					showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Sorry,wrong password.");
				}
			}
		}else if(errorCode == "211"){
			showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Sorry,wrong password.");
		}
	}
	function removeErrorHint(){
		$(".loginForm input").each(function(index){
			$(this).bind('focus', function(event) {
				$(this).removeClass('error');
				$(this).next().hide();
			});
		});
		$(".signupForm input").each(function(index){
			$(this).bind('focus', function(event) {
				$(this).removeClass('error');
				$(this).next().hide();
			});
		});
	}
	(function validateLoginInput(){
		$("#loginEmail").bind('blur', function(event) {
			if(!validate.isEmail(this.value)){
				showErrorInfo($(".J_emailError"),$("#loginEmail"),"Your Email Address is incorrectly formatted.");
			}
		});
		$("#loginPassword").bind('blur', function(event) {
			if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
				showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Your password must be at least 6 characters long.");
			}
		});	
	})();

	//signup
	$(".signup .J_signupBtn").bind('click', function(event) {
	    event.stopPropagation();//阻止冒泡
	    signup();
	    return false;
	});
	function signup(){
		var accounts = $("#signupForm").serialize();
		// accounts._t = $.cookie("_t");

		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/signup/";
		option.error = displaySignupErrorInfo;
		option.success = signupSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}

	(function validateSigupInput(){
		$("#signUpEmail").bind('blur', function(event) {
			if(!validate.isEmail(this.value)){
				showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"Your Email Address is incorrectly formatted.");
			}
		});
		$("#signUpPassword1").bind('blur', function(event) {
			if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
				showErrorInfo($(".J_passwordSignError1"),$("#signUpPassword1"),"Your password must be at least 6 characters long.");
			}
		});	
		$("#signUpPassword2").bind('blur', function(event) {
			var pwd1 = $("#signUpPassword1").val();
			var pwd2 = $("#signUpPassword2").val();
			if(pwd2 != ""){
				if(pwd1 != pwd2){
					showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Different password.");
				}else{
					$(".J_passwordSignError2").hide();
					$("#signUpPassword2").removeClass('error');
				}
			}else{
				showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Your password must be at least 6 characters long.");

			}
		});	
		$("#signFirstName").bind('blur', function(event) {
			if($.trim(this.value) == ""){
				showErrorInfo($(".J_firstNameError"),$("#signFirstName"),"Please enter first name.");
			}
		});	
		$("#signLastName").bind('blur', function(event) {
			if($.trim(this.value) == ""){
				showErrorInfo($(".J_lastNameError"),$("#signLastName"),"Please enter last name.");
			}
		});	
	})();
	function displaySignupErrorInfo(data){
		console.log(data);
	}
	function signupSuccess(data){
		console.log(data.location);
		if(data.location){
			window.location.href = data.location;
		}
		var errorCode = data.c;
		if(errorCode == "201"){
			var d = data.d;
			for(var i = 0, l = d.length; i < l; i++){
				switch(d[i]){
					case 0:
						showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"Your Email Address is incorrectly formatted.");
						break;
					case 1:
						showErrorInfo($(".J_passwordSignError1"),$("#signUpPassword1"),"Your password must be at least 6 characters long.");
						break;
					case 2:
						showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Your password must be at least 6 characters long.");
						break;
					case 3:
						showErrorInfo($(".J_firstNameError"),$("#signFirstName"),"Please enter first name.");
						break;
					case 4:
						showErrorInfo($(".J_lastNameError"),$("#signLastName"),"Please enter last name.");
						break;
				}
			}
		}else if(errorInfo == "202"){
			showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"User Exist.");
		}else if(errorInfo == "203"){
			showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Different password.");
		}
	}

	function showErrorInfo(errinfoObj, inputObj, errorInfo){
		$(errinfoObj).children(".content").html(errorInfo);
		errinfoObj.show();
		inputObj.addClass('error');
	}
});















