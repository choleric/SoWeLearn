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
					$(".J_emailError").val("Your Email Address is incorrectly formatted.").show();
					$("#loginEmail").addClass('error');
				}else if(d[i]=="1"){
					$("#loginPassword").addClass('error');
					$(".J_passwordError").val("Sorry,wrong password.").show();
				}
			}
		}else if(errorCode == "211"){
			$("#loginPassword").addClass('error');
			$(".J_passwordError").val("Sorry,wrong password.").show();
		}
	}
	function removeErrorHint(){
		// $(".loginForm input[type='text']").each(function(index){
		// 	$("this").bind('focus', function(event) {
		// 		$(this).removeClass('error');
		// 		$(this).next().hide();
		// 	});
		// });
		$("#loginEmail").bind('focus', function(event) {
			$("#loginEmail").removeClass('error');
			$(".J_emailError").val("Your Email Address is incorrectly formatted.").hide();
		});
		$("#loginPassword").bind('focus', function(event) {
			$("#loginPassword").removeClass('error');
			$(".J_passwordError").val("Sorry,wrong password.").hide();
		});
	}
	(function validateLoginInput(){
		$("#loginEmail").bind('blur', function(event) {
			if(!validate.isEmail(this.value)){
				$(".J_emailError").val("Your Email Address is incorrectly formatted.").show();
				$("#loginEmail").addClass('error');
			}
		});
		$("#loginPassword").bind('blur', function(event) {
			if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
				$(".J_passwordError").val("Your password must be at least 6 characters long.").show();
				$("#loginPassword").addClass('error');
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
						$(".J_emailSignError").val("Your Email Address is incorrectly formatted.").show();
						$("#signUpEmail").addClass('error');
						break;
					case 1:
						$(".J_passwordSignError1").val("Your password must be at least 6 characters long.").show();
						$("#signUpPassword1").addClass('error');
						break;
					case 2:
						$(".J_passwordSignError2").val("Your password must be at least 6 characters long.").show();
						$("#signUpPassword2").addClass('error');
						break;
					case 3:
						$(".J_firstNameError").val("Your password must be at least 6 characters long.").show();
						$("#signFirstName").addClass('error');
						break;
					case 4:
						$(".J_lastNameError").val("Your password must be at least 6 characters long.").show();
						$("#signLastName").addClass('error');
						break;
				}
			}
		}
	}
});















