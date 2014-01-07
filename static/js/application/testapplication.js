define(function(require,exports,module){
    
     var util = require("../testutil");

     var $ = jQuery = require("libs/jquery-1.7.2");
     console.log($("#hello-seajs").html("abcd"));
     console.log($);
     require('libs/jquery.cookie')($);
     $.cookie("_t");
     console.log($.cookie('_t'));
   
     var helloSeaJS = document.getElementById('hello-seajs');
     helloSeaJS.style.color = util.randomColor();
     window.setInterval(function(){
          helloSeaJS.style.color = util.randomColor();
     },1500);
});