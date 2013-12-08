function AJAXOptions(data, success, type, url, dataType, cache, error)
{
    this.type = type || "get";
    this.url = url || "../profile2/";
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
