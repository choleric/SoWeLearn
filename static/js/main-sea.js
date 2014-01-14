define(function(require,exports,module){
     var $ = jQuery = require('libs/jquery-1.7.2');
     require('libs/jquery.slimscroll')($);
     require('libs/jquery.cookie')($);
     require('libs/jquery.tipsy')($);

     //初始化首页的默认事件
     initMainPage();
     
     if($.cookie("_l")){//判断是否登录
      $(".leftUp").addClass('J_leftUp');
      $(".leftBottom").addClass('J_leftBottom');
      $(".rightBottom").addClass('J_rightBottom');
      initLeft();
      initRight();
    }else{
      //未登陆时的抖动
      $(".leftUp").bind("click",function(e){
        setTimeout(function(){
          $(".leftUp .tooltip").tipsy("hide");
          $(".left").addClass('transform150');
          $(".main").addClass('transform150');

          $(".main").removeClass("nonTransform");
          $(".right").removeClass("nonTransform");
          $(".left").removeClass("nonTransform");
        },0);
        setTimeout(function(){
          $(".left").addClass('nonTransform');
          $(".main").addClass('nonTransform');
          
          $(".main").removeClass("transform150");
          $(".right").removeClass("transform150");
          $(".left").removeClass("transform150");
          $("#loginHint").removeClass('HIDE').addClass('opacity0');
          $("#loginHint").removeClass('opacity0').addClass('opacity100');
          setTimeout(function(){
            $("#loginHint").removeClass('opacity100').addClass('opacity0');
          },5000);
        },200);
     });
    }

//bind leftUp button event
function initLeft(){
    $(".J_leftUp").bind("click",function(e){
        $(".leftUp .tooltip").tipsy("hide");
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
     $(".J_leftUp").mousedown(function(e){
          $(this).addClass("press");
     });
     $(".J_leftUp").mouseup(function(e){
          $(this).removeClass("press");
     });
     
     //左边栏滚动
     $(".left .content").slimScroll({
             width: '420px',
             height:  $(window).height(),
             size: '10px',
             position: 'right',
             color: '#000',
             wheelStep: 10
     });

     //左边栏的tab切换
     $(".tabBtn").bind("click",function(){
          $(".box").hide();
          $(".basicInfo .contsDetail").hide();
          if($(this).hasClass("learning")){$(".basicInfo #learning").show();$(".learningBox").show();}
          else if($(this).hasClass("teaching")){$(".basicInfo #teaching").show(); $(".teachingBox").show();}
          else if($(this).hasClass("personal")){$(".basicInfo #personal").show(); $(".personalInfoBox").show();}
     });

}

//bind rightnBottom button event
function initRight(){
     $(".J_rightBottom").bind("click",function(e){
          $(".rightBottom .tooltip").tipsy("hide");
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
}

//init main page
function initMainPage(){
      
     //open the login box
     $(".rightUp").bind("click",function(e){
          $(".login").fadeIn();
          $("#overlay_black").fadeIn();
          require("/js/userinfo");
     });
     //close the login box
     $("#overlay_black").bind("click",function(e){
          $(".login").fadeOut();
          $(".signup").fadeOut();
          $(this).fadeOut();
     });
     $(".main").bind("click",back);

     //body綁定mousemove事件
     $("body").bind("mousemove",function(){
          $(".leftUp").removeClass("opacity40").addClass("opacity100");
          setTimeout(returnDefaultMain,3000);
     });

     function returnDefaultMain(){
          $(".leftUp").removeClass("opacity100").addClass("opacity40");
     }
     $(".leftUp .tooltip").tipsy({
        gravity:'nw',
        delayIn:'500',
        delayOut:'0',
        trigger:'hover',
        opacity:'0.8',
        fade:true
     });

     $(".rightUp .tooltip").tipsy({
        gravity:'ne',
        delayIn:'500',
        delayOut:'0',
        trigger:'hover',
        opacity:'0.8',
        fade:true
     });

     $(".rightBottom .tooltip").tipsy({
        gravity:'se',
        delayIn:'500',
        delayOut:'0',
        trigger:'hover',
        opacity:'0.8',
        fade:true
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