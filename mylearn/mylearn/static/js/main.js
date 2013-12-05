$(document).ready( function(){
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
		e.stopPropagation();
	});
	$(".leftUp").mousedown(function(e){
		$(this).addClass("press");
	});
	$(".leftUp").mouseup(function(e){
		$(this).removeClass("press");
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
	$('.right').on('mousewheel', function(event) {
	    var top = $(".right .content").css("top");
	    var rightHeight = $(window).height()-$(".content").height();
		top = +top.substr(0,top.length-2);
		var move = event.deltaY*20+top;
		if(move > 0 || rightHeight>0){ move =0; }
		else if(move < rightHeight){move = rightHeight}
		$(".right .content").css("top",move+"px");
		console.log("top:"+top+",   rightHeight:"+rightHeight+",   move:"+move);
	});
});

function back(){
	$(".main").addClass("nonTransform");
	$(".right").addClass("nonTransform");
	$(".left").addClass("nonTransform");

	$(".right").removeClass("transformLeft");
	$(".left").removeClass("transformRight");
	$(".main").removeClass("transformLeft");
	$(".main").removeClass("transformRight");				
}