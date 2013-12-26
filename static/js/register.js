$(document).ready( function(){
	init();
});

function init(){
	//注册表单
	$("#registeBtn").bind("click",signup);
	//邮箱验证
	$("#userEmail").bind("blur",validateUserEmail);
	//密码验证
	$("#password1").bind("blur",isPasswordEmputy);
	$("#password2").bind("blur",validatePassword);

}

function signup(){
	//validate
	$("#signupForm").validate();

	var accounts = $("#signupForm").serializeJson();

	sendAjaxRequest(accounts,"/accounts/signup/",function(){});
}

//validate the userEmail
function validateUserEmail(){
	var email = $("#userEmail").val();
	if(isEmail(email)){
		$(".email .error").html("");
	}else{
		$(".email .error").html("Please enter a valid email address");
	}
}
//判断是否为空
function isPasswordEmputy(){
	var pwd1 = $("#password1").val();
	if(pwd1 == ""){
		$(".password1 .error").html("不能为空");
	}else{
		$(".password1 .error").html("");
	}		
}
//validate the password
function validatePassword(){
	var pwd1 = $("#password1").val();
	var pwd2 = $("#password2").val();
	if(pwd2 != ""){
		if(pwd1 != pwd2){
			$(".password2 .error").html("两次密码不一致")
		}else{
			$(".password2 .error").html("");
		}
	}else{
		$(".password2 .error").html("不能为空");
	}
	
}