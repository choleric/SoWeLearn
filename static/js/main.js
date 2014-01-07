$(document).ready( function(){
	init();
	// getData();
	leftInit();
});

//获取首屏信息
function getData(){
	sendAjaxRequest({},"",displayUserProfile);
	sendAjaxRequest({},"/userTopicourses/",displayTopicourses);
	sendAjaxRequest({},"/userTopiquestions/",displayTopiquestions);
	sendAjaxRequest({},"/getUserAppointment/",displayUserAppointment);
	sendAjaxRequest({},"/getUserRequest/",displayUserRequest);
}

//init 
function init(){
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
		setTimeout(returnDefaultOpacity,3000);
	});

	function returnDefaultOpacity(){
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

	//login
	$(".loginBtn").bind("click",login);
}

function leftInit(){
	//verified  and  unverified 
	$(".switch").bind("click",function(){
		if($(this).hasClass("switch-on")){
			$(this).removeClass("switch-on").addClass("switch-off");
			$(this).children("span").first().html("unverified");
		}else if($(this).hasClass("switch-off")){
			$(this).removeClass("switch-off").addClass("switch-on");
			$(this).children("span").first().html("verified");
		}
	});
}
//display user profile
function displayUserProfile(data){
	var uec = data.personalProfile.userEducationCredential;
	    var uecCode = "";
	    for(var i = 0, elength = uec.length; i < elength; i++){
	        uecCode += "<li>";
	        uecCode += uec[i].userEducationInfo;
	        if(uec[i].IsVerified){
	            uecCode += "[Verified]</li>";
	        }else{
	            uecCode += "[Unverified]</li>";
	        }
	    }
	    uec = data.personalProfile.userWorkCredential;
	    for(var i = 0, elength = uec.length; i < elength; i++){
	        uecCode += "<li>";
	        uecCode += uec[i].userWorkInfo;
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
//加载显示TOpicourses信息
function displayTopicourses(data){
	
	var tcHtml = "";
	var utcl = data.userTopicoursesList;
	for(var i = 0,l = utcl.length; i < l; i++){
		tcHtml += "<li>topiquestionTitle:"+utcl[i].topicourseTitle+"</li>";
	}
	$("#teaching #topicourses").html(tcHtml);
}
//显示topiquestions的数据
function displayTopiquestions(data){

	var tqHtml = "";
	var uttl = data.userTopiquestionsList;
	for(var i = 0,l = uttl.length; i < l; i++){
		tqHtml += "<li>topiquestionTitle:"+uttl[i].topiquestionTitle+"</li>";
	}
	$("#teaching #topicquestions").html(tqHtml);
}
//
function displayUserAppointment(data){
	var ualHtml = "";
	var ual = data.UserAppointmentsList;
	for(var i = 0, l = ual.length; i < l; i++){
		ualHtml += "<div style='border:1px solid;'><ul>";
		ualHtml += "<li>serAppointmentCost:"+ual[i].userAppointmentCost+"</li>";
		ualHtml += "<li>userAppointmentDate:"+ual[i].userAppointmentDate+"</li>";
		ualHtml += "<li>userAppointmentStartTime:"+ual[i].userAppointmentStartTime+"</li>";
		ualHtml += "<li>userAppointmentTitle:"+ual[i].userAppointmentTitle+"</li>";
		ualHtml += "<li>userAppointmentTutorMessage:"+ual[i].userAppointmentTutorMessage+"</li>";
		ualHtml += "</ul></div>";
	}
	$("#right .rightDown .appointmentSchedule").html(ualHtml);
}
//
function displayUserRequest(data){
	var urdpHtml = "";
	var urdp = data.userRequestsList;
	for(var i = 0, l = urdp.length; i < l; i++){
		urdpHtml += "<li><div style='border:1px solid; width:400px; height:260px;'>";
		urdpHtml += "<p>userRequestDatePreference:"+urdp[i].userRequestDatePreference+"</p>";
		urdpHtml += "<p>userRequestOther:"+urdp[i].userRequestOther+"</p>";
		urdpHtml += "<p>userRequestStudentName:"+urdp[i].serRequestStudentName+"</p>";
		urdpHtml += "<p>userRequestTimePreference:"+urdp[i].userRequestTimePreference+"</p>";
		urdpHtml += "<p>userRequestTimeZone:"+urdp[i].userRequestTimeZone+"</p>";
		urdpHtml += "<p>userRequestTuitionLearningGoal:"+urdp[i].userRequestTuitionLearningGoal+"</p>";
		urdpHtml += "<p>userRequestTuitionLevel:"+urdp[i].userRequestTuitionLevel+"</p>";
		urdpHtml += "<p>userRequestTuitionSubject:"+urdp[i].userRequestTuitionSubject+"</p>";
		urdpHtml += "<p>userRequestTutorName:"+urdp[i].userRequestTutorName+"</p>";
		urdpHtml += "</li>";
	}
	$("#right .requestInbox #requestInbox-slider").html(urdpHtml);
	
	//右上轮播，一定要放在获取数据之后
	$('#requestInbox-slider').bxSlider();
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

function login(){
	var accounts = $("#loginForm").serializeJson();
	accounts._t = $.cookie("_t");
	accounts.csrftoken = $.cookie("csrftoken");
	accounts.remember = "False";
	sendAjaxRequest(accounts,"/accounts/login/",function(){},$.cookie("csrftoken"));
}


