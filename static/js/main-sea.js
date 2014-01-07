define(function(require,exports,module){
     var $ = jQuery = require('libs/jquery-1.7.2');
     require('libs/jquery.slimscroll')($);

     //初始化首页的默认事件
     initMainPage();
     
//init main page
function initMainPage(){
     $(".leftUp").bind("click",function(e){
          if($(".left").hasClass("transformRight")){
               back();
          }else{
               $(".left").addClass("transformRight");
               $(".main").addClass("transformRight");

               $(".main").removeClass("nonTransform");
               $(".right").removeClass("nonTransform");
               $(".left").removeClass("nonTransform");
          }
          e.stopPropagation();//阻止冒泡
     });
     $(".leftUp").mousedown(function(e){
          $(this).addClass("press");
     });
     $(".leftUp").mouseup(function(e){
          $(this).removeClass("press");
     });
     //open the login box
     $(".rightUp").bind("click",function(e){
          $(".login").fadeIn();
          require("/js/login");
     });
     //close the login box
     $(".black_overlay").bind("click",function(e){
          $(".login").fadeOut();
     });
     $(".rightBottom").bind("click",function(e){
          if($(".right").hasClass("transformLeft")){
               back();
          }else{
               $(".right").addClass("transformLeft");
               $(".main").addClass("transformLeft");

               $(".main").removeClass("nonTransform");
               $(".right").removeClass("nonTransform");
               $(".left").removeClass("nonTransform");
          }
          e.stopPropagation();
     });
     $(".main").bind("click",back);

     //body綁定mousemove事件
     $("body").bind("mousemove",function(){
          $(".leftUp").removeClass("opacity40").addClass("opacity100");
          setTimeout(returnDefault,3000);
     });

     function returnDefault(){
          $(".leftUp").removeClass("opacity100").addClass("opacity40");
     }
     
     //右边滚动
     var rightHeight = $(window).height()-$(".right  .content").height();
     $(".right .rightDown").slimScroll({
             width: '420px',
             height: rightHeight,
             size: '10px',
             position: 'right',
             color: '#000',
             wheelStep: 10
     });
     $(".left .content").slimScroll({
             width: '420px',
             height:  $(window).height(),
             size: '10px',
             position: 'right',
             color: '#000',
             wheelStep: 10
     });
     //left-down nav
     $(".tabBtn").bind("click",function(){
          $(".box").hide();
          $(".basicInfo .contsDetail").hide();
          if($(this).hasClass("learning")){$(".basicInfo #learning").show();$(".learningBox").show();}
          else if($(this).hasClass("teaching")){$(".basicInfo #teaching").show(); $(".teachingBox").show();}
          else if($(this).hasClass("personal")){$(".basicInfo #personal").show(); $(".personalInfoBox").show();}
     });
}
   
//回到主界面
function back(){
     $(".main").addClass("nonTransform");
     $(".right").addClass("nonTransform");
     $(".left").addClass("nonTransform");

     $(".right").removeClass("transformLeft");
     $(".left").removeClass("transformRight");
     $(".main").removeClass("transformLeft");
     $(".main").removeClass("transformRight");                   
} 
});