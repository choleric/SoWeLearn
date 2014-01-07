define(function(require,exports,module){
    var $ = require("libs/jquery-1.7.2");

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

    module.sendAjaxRequest = function (option,csrftoken)
    {
        var ajaxOptions = new AJAXOptions(option);
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

});



