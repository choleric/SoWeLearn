function AJAXOptions(data, success, type, url, dataType, cache, error)
{
    this.type = type || "get";
    this.url = url || "";
    this.dataType = dataType || "json";
    this.cache = cache || false;
    this.success = success || function(){};
    this.error = error || function(){alert("操作失败!提交失败");};
}

AJAXOptions.prototype.setSuccess = function(sucCallback)
{
    this.success = function(data, textStatus){
        if(!data)
            return;
        else{
            sucCallback(data);
        }
    };
}

AJAXOptions.prototype.setData = function(inputJSONObject)
{
    this.data =  JSON.stringify(inputJSONObject);
}

function sendAjaxRequest(inputJsonData, url, successCallback,csrftoken)
{
    var ajaxOptions = new AJAXOptions();
    ajaxOptions.url = url || "../profile2/";
    ajaxOptions.setData(inputJsonData);
    ajaxOptions.setSuccess(successCallback);
    ajaxOptions.beforeSend = function(xhr,csrftoken){
        xhr.setRequestHeader("X-CSRFToken",csrftoken);
    }
    $.ajax(ajaxOptions);
}

//将表单序列化成JSON格式的数据
(function($){
    $.fn.serializeJson=function(){
        var serializeObj={};
        $(this.serializeArray()).each(function(){
            serializeObj[this.name]=this.value;
        });
        return serializeObj;
    };
})(jQuery);

/**
 * 验证是否为正确的邮箱格式
 * return 
 *    true or false
 */
function isEmail(email){
    var re_email = new RegExp("^([a-zA-Z0-9]+[_|\_|.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|.]?)*[a-zA-Z0-9]+.[a-zA-Z]{2,3}$");
    if(re_email.test(email)){
        return true; 
    }else{
        return false;
    }
}
