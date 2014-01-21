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
	$(".login .J_toForgotPassword").bind("click",function(){
		$(".login").fadeOut();
		$(".forgotPassword").fadeIn();
		tools.getToken();
		$(".rightUp .tooltip").tipsy("hide");
		return false;
	});

	$(".login .J_toSignup").bind("click",function(){
		$(".login").fadeOut();
		$(".signup").fadeIn();
		tools.getToken();
		$(".rightUp .tooltip").tipsy("hide");
		return false;
	});

	function login(){
		var accounts = $("#loginForm").serialize();
		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/login/";
		option.cache = false;
		option.error = displayLoginErrorInfo;
		option.success = loginSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}

	function displayLoginErrorInfo(data){
		console.log(data.c);
	}
	function loginSuccess(data){
		if(data.c == "0"){
			window.location.href = data.d;
		}
		var errorCode = data.c;
		if(errorCode == "212"){
			var d = data.d;
			for(var i = 0, l = d.length; i < l; i++){
				if(d[i]=="0"){
					tools.showErrorInfo($(".J_emailError"),$("#loginEmail"),"Your Email Address is incorrectly formatted.");
				}else if(d[i]=="1"){
					tools.showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Sorry,wrong password.");
				}
			}
		}else if(errorCode == "211"){
			tools.showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Sorry,wrong password.");
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
				tools.showErrorInfo($(".J_emailError"),$("#loginEmail"),"Your Email Address is incorrectly formatted.");
			}
		});
		$("#loginPassword").bind('blur', function(event) {
			if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
				tools.showErrorInfo($(".J_passwordError"),$("#loginPassword"),"Your password must be at least 6 characters long.");
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
				tools.showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"Your Email Address is incorrectly formatted.");
			}
		});
		$("#signUpPassword1").bind('blur', function(event) {
			if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
				tools.showErrorInfo($(".J_passwordSignError1"),$("#signUpPassword1"),"Your password must be at least 6 characters long.");
			}
		});	
		$("#signUpPassword2").bind('blur', function(event) {
			var pwd1 = $("#signUpPassword1").val();
			var pwd2 = $("#signUpPassword2").val();
			if(pwd2 != ""){
				if(pwd1 != pwd2){
					tools.showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"The passwords for the two fields are different.");
				}else{
					$(".J_passwordSignError2").hide();
					$("#signUpPassword2").removeClass('error');
				}
			}else{
				tools.showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Your password must be at least 6 characters long.");

			}
		});	
		$("#signFirstName").bind('blur', function(event) {
			if($.trim(this.value) == ""){
				tools.showErrorInfo($(".J_firstNameError"),$("#signFirstName"),"Please enter first name.");
			}
		});	
		$("#signLastName").bind('blur', function(event) {
			if($.trim(this.value) == ""){
				tools.showErrorInfo($(".J_lastNameError"),$("#signLastName"),"Please enter last name.");
			}
		});	
	})();
	function displaySignupErrorInfo(data){
		console.log(data);
	}
	function signupSuccess(data){
		if(data.location){
			window.location.href = data.location;
		}
		var errorCode = data.c;
		if(errorCode == "201"){
			var d = data.d;
			for(var i = 0, l = d.length; i < l; i++){
				switch(d[i]){
					case 0:
						tools.showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"Your Email Address is incorrectly formatted.");
						break;
					case 1:
						tools.showErrorInfo($(".J_passwordSignError1"),$("#signUpPassword1"),"Your password must be at least 6 characters long.");
						break;
					case 2:
						tools.showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"Your password must be at least 6 characters long.");
						break;
					case 3:
						tools.showErrorInfo($(".J_firstNameError"),$("#signFirstName"),"Please enter first name.");
						break;
					case 4:
						tools.showErrorInfo($(".J_lastNameError"),$("#signLastName"),"Please enter last name.");
						break;
				}
			}
		}else if(errorInfo == "202"){
			tools.showErrorInfo($(".J_emailSignError"),$("#signUpEmail"),"User Exist.");
		}else if(errorInfo == "203"){
			tools.showErrorInfo($(".J_passwordSignError2"),$("#signUpPassword2"),"The passwords for the two fields are different.");
		}
	}

	//forgot password
	$(".forgotPassword .forgotPasswordBtn").bind('click', function(event) {
	    event.stopPropagation();//阻止冒泡
	    fogotPassword();
	    return false;
	});
	function fogotPassword(){
		var accounts = $("#forgotPasswordForm").serialize();
		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/password/reset/";
		option.error = displayForgotPasswordErrorInfo;
		option.success = forgotPasswordSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}
	function displayForgotPasswordErrorInfo(data){
		console.log(data.responseText);
	}
	function forgotPasswordSuccess(data){
		var code = data.c || "";
		if(code == "0"){
			window.location.href = data.d;
		}
		if(code == "206"){
			tools.showErrorInfo($(".J_emailForgotPasswordError"),$("#forgotPasswordEmail"),"Email does not exist.");
		}else if(code == "207"){
			tools.showErrorInfo($(".J_emailForgotPasswordError"),$("#forgotPasswordEmail"),"Reset Password Failure.");
		}
	}

	//reset Password
	function resetPassword(){
		var accounts = $("#XXXXXXXForm").serialize();
		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/password/reset/key/(?P[0-9A-Za-z]+)-(?P.+)/";
		option.error = displayResetPasswordErrorInfo;
		option.success = resetPasswordSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}
	function displayResetPasswordErrorInfo(data){
		console.log(data.responseText);
	}
	function resetPasswordSuccess(data){
		var code = data.c || "";
		if(code == "0"){
			window.location.href = data.d;
		}else if(code == "203"){
			console.log("password1 and password2 are different.");
		}else if(code == "208"){
			console.log("other problem.");
		}else if(code == "209"){
			console.log("request token is invalid.");
		}
	}

	//change password
	function changePassword(){
		var accounts = $("#*******Form").serialize();
		var option = {};//ajax option
		option.data = accounts;
		option.type = "post";
		option.url = "/accounts/password/change/";
		option.error = displayChangePasswordErrorInfo;
		option.success = changePasswordSuccess;
		tools.sendAjaxRequest(option,$.cookie("_t"));
	}
	function displayChangePasswordErrorInfo(data){
		console.log(data.responseText);
	}
	function changePasswordSuccess(data){
		var code = data.c || "";
		if(code == "0"){
			window.location.href = data.d;
		}else if(code == "204"){
			console.log("Common failure: d is the index of the field that went wrong in this list");
		}else if(code == "205"){
			console.log("Wrong old password;");
		}else if(code == "203"){
			console.log("Different password");
		}
	}

});















