        $('.fa-chevron-circle-left').tooltip({animation:false, container: 'body', html:true});
        $('.fa-chevron-circle-right').tooltip({animation:false, container: 'body', html:true});
	var disqusLoad = false;
        $('#myTab a[href="#reviews"]').click(function(e) {
          if (!disqusLoad)
            {
              e.preventDefault();
              $.ajaxSetup({cache: true});
              $.getScript("https://gonaturalistic.disqus.com/embed.js");
              $.ajaxSetup({cache: false});
              disqusLoad = true;
            }
        });
	//Stripe Configuration//////////
	var stripe_pub_key = '{{stripePubKey}}'; 
	var handler = StripeCheckout.configure({
          key: stripe_pub_key,
	  allowRememberMe: false,
	  shippingAddress: false,
	  billingAddress: true,
	  name: 'GoNaturalistic',
	  email: '{{user.username}}',
          token: function(token, args) {
	    $("#modalTitleId").text("Processing...");
	    $("#modalBodyDetails").hide();
	    $("#modalBodyLoader").show();
            $.post("",{stripeToken:token.id,date:date,time:time,promoCode:promoCode,duration:duration,method:method}, "json").done(function(data) {
	      if(data.payment == "ok"){
	        $("#modalBodyLoader").fadeOut("fast", function(){
		  $("#modalTitleId").text("Confirmed");
		  $("#doneButton").hide();
                  $("#modalFooterBackButton").hide();
		  $("#modalChargeSuccess").fadeIn("slow");
		});
	      }else if(data.payment == "fail"){
                $("#modalBodyLoader").fadeOut("fast", function(){
                  $("#modalTitleId").text("Declined");
                  $("#doneButton").hide();
                  $("#modalChargeFail").fadeIn("slow");
		  step = 7;
                });
	      }else if(data.payment == "wrong"){
                $("#modalBodyLoader").fadeOut("fast", function(){
                  $("#modalTitleId").text("Oops!");
                  $("#doneButton").hide();
                  $("#modalChargeWrong").fadeIn("slow");
                  step = 8;
                });
              }else if(data.payment == "gone"){
                $("#modalBodyLoader").fadeOut("fast", function(){
                  $("#modalTitleId").text("Please select another appointment");
                  $("#doneButton").hide();
                  $("#modalNotAvailable").fadeIn("slow");
                  step = 9;
                });
              }
            }).fail(function() {
              jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
              setTimeout(function() {
                location.reload();
              }, 3000);
            });	  
	  }
        });
	////////////////////////////////
	//Get Appointment/////////////////////
	$.ajaxSetup({cache: false});
	var step = 0;
	var methodName = new Object();
	var durationName = {"h":"60 Minutes","hh":"30 Minutes","qh":"15 Minutes"}	
	methodName["s"] = "Skype";
	methodName["ft"] = "FaceTime";
	methodName["ph"] = "Phone Call";
        methodName["o"] = "Face to Face";
	var methodPage = "Please select consultation method";
	var durationPage = "Please select consultation duration";
	var datePage = "Please select a date";
	var timePage = "Please select a time";
	var detailsPage = "Please verify appointment details";
	var checkoutPage = "Checkout";
	var notAvailablePage = "Sorry";
	var method = null;
	var duration = null;
	var promoCode = null;
	var timeZone = null;
	var date = null;
	var time = null;
	var methodAndDurationData = null;
	var currentDay = null;
	var thisMonthName = null;
	var thisMonthData = null;
	var nextMonthName = null;
	var nextMonthData = null; 
	var practitionerTimeZone = null;
	//Select Method - Step 1//////////////////
	function selectMethod(data){
	    $("#modalFooterBackButton").addClass("disabled");
	    $("#modalTitleId").text(methodPage);
	    if(data.length == 0){
	      $("#modalBodyMethod").append('<div class="alert alert-danger">Sorry, there are no <strong>consultation methods</strong> available at this time.</div>');
	    }
	    methodStatus = false;
	    $.each(data, function(key, val) {
	      if(val.method_status == "y"){
		methodStatus = true;
		if(val.method_name == "s"){
	          $("#modalBodyMethod .container").append('<button type="button" class="btn btn-info btn-block" id="'+val.method_name+'Button"><i class="fa fa-fw fa-skype"></i><strong>'+methodName[val.method_name]+'</strong></button>');
		}else if(val.method_name == "ph"){
		  $("#modalBodyMethod .container").append('<button type="button" class="btn btn-info btn-block" id="'+val.method_name+'Button"><i class="fa fa-fw fa-phone"></i><strong>'+methodName[val.method_name]+'</strong></button>');
		}else if(val.method_name == "ft"){ 
		  $("#modalBodyMethod .container").append('<button type="button" class="btn btn-info btn-block" id="'+val.method_name+'Button"><i class="fa fa-fw fa-apple"></i><strong>'+methodName[val.method_name]+'</strong></button>');
                }else if(val.method_name == "o"){
                  $("#modalBodyMethod .container").append('<button type="button" class="btn btn-info btn-block" id="'+val.method_name+'Button"><i class="fa fa-fw fa-hospital-o"></i><strong>'+methodName[val.method_name]+'</strong></button>');
                }
	      }
	    });
            if(!methodStatus){
              $("#modalBodyMethod").append('<div class="alert alert-danger">Sorry, there are no <strong>consultation methods</strong> available at this time.</div>');
            }	    
	    $("#sButton").click(function(){
	      method="s";
	      selectDuration(data);
	    });
            $("#ftButton").click(function(){
	      method="ft";
	      selectDuration(data);
            });
            $("#phButton").click(function(){
	      method="ph";
	      selectDuration(data);
            });
            $("#oButton").click(function(){
              method="o";
              selectDuration(data);
            });
	    $("#modalBodyLoader").fadeOut("fast",function(){
	      $("#modalBodyMethod").fadeIn("slow");
	      step = 1;
	    });
	}
	///////////////////////////////////////
	//Select Duration - Step 2//////////////
	function selectDuration(data){
	  $("#modalBodyDuration .container").html("");
	  $("#modalFooterBackButton").removeClass("disabled");
	  $("#modalTitleId").text(durationPage);
	  $.each(data, function(key, val) {
	    if(val.method_name == method){
	      if(val.method_hour == "y"){	
	        $("#modalBodyDuration .container").append('<button type="button" class="btn btn-info btn-block" id="hourButton"><strong>60 Minutes</strong></button>'); 
	      } 
              if(val.method_half_hour == "y"){
                $("#modalBodyDuration .container").append('<button type="button" class="btn btn-info btn-block" id="halfHourButton"><strong>30 Minutes</strong></button>');
              }
              if(val.method_quarter_hour == "y"){
                $("#modalBodyDuration .container").append('<button type="button" class="btn btn-info btn-block" id="quarterHourButton"><strong>15 Minutes</strong></button>');
              }
	    }
	  });	  
	  $("#hourButton").click(function(){
              duration="h";
	      selectDate();
	  });
          $("#halfHourButton").click(function(){
              duration="hh";
	      selectDate();
          });
          $("#quarterHourButton").click(function(){
              duration="qh";
	      selectDate();
          });
	  $("#modalBodyMethod").fadeOut("fast",function(){
            $("#modalBodyDuration").fadeIn("slow");
	    step = 2;
          });
	}
	///////////////////////////////////////////////////
	//Create Calendar Func////////////////////////////
	function is_day_available(monthYear,day,dayData){
	  intDay = parseInt(day);
	  if(intDay < 10 ){
	   fullDate = monthYear+"-0"+day;
	  }else{
           fullDate = monthYear+"-"+day;
	  }
	  dayResult = false;
	  $.each(dayData, function(key, val){
            timeResult = false;
	    if(key == fullDate){
	      if(val.length > 0){
	        $.each(val, function(key1, val1){
		  if(val1.status == "available"){
		    timeResult = true;
		    return false;	
		  }
		}); 
	      }
	      if(timeResult){
		dayResult = true;
	        return false;
	      }  
	    }
	  });
	  return dayResult;
	}
	//////////////////////////////////////////////////
	//Select Date - Step 3////////////////////////////
	function selectDate(){
          $("#modalTitleId").text(datePage);
          $("#modalFooterBackButton").addClass("disabled");
          key = "dateTime";
          $.get("",{key:key, duration:duration}, "json").done(function(data) {
            $("#modalBodyDate table").html("");
            $("#modalBodyDate #monthNav").html("");
	    console.log(data);$("#modalBodyLoader").hide();
	    //Create Calendar with current month and next month////////
	    userCurrentDay = data[0].userCurrentDay;
	    firstMonthName = data[0].firstMonthName;
            firstYearMonth = data[0].firstYearMonth;
	    firstMonthData = data[0].firstMonthData;
            nextMonthName = data[0].nextMonthName;
            nextYearMonth = data[0].nextYearMonth;
            nextMonthData = data[0].nextMonthData;
            userSelectedYearMonth = firstYearMonth;
	    practitionerTimeZone = data[0].practitionerTimeZone
		  navHTML = '<ul id="currentMonthUl" class="pagination pagination-sm" style="margin:0px;">';	    
		  navHTML += "<li class='disabled'>";
		  navHTML += "<a href='#'><strong><i class='fa fa-1x fa-caret-left'></i></strong></a></li>";
		  navHTML += "<li class='active'><a href='#'><strong>"+firstMonthName+"</strong></a></li>";
                  navHTML += "<li>";
                  navHTML += "<a href='#' id='nextMonth'><strong><i class='fa fa-1x fa-caret-right'></i></strong></a></li>";
		  navHTML += '</ul>';
		  $("#modalBodyDate #monthNav").append(navHTML);
                  navHTML = '<ul id="nextMonthUl" class="pagination pagination-sm" style="margin:0px;display:none;">';
                  navHTML += "<li>";
                  navHTML += "<a href='#' id='currentMonth'><strong><i class='fa fa-1x fa-caret-left'></i></strong></a></li>";
                  navHTML += "<li class='active'><a href='#'><strong>"+nextMonthName+"</strong></a></li>";
                  navHTML += "<li class='disabled'>";
                  navHTML += "<a href='#'><strong><i class='fa fa-1x fa-caret-right'></i></strong></a></li>";
                  navHTML += "</ul>";
		  tableHTML = '<thead><tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>';
		  tableHTML += '<tbody id="currentMonthTBody">';
		  for(i=0;i<firstMonthData.length;i++){
		    tableHTML +='<tr>';
		    for(w=0;w<7;w++){
		      tdVal = firstMonthData[i][w];
		      if(tdVal == "0"){	
                        tableHTML +='<td class="active"></td>';
		      }else{
			if(is_day_available(firstYearMonth,tdVal,data[1])){
			  if(tdVal == userCurrentDay){
                            tableHTML +='<td class="success text-center"><a href="#" class="text-success" style="display:block;"><strong><span class="badge" style="font-size:10px; background-color:#5cb85c;">'+tdVal+'</span></strong></a></td>';
			  }else{
                            tableHTML +='<td class="success text-center"><a href="#" class="text-success" style="display:block;"><strong>'+tdVal+'</strong></a></td>';
			  }
			}else{
                          if(tdVal == userCurrentDay){
                            tableHTML +='<td class="danger text-center"><strong><span class="badge" style="font-size:10px; background-color:#d9534f;">'+tdVal+'</span></strong></td>';
                          }else{
                            tableHTML +='<td class="danger text-center"><strong>'+tdVal+'</strong></td>';
                          }
			}
		      }
		    }
                    tableHTML +='</tr>';
		  }
                  tableHTML += '</tbody>';
                  tableHTML += '<tbody id="nextMonthTBody" style="display:none;">';
                  for(i=0;i<nextMonthData.length;i++){
                    tableHTML +='<tr>';
                    for(w=0;w<7;w++){
                      tdVal = nextMonthData[i][w];
                      if(tdVal == "0"){ 
                        tableHTML +='<td class="active"></td>';
                      }else{
                        if(is_day_available(nextYearMonth,tdVal,data[1])){
                            tableHTML +='<td class="success text-center"><a href="#" class="text-success" style="display:block;"><strong>'+tdVal+'</strong></a></td>';
                        }else{
                            tableHTML +='<td class="danger text-center"><strong>'+tdVal+'</strong></td>';
                        }
                      }
                    }
                    tableHTML +='</tr>';
                  }
                  tableHTML += '</tbody>';
		  $("#modalBodyDate table").append(tableHTML);
          	  splitedTimeZone = practitionerTimeZone.split("/",2)[1]
          	  if(splitedTimeZone == "Paris"){
            	    $("#modalBodyDate table").append('<tfoot><tr><td colspan="7" class="active"><strong>*Current date shown in Central European Time Zone.</strong></td></tr></tfoot>');
          	  }
          	  else if(splitedTimeZone == "Istanbul"){
            	    $("#modalBodyDate table").append('<tfoot><tr><td colspan="7" class="active"><strong>*Current date shown in Eastern European Time Zone.</strong></td></tr></tfoot>');
          	  }
          	  else if(splitedTimeZone == "London"){
            	    $("#modalBodyDate table").append('<tfoot><tr><td colspan="7" class="active"><strong>*Current date shown in Greenwich Mean Time Zone.</strong></td></tr></tfoot>');
          	  }
          	  else{
            	    $("#modalBodyDate table").append('<tfoot><tr><td colspan="7" class="active"><strong>*Current date shown in '+splitedTimeZone+' Time Zone.</strong></td></tr></tfoot>');
          	  }
                  $("#modalBodyDate #monthNav").append(navHTML);
		  $("#nextMonth").click(function(event){
		    event.preventDefault();
		    $("#currentMonthUl").hide();
		    $("#nextMonthUl").show();
		    $("#currentMonthTBody").hide();
		    $("#nextMonthTBody").show();
		    userSelectedYearMonth = nextYearMonth;
		  });
                  $("#currentMonth").click(function(){
		    event.preventDefault();
                    $("#nextMonthUl").hide();
                    $("#currentMonthUl").show();
                    $("#nextMonthTBody").hide();
                    $("#currentMonthTBody").show();
		    userSelectedYearMonth = firstYearMonth;
                  });
	    //////////////////////////////
	    $("#modalBodyDate").fadeIn("slow");
	    $("#modalFooterBackButton").removeClass("disabled");
            $("#modalBodyDate table tbody td.success").click(function(e){
	      e.preventDefault();
              selectTime(userSelectedYearMonth,$(this).index(),$(this).text(),data[1]);
	      date = userSelectedYearMonth+"-"+$(this).text();
            });
          }).fail(function() {
            jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
            setTimeout(function() {
              location.reload();
            }, 3000);
          });
          $("#modalBodyDuration").fadeOut("fast",function(){
            $("#modalBodyLoader").show();
            step = 3;
          });
	}
	///////////////////////////////////////////////////
	function convertFullDate(selectedYearMonth,day,dayName){
	  dayArray = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
	  monthArray = ["January","February","March","April","May","June","July","August","September","October","November","December"];
	  monthName = selectedYearMonth.split("-",2);
	  return dayArray[(dayName)]+" "+monthArray[(parseInt(monthName[1]) - 1)]+" "+day
	}
	//Step 4 - Select Time/////////////////////////////
	function selectTime(selectedYearMonth,dayName, day,monthData){
	  $("#modalBodyTime table").html("");
          $("#modalTitleId").text(timePage);
	  intDay = parseInt(day);
	  if(intDay < 10 ){
	    fullSelectedDate = selectedYearMonth+"-0"+day;
	  }else{
            fullSelectedDate = selectedYearMonth+"-"+day;
	  }
	  convertedFullName = convertFullDate(selectedYearMonth, day, dayName);
	  $("#modalBodyTime table").append('<thead><tr><th class="active text-center" style="font-size:12px;">Available Times on '+convertedFullName+'</th></tr></thead>');

	  tbodyHtml = '<tbody>';
	  $.each(monthData, function(key, val){
	    if(key == fullSelectedDate){
	      $.each(val, function(key1, val1){
		if(val1.status == "available"){
                  tbodyHtml += '<tr><td class="success text-center" id="'+val1.start_time+'" style="font-size:11px;"><a href="#" class="text-success" style="display:block"><strong>'+val1.period+'</strong></a></td></tr>';
	        }
	      });
	      return false;
	    }
	  });
          tbodyHtml += '</tbody>';
	  $("#modalBodyTime table").append(tbodyHtml);
	  splitedTimeZone = practitionerTimeZone.split("/",2)[1]
	  if(splitedTimeZone == "Paris"){
	    $("#modalBodyTime table").append('<tfoot><tr><td class="active"><strong>*Times shown in Central European Time Zone.</strong></td></tr></tfoot>');
	  }
          else if(splitedTimeZone == "Istanbul"){
            $("#modalBodyTime table").append('<tfoot><tr><td class="active"><strong>*Times shown in Eastern European Time Zone.</strong></td></tr></tfoot>');
          }
          else if(splitedTimeZone == "London"){
            $("#modalBodyTime table").append('<tfoot><tr><td class="active"><strong>*Times shown in Greenwich Mean Time Zone.</strong></td></tr></tfoot>');
          }
	  else{
            $("#modalBodyTime table").append('<tfoot><tr><td class="active"><strong>*Times shown in '+splitedTimeZone+' Time Zone.</strong></td></tr></tfoot>');
	  }
	  $("#modalBodyTime table tbody td.success").click(function(e){
	    e.preventDefault();
	    showConsultationDetails(convertedFullName,$(this).attr("id"),$(this).text());
	    time = $(this).text();
	  });
	  $("#modalBodyDate").fadeOut("fast", function(){
	    $("#modalBodyTime").fadeIn("slow");
	    step = 4;
	  });	  
	}
	//Show Consultation Details to Complete////////////
	function showConsultationDetails(convertedDate,startTime,convertedTime){
	  $("#modalTitleId").text(detailsPage);
	  $("#modalBodyDetails table").html("");
	  $("#modalBodyDetails table").append('<thead><tr><th colspan="2" class="active text-center" style="font-size:14px;"><strong>Appointment Details</strong></th></tr></thead>');
	  $("#modalBodyDetails table").append('<tbody></tbody>');
          $("#modalBodyDetails table tbody").append('<tr><td style="font-size:12px;"><strong>Method:</strong></td><td class="success" style="font-size:13px;"><strong>'+methodName[method]+'</strong></td></tr>');
          $("#modalBodyDetails table tbody").append('<tr><td style="font-size:12px;"><strong>Duration:</strong></td><td class="success" style="font-size:13px;"><strong>'+durationName[duration]+'</strong></td></tr>');
          $("#modalBodyDetails table tbody").append('<tr><td style="font-size:12px;"><strong>Date:</strong></td><td class="success" style="font-size:13px;"><strong>'+convertedDate+'</strong></td></tr>');
          $("#modalBodyDetails table tbody").append('<tr><td style="font-size:12px;"><strong>Time:</strong></td><td class="success" style="font-size:13px;"><strong>'+convertedTime+'</strong></td></tr>');
          consultationPriceLoader = '<i class="fa fa-lg fa-spinner fa-spin fa-fw text-danger"></i>';
	  $("#modalBodyDetails table tbody").append('<tr><td style="font-size:12px;"><strong>Price:</strong></td><td class="success text-danger" id="consultationPriceContent" style="margin-bottom:0px;font-size:13px;">'+consultationPriceLoader+'</td></tr>');
	  $("#modalBodyDetails table").append('<tfoot><tr><td colspan="2" class="warning"><strong>*Detailed Consultation Method Information will be sent to your email address after purchase.</strong></td></tr></tfoot>');
          //Get Price//////////
	  redeemPromoInputHtml = '<div class="input-group" style="display:none"><input id="redeemInput" type="text" class="form-control input-sm"><span class="input-group-btn"><button id="promoCodeApplyButton" class="btn btn-default btn-sm" type="button"><strong>Apply</strong></button><button id="closeRedeemInput" class="btn btn-default btn-sm" type="button">&times;</button></span></div>';
	  redeemPromoHtml = '<a href="#" id="redeemPromoButton"  style="font-size:12px;"><strong>Redeem promo code</strong></a>';
          key = "getPrice";
	  $("#doneButton").addClass("disabled");
          $.get("",{key:key,duration:duration,method:method}, "json").done(function(data) {
	    doneAppointment();
            $("#consultationPriceContent").html('<div style="width:160px;"><p id="priceText" style="margin-bottom:0px;"><strong>$'+data.price+'</strong></p><div id="redeemPromoInput" style="width:160px;">'+redeemPromoHtml+redeemPromoInputHtml+'</div><div id="invalidPromoCode" style="display:none;margin-top:2px;"><i class="fa fa-warning fa-fw"></i><strong>Invalid Promo Code</strong></div></div>');
	    $("#redeemPromoButton").click(function(event){
	      $("#redeemPromoInput div.input-group").fadeIn("fast");
	      $("#redeemPromoButton").hide();	      
	      $("#redeemInput").focus();
	      event.preventDefault();
	    });
            $("#closeRedeemInput").click(function(){
	      $("#redeemPromoButton").show();
	      $("#redeemPromoInput div.input-group").hide();
	      $("#invalidPromoCode").hide();
            });
	    $("#promoCodeApplyButton").click(function(){
	      key = "validatePromoCode";
	      enteredPromoCode = $("#redeemInput").val();
	      applyButtonHTML = $("#promoCodeApplyButton").html();
	      $("#redeemInput").addClass("disabled");
	      $("#promoCodeApplyButton").addClass("disabled");
	      loaderHTML = '<i class="fa fa-lg fa-spinner fa-spin fa-fw"></i>';
	      $("#promoCodeApplyButton").html(loaderHTML);
	      $("#doneButton").addClass("disabled");
	      $.get("",{key:key,promoCode:enteredPromoCode,method:method,duration:duration}, "json").done(function(data) {
	        if(data.status == "valid"){
		  $("#priceText").html("<strong>$"+data.price+"&nbsp;&nbsp;<span class='text-muted' style='font-size:12px;'>( "+data.percent+"% Discount )</span></strong>");
		  $("#redeemPromoButton").show();
                  $("#redeemPromoInput div.input-group").hide();
		  $("#invalidPromoCode").hide();
		  promoCode = data.promoCode;
		}else{
		  $("#invalidPromoCode").show(); 
		}
		doneAppointment();
		$("#promoCodeApplyButton").html(applyButtonHTML);
                $("#redeemInput").removeClass("disabled");
                $("#promoCodeApplyButton").removeClass("disabled");
	      }).fail(function() {
                jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
                setTimeout(function() {
                  location.reload();
                }, 3000);
              });
	    });
         }).fail(function() {
            jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
            setTimeout(function() {
              location.reload();
            }, 3000);
          });
          ///////////////////// 
         $("#modalBodyTime").fadeOut("fast", function(){
            $("#modalBodyDetails").fadeIn("slow");
            step = 5;
          });
	}
	var stripePrice = "";
	var stripeDescription = "";
	//Get Stripe Form//////////////////////////
	function doneAppointment(){
          key = "getStripe";
          $.get("",{key:key,date:date,time:time,promoCode:promoCode,duration:duration,method:method}, "json").done(function(data) {
	    stripePrice = parseFloat(data.price)*100;
	    stripeDescription = data.description;
	    $("#doneButton").removeClass("disabled");
	  }).fail(function() {
            jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
            setTimeout(function() {
              location.reload();
            }, 3000);
          });
	}
	$("#doneButton").click(function(event){
          handler.open({
            description: stripeDescription,
            amount: stripePrice
          });
	});
	///////////////////////////////////////////////////
	$("#appointmentButton").click(function(){
	  if( step == 0 ){
	    step = 1;
	    key = "methodDuration";
	    $.get("",{key:key}, "json").done(function(data) {
	      selectMethod(data);
            }).fail(function() {
              jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
              setTimeout(function() {
                location.reload();
              }, 3000);
            });
	  }
	});
	///////////////////////////////////////////////
	//Natigation - Back////////////////////////////
	$("#modalFooterBackButton").click(function(){
	  if(step == 2){
	    $("#modalBodyDuration").fadeOut("fast",function(){
	      $("#modalFooterBackButton").addClass("disabled");
              $("#modalBodyMethod").fadeIn("slow");
	      $("#modalTitleId").text(methodPage);
	      step = 1;
            });
	  }else if(step == 3){
            $("#modalBodyDate").fadeOut("fast",function(){
              $("#modalBodyDuration").fadeIn("slow");
              $("#modalTitleId").text(durationPage);
              step = 2;
            });	
	  }else if(step == 4){
	    $("#modalBodyTime").fadeOut("fast",function(){
	      $("#modalBodyDate").fadeIn("slow");
              $("#modalTitleId").text(datePage);
	      step = 3;
	    });
	  }else if(step == 5){
            $("#modalBodyDetails").fadeOut("fast",function(){
              $("#modalBodyTime").fadeIn("slow");
	      promoCode = null;
              $("#modalTitleId").text(timePage);
	      $("#modalFooterDoneButton").addClass("disabled");
              step = 4;
            });
          }else if(step == 6){
	    $("#checkOut").fadeOut("fast",function(){
	      $("#modalTitleId").text(detailsPage);
	      $("#checkoutButton").hide();
	      $("#modalFooterDoneButton").show();
	      $("#modalBodyDetails").fadeIn("slow");
	    });
	    step = 5;
          }else if(step == 7){
	    $("#modalChargeFail").fadeOut("fast",function(){
              $("#modalFooterBackButton").addClass("disabled");
	      $("#doneButton").show();
              $("#modalTitleId").text(methodPage);
              $("#modalBodyMethod").fadeIn("slow");
            });
	    step = 1;
	  }else if(step == 8){
            $("#modalChargeWrong").fadeOut("fast",function(){
              $("#modalFooterBackButton").addClass("disabled");
              $("#doneButton").show();
              $("#modalTitleId").text(methodPage);
              $("#modalBodyMethod").fadeIn("slow");
            });
            step = 1;
          }else if(step == 9){
            $("#modalNotAvailable").fadeOut("fast",function(){
              $("#modalFooterBackButton").addClass("disabled");
              $("#doneButton").show();
              $("#modalTitleId").text(methodPage);
              $("#modalBodyMethod").fadeIn("slow");
            });
            step = 1;
          }	  
	});
	//////////////////////////////////////
	//////////////////////////////////////
{% if user.is_authenticated %}
var inWL = {{inWishlist}};
/////////////////////////
////WishList///////////////
        $("#wishlistButton").click(function(){
	  $(this).addClass("disabled");
	  $(this).html('<i class="fa fa-spinner fa-fw fa-spin"></i>');
	    if(inWL){
              key = "delete";
	    }else{
              key = "add";
	    }
	    addButton = '<i class="fa fa-lg fa-star-o fa-fw"></i>Add to Wish List';
	    removeButton = '<i class="fa fa-lg fa-star fa-fw"></i>Remove from Wish List';
	    cId = "{{object.id}}";
          $.get("{% url 'users:wishlist' user.pk %}",{key:key,cId:cId}, "json").done(function(data) {
		if(data.status == "added"){
		  inWL = true;
		  $("#wishlistButton").html(removeButton);
		}else{
		  inWL = false;
                  $("#wishlistButton").html(addButton);
		}
		$("#wishlistButton").removeClass("disabled");
          }).fail(function() {
            jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
            setTimeout(function() {
              location.reload();
            }, 3000);
          });
        });
/////////////////////////
{% endif %}
