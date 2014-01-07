define(function(require,exports,module){
	var $ = require("libs/jquery-1.7.2");
    require('libs/jquery.cookie')($);

	//login
	$(".loginBtn").bind("click",loginAjax);

	function loginAjax(){
		var accounts = $("#loginForm").serializeJson();
		accounts._t = $.cookie("_t");
		accounts.remember = "False";

		var option = {};//ajax option
		option.data = accounts;
		option.url = "/accounts/login/";
		sendAjaxRequest(option,$.cookie("_t"));
	}
});