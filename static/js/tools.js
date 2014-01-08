define(function(require,exports,module){
    var $ = jQuerys = require("libs/jquery-1.7.2");
    var tools = {};

    function AJAXOptions(option)
    {
        this.type = option.type || "post";
        this.url = option.url || "../profile2/";
        this.dataType = option.dataType || "json";
        this.data =  JSON.stringify(option.data) || "";
        this.cache = option.cache || false;
        this.success = option.success || function(){};
        this.error = option.error || function(){alert("操作失败!提交失败");};
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

    function sendAjaxRequest(option,csrftoken)
    {
        var ajaxOptions = new AJAXOptions(option);
        if(csrftoken){
            ajaxOptions.beforeSend = function(xhr){
                xhr.setRequestHeader("X-CSRFToken",csrftoken);
            }
        }
        $.ajax(ajaxOptions);
    }

    tools.sendAjaxRequest = sendAjaxRequest;

    //将表单序列化成JSON格式的数据
    tools.serializeJson = function(obj){
        var serializeObj={};
        $(obj.serializeArray()).each(function(){
            serializeObj[this.name]=this.value;
        });
        return serializeObj;
    }
    
    tools.getToken = function(){
        var option = {};//ajax option
        option.url = "_t";
        option.type = "get";
        sendAjaxRequest(option);
    }

    module.exports = tools;
});



