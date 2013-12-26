function AJAXOptions(data, success, type, url, dataType, cache, error)
{
    this.type = type || "get";
    this.url = url || "";
    this.dataType = dataType || "json";
    this.cache = cache || false;
    this.success = success || function(){};
    this.error = error || function(){alert("操作失败!求提交失");};
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
    this.data = {"dictData" : JSON.stringify(inputJSONObject)};
}

function sendAjaxRequest(inputJsonData, url, successCallback)
{
    var ajaxOptions = new AJAXOptions();
    ajaxOptions.url = url || "../profile2/";
    ajaxOptions.setData(inputJsonData);
    ajaxOptions.setSuccess(successCallback);
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