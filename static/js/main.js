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
	var rightHeight = $(window).height()-$(".right  .content").height();
	$(".right .rightDown").slimScroll({
	        width: '420px',
	        height: rightHeight,
	        size: '10px',
	        position: 'right',
	        color: '#000',
	        wheelStep: 10
	});
	//右上轮播
	$('#requestInbox-slider').bxSlider();
	//left-down nav
	$(".tabBtn").bind("click",function(){
		$(".leftDown .contsDetail").hide();
		if($(this).hasClass("learning")){$(".leftDown #learning").show();}
		else if($(this).hasClass("teaching")){$(".leftDown #teaching").show();}
		else if($(this).hasClass("personal")){$(".leftDown #personal").show();}
	});
	var getUserProfile = new AJAXOptions();
	getUserProfile.setSuccess(displayUserProfile);
	$.ajax(getUserProfile);
	var  getTopicourses = new AJAXOptions();
	getTopicourses.url =  "/topicourses/";
	getTopicourses.setSuccess(displayTopicourses);
	$.ajax(getTopicourses);

});

function displayUserProfile(data){
	var uec = data.personalProfile.userEducationCredential;
	    var uecCode = "";
	    for(var i = 0, elength = uec.length; i < elength; i++){
	        uecCode += "<li>";
	        uecCode += uec[i].educationInfo;
	        if(uec[i].IsVerified){
	            uecCode += "[Verified]</li>";
	        }else{
	            uecCode += "[Unverified]</li>";
	        }
	    }
	    uec = data.personalProfile.userWorkCredential;
	    for(var i = 0, elength = uec.length; i < elength; i++){
	        uecCode += "<li>";
	        uecCode += uec[i].workInfo;
	        if(uec[i].IsVerified){
	            uecCode += "[Verified]</li>";
	        }else{
	            uecCode += "[Unverified]</li>";
	        }
	    }
	    $("#aboutUserQuote").val(data.personalProfile.aboutUserQuote);
	    $("#userEducationCredential").html(uecCode);
	    $("#location").html(data.userLocation);
	    $("#tutorTuitionTopics").html(data.tutorTuitionTopics);
}
function displayTopicourses(data){
	var tcHTML = "<ul>";
	for(var i = 0,l = data.length; i < l; i++){
		tcHTML += "<li>userTopicoursesTimestamp:"+data[i].userTopicoursesTimestamp+"</li>"
		tcHTML += "<li>userTopicourseCreatorUserID:"+data[i].userTopicourseCreatorUserID+"</li>"
		tcHTML += "<li>topicourseTitle:"+data[i].topicourseTitle+"</li>"
		tcHTML += "<li>topicoursePath:"+data[i].topicoursePath+"</li>"
		var topicQuiz = data[i].userTopicquizList;
		for(var j  = 0, jl = topicQuiz.length; j < jl ; j++){
			tcHTML += "<li>userTopicquizTimestamp:"+topicQuiz[j].userTopicquizTimestamp+"</li>";
			tcHTML += "<li>userTopicquizResult:"+topicQuiz[j].userTopicquizResult+"</li>";
			tcHTML += "<li>userTopicquizList:"+topicQuiz[j].userTopicquizList+"</li>";
		}
	}
	tcHTML += "</ul>";
	$("#teaching p").html(tcHTML);
}
function back(){
	$(".main").addClass("nonTransform");
	$(".right").addClass("nonTransform");
	$(".left").addClass("nonTransform");

	$(".right").removeClass("transformLeft");
	$(".left").removeClass("transformRight");
	$(".main").removeClass("transformLeft");
	$(".main").removeClass("transformRight");				
}