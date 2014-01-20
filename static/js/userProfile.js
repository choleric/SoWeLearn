define(function(require,exports,module){
    var $ = jQuerys = require("libs/jquery-1.7.2");
    var tools = require('tools');
    
    bindEvent();

    function bindEvent(){
        $(".contsDetail").bind("click",function(e){//给所有有下拉菜单的title绑定点击事件
            var $target = $(e.target);
            if ($target.hasClass('title')) {
                var detailContApp = $target.next();
                if(detailContApp.hasClass('detailContApp') && $target.children('.arrow-right').length){
                    detailContApp.slideDown();
                    $target.children('.arrow-right').removeClass('arrow-right').addClass('arrow-down');
                }else if(detailContApp.hasClass('detailContApp') && $target.children('.arrow-down').length){
                    detailContApp.slideUp();
                    $target.children('.arrow-down').removeClass('arrow-down').addClass('arrow-right');
                }
            }
        });

        //change password
        //cancel
        $("#changePasswordForm .cancel").bind('click', function(event) {
            var detailContApp = $(this).parent().parent();
            detailContApp.slideUp();
            detailContApp.parent().children('.arrow-down').removeClass('arrow-down').addClass('arrow-right');
        });
        //commit ajax request 
        $("#changePasswordForm .changePassword").bind("click", function(){
            var accounts = $("#changePasswordForm").serialize();
            var option = {};//ajax option
            option.data = accounts;
            option.type = "post";
            option.url = "/accounts/password/change/";
            option.cache = false;
            option.error = displayChagnePwdErrorInfo;
            option.success = changePwdSuccess;
            tools.sendAjaxRequest(option,$.cookie("_t"));
        });
        function displayChagnePwdErrorInfo(data){

        }
        function changePwdSuccess(data){
            
        }
    }
});
