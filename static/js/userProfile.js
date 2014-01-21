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
            detailContApp.prev().children('.arrow-down').removeClass('arrow-down').addClass('arrow-right');
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
            var code = data.c;
            if(code == "0"){
                // window.location.href = data.d;
            }else if(code == "204"){
                var d = data.d;
                for(var i = 0, l = d.length; i < l; i++){
                    switch(d[i]){
                        case 0:
                            tools.showUpErrorInfo($("#changePasswordForm .J_changePwdOldErr"),$("#changePasswordForm .J_changePwdOld"),"Your password must be at least 6 characters long.");
                            break;
                        case 1:
                            tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew1Err"),$("#changePasswordForm .J_changePwdNew1"),"Your password must be at least 6 characters long.");
                            break;
                        case 2:
                            tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew2Err"),$("#changePasswordForm .J_changePwdNew2"),"Your password must be at least 6 characters long.");
                            break;
                    }
                }
            }else if(code == "205"){
                tools.showUpErrorInfo($("#changePasswordForm .J_changePwdOldErr"),$("#changePasswordForm .J_changePwdOld"),"Wrong old password.");
            }else if(code == "203"){
                tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew2Err"),$("#changePasswordForm .J_changePwdNew2"),"The passwords for the two fields are different.");
            }
        }
        (function removeErrorHint(){
            $("#changePasswordForm input").each(function(index){
                $(this).bind('focus', function(event) {
                    $(this).removeClass('error');
                    $(this).prev().hide();
                });
            });
        })();
        (function validateChangePasswordForm(){
            $("#changePasswordForm .J_changePwdOld").bind('blur', function() {
                if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
                    tools.showUpErrorInfo($("#changePasswordForm .J_changePwdOldErr"),$("#changePasswordForm .J_changePwdOld"),"Your password must be at least 6 characters long.");
                }
            });
            $("#changePasswordForm .J_changePwdNew1").bind('blur', function() {
                if($.trim(this.value) == "" || $.trim(this.value).length <6 ){
                    tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew1Err"),$("#changePasswordForm .J_changePwdNew1"),"Your password must be at least 6 characters long.");
                }
            });
            $("#changePasswordForm .J_changePwdNew2").bind('blur', function() {
                var pwd1 = $("#changePwd1").val();
                var pwd2 = $("#changePwd2").val();
                if(pwd2 != ""){
                    if(pwd1 != pwd2){
                        tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew2Err"),$("#changePasswordForm .J_changePwdNew2"),"The passwords for the two fields are different.");
                    }else{
                        $(".J_changePwdNew2").hide();
                        $("#changePasswordForm .J_changePwdNew2Err").removeClass('error');
                    }
                }else{
                    tools.showUpErrorInfo($("#changePasswordForm .J_changePwdNew2Err"),$("#changePasswordForm .J_changePwdNew2"),"Your password must be at least 6 characters long.");
                }
            });
        })();
    }
});







