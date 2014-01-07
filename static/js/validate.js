define(function(require,exports,module){
	var $ = require("libs/jquery-1.7.2");

	/**
	 * 验证是否为正确的邮箱格式
	 * return 
	 *    true or false
	 */
	module.isEmail = function(email){
	    var re_email = new RegExp("^([a-zA-Z0-9]+[_|\_|.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|.]?)*[a-zA-Z0-9]+.[a-zA-Z]{2,3}$");
	    if(re_email.test(email)){
	        return true; 
	    }else{
	        return false;
	    }
	}
});