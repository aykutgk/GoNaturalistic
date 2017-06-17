function addError(obj){
  formGroupObj = obj.parent().parent();
  colSpanObj = obj.parent();
  formGroupObj.addClass("has-error has-feedback");
  colSpanObj.append('<i class="fa fa-exclamation-triangle form-control-feedback"></i>');
}
function removeError(obj){
  formGroupObj = obj.parent().parent();
  colSpanObj = obj.parent();
  formGroupObj.removeClass("has-error has-feedback");
  colSpanObj.find("i").remove();
}
function hasError(obj){
  formGroupObj = obj.parent().parent();
  return formGroupObj.hasClass("has-error");
}
function validate(formObj){
  inputs = formObj.find(":input");
  regex =/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i;
  $.each(inputs, function(i,field){
    obj = $(field);
    value = obj.val();
    tag = obj.prop("tagName");
    if(tag == "INPUT"){
      type = obj.attr("type");
      if(type == "text"){
        if(value == ""){
          addError(obj);
        }else if( hasError(obj) && value != ""){
	  removeError(obj);
        }        
      }else if(type == "email"){
	if(value == "" || ! regex.test(value)){
	  addError(obj);
        }else{
	  removeError(obj);
        }
      }
    }else if(tag == "TEXTAREA"){
      if(value == ""){ 
        addError(obj);
      }else if( hasError(obj) && value != ""){
        removeError(obj);
      }
    }
  });
return ! formObj.find(".form-group").hasClass("has-error");}
$("#contactusSendButton").click(function(e){
  successAlert = $("#formSentAlert");
  failAlert = $("#formFailedAlert");
  failAlert.hide();
  panel = $("#formContent");
  buttonHtml = $(this).html();
  buttonObj = $(this);
  loader = '<i class="fa fa-spinner fa-fw fa-spin"></i>';
  formObj = $("#contactusForm");
  fieldsetObj = formObj.find("fieldset");
  serializedData = formObj.serialize();
  flag = false;
  flag = validate(formObj);
  if(flag){
    fieldsetObj.attr("disabled", true);
    buttonObj.html(loader);
    $.post("", serializedData, "json").done(function(data) {
      if(data.status == "ok"){
        panel.fadeOut("fast", function(){
	  successAlert.fadeIn("slow");
        });
      }else{
	fieldsetObj.removeAttr("disabled");
        buttonObj.html(buttonHtml);
	failAlert.show();
      }
    }).fail(function() {
      jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
      setTimeout(function() {
        location.reload();
      }, 3000);
    });
  }
  e.preventDefault();
});

