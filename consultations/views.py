import json
import stripe
from django.db import IntegrityError
from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from consultations.models import Consultation
from professionals.models import Professional_Purchased_Consultation, Consultation_Order_Detail
from stripe_payment.models import Stripe_Error
from users.models import User_Consultation_Purchase
from django.utils.text import Truncator
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
import datetime
import time
import pytz
import calendar
import pprint
from django.conf import settings 
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from users.models import User_Consultation_Wishlist, User_Consultation_Purchase
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from home.models import Gonaturalistic, Activity
from django.template import loader
from django.template import Context, Template
from django.core.urlresolvers import reverse
from django.conf import settings 

class JSONResponseMixin(object):
        def render_to_json_response(self, context, **response_kwargs):
                data = json.dumps(context)
                response_kwargs['content_type'] = 'application/json'
                return HttpResponse(data, **response_kwargs)

class IndexView(ListView, FormView):
        template_name = 'consultations/consultationIndexPage.html'
        context_object_name = 'latest_consultation_list'
        form_class = AuthenticationForm
        paginate_by = 5

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
                self.sortBy = request.GET.get('sortBy', 'l')
                perPage = request.GET.get('perPage', None)
                if perPage:
                        self.paginate_by = int(perPage)
                else:
                        pass
                return super(IndexView, self).get(request, *args, **kwargs)

        def get_queryset(self):
                if self.user.is_superuser:
                        if self.sortBy:
                                if self.sortBy == "p":
                                        return Consultation.objects.order_by('-consultation_hits')
                                else:
                                        return Consultation.objects.order_by('-consultation_pubdate')
                        else:
                                return Consultation.objects.order_by('-consultation_pubdate')
                else:
                        if self.sortBy:
                                if self.sortBy == "p":
                                        return Consultation.objects.filter(consultation_status="p").order_by('-consultation_hits')
                                else:
                                        return Consultation.objects.filter(consultation_status="p").order_by('-consultation_pubdate')
                        else:
                                return Consultation.objects.filter(consultation_status="p").order_by('-consultation_pubdate')

        def get_context_data(self, **kwargs):
                context = super(IndexView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['url'] = self.url
                context['sortBy'] = self.sortBy
                return context

class ConsultationPageView(JSONResponseMixin, FormView, DetailView):
        model = Consultation
        template_name = 'consultations/consultationPage.html'
        form_class = AuthenticationForm

	def getMethodName(self, method):
		if method == "s":
			return "Skype"
		elif method == "ft":
			return "FaceTime"
		elif method == "ph":
			return "Phone Call"
		elif method == "o":
			return "Face to Face"
	def getDurationName(self, duration):
		if duration == "h":
			return "60 Minutes"
		elif duration == "hh":
			return "30 Minutes"
		elif duration == "qh":
			return "15 Minutes"

	def convertHourTo24(self,hour):
        	splited_str = hour.split(':')
        	hour = int(splited_str[0])
                splited_str = splited_str[1].split(' ')
                period = splited_str[1]
                if period == "AM":
                	if hour == 12:
                        	hour = 0
                elif period == "PM":
                        if hour == 1:
                        	hour = 13
                        elif hour == 2:
                                hour = 14
                        elif hour == 3:
                                hour = 15
                        elif hour == 4:
                                hour = 16
                        elif hour == 5:
                                hour = 17
                        elif hour == 6:
                                hour = 18
                        elif hour == 7:
                                hour = 19
                        elif hour == 8:
                                hour = 20
                        elif hour == 9:
                                hour = 21
                        elif hour == 10:
                                hour = 22
                        elif hour == 11:
                                hour = 23
		return hour

	def getServerDateTime(self):
        	serverTZ = pytz.timezone(settings.TIME_ZONE)
		#for testing replace(hour=12,minute=30,second=1,microsecond=0)
                serverToday = serverTZ.localize(datetime.datetime.now())
		return serverToday

	def getPractitionerTimeZone(self,obj):
                professional_tz = obj.professional_time_zone
                if professional_tz == "cst":
                        professionalTimeZone = "US/Central"
                elif professional_tz == "est":
                        professionalTimeZone = "US/Eastern"
                elif professional_tz == "pst":
                        professionalTimeZone = "US/Pacific"
                elif professional_tz == "mst":
                        professionalTimeZone = "US/Mountain"
                elif professional_tz == "gmtz":
                        professionalTimeZone = "Europe/London"
                elif professional_tz == "eest":
                        professionalTimeZone = "Europe/Istanbul"
                elif professional_tz == "cest":
                        professionalTimeZone = "Europe/Paris"
		return professionalTimeZone

	def getPractitionerDateTime(self,professionalTimeZone):
		professionalPytz = pytz.timezone(professionalTimeZone)
		return self.getServerDateTime().astimezone(professionalPytz)

        def getDateObj(self,obj,appointmentDate):
                dateObj = obj.professional_available_day_time_set.get(available_day=appointmentDate)
                return dateObj

        def getTimeObj(self,dateObj,appointmentTime):
                timeObj = dateObj.professional_available_time.get(consultation_time_period=appointmentTime)
                return timeObj

	#Get All available Dates for This practitioner
	def getAvailableDates(self,obj,professionalDateTime):
        	professionalToday = professionalDateTime.strftime("%Y-%m-%d")
                dates = obj.professional_available_day_time_set.filter(available_day__gte=professionalToday)
		return dates
	#Get Available Times (30 mins diffrence to current time) --> condition is 30 mins
	def getAvailableTimes(self,dateObj, duration, professionalDateTime):
		currentDay = professionalDateTime.strftime("%Y-%m-%d")
		conditionDateTime = professionalDateTime + datetime.timedelta(minutes=30)
		conditionalDay = conditionDateTime.strftime("%Y-%m-%d")
		conditionalTime = conditionDateTime.time().strftime("%H:%M:%S")

		if currentDay == dateObj.available_day.isoformat():
			if currentDay == conditionalDay:
	        		if duration == "h":
        				times = dateObj.professional_available_time.filter(consultation_duration="h",consultation_24hour_start_time__gte=conditionalTime)
        			elif duration == "hh":
                			times = dateObj.professional_available_time.filter(consultation_duration="hh",consultation_24hour_start_time__gte=conditionalTime)
        			elif duration == "qh":
                			times = dateObj.professional_available_time.filter(consultation_duration="qh",consultation_24hour_start_time__gte=conditionalTime)
				return times
			else:
				return []
		else:
			if conditionalDay == dateObj.available_day.isoformat():
	                        if duration == "h":
        	                        times = dateObj.professional_available_time.filter(consultation_duration="h",consultation_24hour_start_time__gte=conditionalTime)
				elif duration == "hh":
                                	times = dateObj.professional_available_time.filter(consultation_duration="hh",consultation_24hour_start_time__gte=conditionalTime)
                        	elif duration == "qh":
                                	times = dateObj.professional_available_time.filter(consultation_duration="qh",consultation_24hour_start_time__gte=conditionalTime)
                        	return times
			else:
                                if duration == "h":
                                        times = dateObj.professional_available_time.filter(consultation_duration="h")
                                elif duration == "hh":
                                        times = dateObj.professional_available_time.filter(consultation_duration="hh")
                                elif duration == "qh":
                                        times = dateObj.professional_available_time.filter(consultation_duration="qh")
                                return times

	#Does Date and Time meet Time Condition (30 mins diffrence to current time)
	def doesDateTimeMeetTimeCondition(self,dateObj,startTime,professionalDateTime):
		dateObjString = dateObj.available_day.isoformat()
                currentDay = professionalDateTime.strftime("%Y-%m-%d")
                conditionDateTime = professionalDateTime + datetime.timedelta(minutes=30)
                conditionalDay = conditionDateTime.strftime("%Y-%m-%d")
                conditionalTime = conditionDateTime.time()
		if currentDay == dateObjString:
			if currentDay == conditionalDay:
				if startTime >= conditionalTime:
					return True
				else:
					return False
			else:
				return False
		else:
			if conditionalDay == dateObjString:
                                if startTime >= conditionalTime:
                                        return True
				else:
					return False
			else:
				return True

	#Is Date and Time Still Available? Checks as Date and Time String
	def isDateTimeAvailable(self,obj,dateString,timeString):
        	cDateObj = self.getDateObj(obj,dateString)
                cTimeObj = self.getTimeObj(cDateObj,timeString)
		if not obj.professional_purchased_consultation_set.filter(consultation_day=cDateObj,consultation_time=cTimeObj).exists():
			return True
		else:
			return False

        #Is Date and Time Still Available? Checks as Date and Time Object
	def isDateTimeAvailableAsDateObj(self,obj,dateObj,timeObj):
                if not obj.professional_purchased_consultation_set.filter(consultation_day=dateObj,consultation_time=timeObj).exists():
                        return True
                else:
                        return False

	#Get Price of Method based on Duration
	def getPrice(self,method,duration,obj):
                if duration == "h":
                	price = obj.hour_price
                elif duration == "hh":
                        price = obj.half_hour_price
                elif duration == "qh":
                        price = obj.quarter_hour_price
		return price

	def isPromoCodeValid(self,obj,promoCode):
        	today = datetime.datetime.today().date()
                promo_obj = obj.professional_promo_code_set.filter(promo_code_start_date__lte=today,promo_code_end_date__gte=today,promo_code=promoCode)
                return promo_obj.exists()

	def getPromoObj(self,obj,promoCode):
		promoObj = obj.professional_promo_code_set.get(promo_code=promoCode)
		return promoObj

	def calculatePromoCode(self,price,percent):
		priceAfterPromoCode = Decimal(price) - ((Decimal(price)*int(percent))/100)
		return str(priceAfterPromoCode)

        def get(self, request, *args, **kwargs):
                key = request.GET.get('key', None)
		duration = request.GET.get('duration', None)
		timeZone = request.GET.get('timeZone', None)
		method = request.GET.get('method', None)
		promoCode = request.GET.get('promoCode', None)
		appointmentTime = request.GET.get('time', None)
		appointmentDate = request.GET.get('date', None)
		obj = self.get_object().consultation_professional
                practitionerTimeZone = self.getPractitionerTimeZone(obj)
                practitionerDateTime =  self.getPractitionerDateTime(practitionerTimeZone)
                if self.request.is_ajax():
			if key == "methodDuration":
				method_obj = obj.consultation_method_set.order_by('consultation_method_order')
				x = []
				for method in  method_obj:
					y = {}
					y['method_name'] = method.consultation_method_name
					y['method_status'] = method.consultation_method_status
					y['method_hour'] = method.consultation_method_hour_allowed
                                	y['method_half_hour'] = method.consultation_method_half_hour_allowed
                                	y['method_quarter_hour'] = method.consultation_method_quarter_hour_allowed
					y['method_order'] = method.consultation_method_order
					x.append(y)
				time.sleep(1);
				return self.render_to_json_response(x)
			elif key == "dateTime" and duration:
				dates = self.getAvailableDates(obj,practitionerDateTime)
				a = []
				b = {}
				calendarInfo = {}
				createCalendar = calendar
				createCalendar.setfirstweekday(calendar.SUNDAY)
                                calendarInfo["practitionerTimeZone"] = practitionerTimeZone
				calendarInfo["userCurrentDay"] = practitionerDateTime.day
				calendarInfo["firstMonthName"] = practitionerDateTime.strftime("%b %Y")
                                calendarInfo["firstYearMonth"] = practitionerDateTime.strftime("%Y-%m")
				calendarInfo["firstMonthData"] = createCalendar.monthcalendar(int(practitionerDateTime.year),int(practitionerDateTime.month))	
				nextMonthUser_tz = practitionerDateTime + datetime.timedelta(days=(practitionerDateTime.max.day - practitionerDateTime.day)+1)
                                calendarInfo["nextMonthName"] = nextMonthUser_tz.strftime("%b %Y")
                                calendarInfo["nextYearMonth"] = nextMonthUser_tz.strftime("%Y-%m")
                                calendarInfo["nextMonthData"] = createCalendar.monthcalendar(int(nextMonthUser_tz.year),int(nextMonthUser_tz.month))
				a.append(calendarInfo)
                                for date in dates:
					times = self.getAvailableTimes(date,duration,practitionerDateTime)
					c = []
					for timeModel in times:
						d = {}
						d['type'] = timeModel.consultation_duration
						d['ss'] = str(timeModel.consultation_24hour_start_time)
						d['start_time'] = timeModel.consultation_start_time
						d['period'] = str(timeModel)
						if self.isDateTimeAvailableAsDateObj(obj,date,timeModel):
							d['status'] = "available"
						else:
							d['status'] = "sold"
						c.append(d)
					b[str(date)] = c
				a.append(b)
				time.sleep(1)	
				return self.render_to_json_response(a)

			if key == "getPrice" and duration and method:
				price = str(self.getPrice(method,duration,obj))
				time.sleep(1)
				return self.render_to_json_response({"price": price})

			if key == "validatePromoCode" and promoCode and method and duration:
				price = str(self.getPrice(method,duration,obj))
				dict = {}
				if self.isPromoCodeValid(obj,promoCode):
					promoObj = self.getPromoObj(obj,promoCode)
					percent = promoObj.promo_code_percent
					dict["status"] = "valid"
					dict["percent"] = percent
					dict["price"] = self.calculatePromoCode(price,percent)
					dict["promoCode"] = promoCode	
				else:
                                        dict["status"] = "invalid"

				time.sleep(1)
				return self.render_to_json_response(dict)
							
			if key == "getStripe" and appointmentDate and appointmentTime and duration and method:
				consultationObj = self.get_object()
                                dateObj = self.getDateObj(obj,appointmentDate)
				price = str(self.getPrice(method,duration,obj))
				dict = {}
				if promoCode:
					if self.isPromoCodeValid(obj,promoCode):
						promoObj = self.getPromoObj(obj,promoCode)
						percent = promoObj.promo_code_percent
						price = self.calculatePromoCode(price,percent)
						dict['price'] = price
					else:
                                        	dict['price'] = price
				else:									
					dict['price'] = price
				dict['description'] = consultationObj.consultation_title+" "+"Consultation"					
				return self.render_to_json_response(dict)

			if key == "isTimeStillAvailable" and appointmentDate and appointmentTime:
                                dateObj = self.getDateObj(obj,appointmentDate)
                                timeObj = self.getTimeObj(dateObj,appointmentTime).consultation_24hour_start_time
				dict = {}
                                if self.isDateTimeAvailable(obj,appointmentDate,appointmentTime):
                                        if self.doesDateTimeMeetTimeCondition(dateObj,timeObj,practitionerDateTime):
                                                dict['status'] = "y"
                                        else:
                                                dict['status'] = "n"
                                else:
                                        dict['status'] = "n"
				time.sleep(1)
				return self.render_to_json_response(dict)
			
                self.user = request.user
                self.url = request.path
                return super(ConsultationPageView, self).get(request, *args, **kwargs)

        @csrf_exempt
        def dispatch(self, *args, **kwargs):
                return super(ConsultationPageView, self).dispatch(*args, **kwargs)

        def post(self, request, *args, **kwargs):
                duration = request.POST.get('duration', None)
                method = request.POST.get('method', None)
                promoCode = request.POST.get('promoCode', None)
                appointmentTime = request.POST.get('time', None)
                appointmentDate = request.POST.get('date', None)
                obj = self.get_object().consultation_professional
                practitionerTimeZone = self.getPractitionerTimeZone(obj)
                practitionerDateTime =  self.getPractitionerDateTime(practitionerTimeZone)
                token = request.POST.get('stripeToken', None)

		if settings.STRIPE_MODE == "TEST":
                	stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
		elif settings.STRIPE_MODE == "LIVE":
                        stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

		if self.request.is_ajax():
			if token and duration and method and appointmentTime and appointmentDate:
                                dateTimeStillAvailable = False
                                dateObj = self.getDateObj(obj,appointmentDate)
                                timeObj = self.getTimeObj(dateObj,appointmentTime).consultation_24hour_start_time
				methodObj = obj.consultation_method_set.get(consultation_method_name=method)
                                consultationObj = self.get_object()
                                price = str(self.getPrice(method,duration,obj))
				firstPrice = price
                                if promoCode:
                                        if self.isPromoCodeValid(obj,promoCode):
                                                promoObj = self.getPromoObj(obj,promoCode)
                                                percent = promoObj.promo_code_percent
                                                price = self.calculatePromoCode(price,percent)
                                                stripePrice = price
                                        else:
                                                stripePrice = price
                                else:
                                        stripePrice = price
                                description = consultationObj.consultation_title+" "+"Consultation"

                                if self.isDateTimeAvailable(obj,appointmentDate,appointmentTime):
                                        if self.doesDateTimeMeetTimeCondition(dateObj,timeObj,practitionerDateTime):
                                                dateTimeStillAvailable = True
                                        else:
                                                dateTimeStillAvailable = False
                                else:
                                        dateTimeStillAvailable = False

                                respond = {}
				#Professional_Purchased_Consultation, Consultation_Order_Detail
                                saveConsultation = Professional_Purchased_Consultation(
                                        user=request.user,
					professional=obj,
                                        consultation=self.get_object(),
                                        consultation_day=dateObj,
                                        consultation_time=self.getTimeObj(dateObj,appointmentTime),
                                	consultation_method=methodObj
                                )
				if dateTimeStillAvailable:
                			try:
						try:
                                                	saveConsultation.save()
						except IntegrityError:
							respond['payment'] = "gone"
							return self.render_to_json_response(respond)

						customer = stripe.Customer.create(
							card=token,
							email=request.user.username,
                                                        description="GoNaturalistic Customer"
						)
                        			charge = stripe.Charge.create(
                                			amount=int(Decimal(stripePrice)*100),
                                			currency="usd",
                                                        description=description,
							customer=customer.id
                        			)
						#Consultation_Order_Detail
						saveConsultation.consultation_time_status = 's'
						saveConsultation.stripe_customer = customer.id
						saveConsultation.stripe_token = token
						saveConsultation.stripe_charge = charge.id
						saveConsultation.payment = Decimal(stripePrice)
						saveConsultation.save()
                                                if not promoCode:
                                                	percent = 0
						consultation_order_detail = Consultation_Order_Detail(
							professional_purchased_consultation = saveConsultation,
							user_name = request.user.username,
							professional_name = obj.professional_full_name,
        						consultation_name = self.get_object().consultation_title,
        						consultation_method_name = method,
        						consultation_date = dateObj.available_day.strftime("%A %b %d, %Y"),
        						consultation_time_period = appointmentTime,
        						consultation_time_zone = practitionerTimeZone,
							consultation_duration = duration,
							full_price = str(firstPrice),
							promo_code_discount = str(percent),
							final_price = str(stripePrice)
						)
						consultation_order_detail.save()
						user_consultation_purchase = User_Consultation_Purchase(
							user = request.user,
							professional_purchased_consultation = saveConsultation,
							consultation_order_detail = consultation_order_detail							
						)
						user_consultation_purchase.save()
						#Send Emails##########################
                        			serverTZ = pytz.timezone(settings.TIME_ZONE)
                        			serverToday = serverTZ.localize(datetime.datetime.now())
						emailObj = Activity.objects.all()[0]
						to = request.user.username
						from_email = emailObj.consultation_purchase_email_from
						c = {
							'username': request.user.first_name.title(),
							'user_email': request.user.username,
							'professional_email': obj.professional_email,
							'user_phone': request.user.user_account_set.all()[0].user_phone,
							'from_email': from_email,
							'consultation': self.get_object().consultation_title,
							'professional': obj.professional_full_name,
							'method': self.getMethodName(method),
							'duration': self.getDurationName(duration),
							'date': dateObj.available_day.strftime("%A %b %d, %Y"),
							'time': appointmentTime,
							'timezone': practitionerTimeZone,
							'link': reverse('users:consultations', args=[request.user.pk]),
                                                        'initial_price': str(firstPrice),
							'promo_code_percent': str(percent),
							'final_price': str(stripePrice),
							'purchase_date': serverToday
						}
						html = emailObj.consultation_purchase_email_message_to_user
						#msg = loader.render_to_string(html, c)
						t = Template(html)
						con = Context(c)
						message = t.render(con)
						subject = emailObj.consultation_purchase_email_subject
						msg = EmailMessage(subject,message,from_email,[to])
                                                msg.content_subtype = "html"
                                                msg.send()
						#send Email from Professional##########
						professional_html = obj.professional_consultation_purchase_email_message
						professional_subject = obj.professional_consultation_purchase_email_subject
						professional_from_email = obj.professional_consultation_purchase_email_from
                                                c2 = {
                                                        'username': request.user.first_name.title(),
							'methodList': obj.consultation_method_set.filter(consultation_method_status="y")
                                                }						
                                                t2 = Template(professional_html)
                                                con2 = Context(c2)
                                                professional_message = t2.render(con2)
                                                msg2 = EmailMessage(professional_subject,professional_message,professional_from_email,[to])
                                                msg2.content_subtype = "html"
                                                msg2.send() 
						##############################
						#Send Email to Professional#######
                                                html3 = emailObj.consultation_purchase_email_message_to_professional
                                                t3 = Template(html3)
                                                con3 = Context(c)
                                                message3 = t3.render(con3)
						professional_email = obj.professional_email
						professional_gn_email = obj.professional_gn_email
						msg3 = EmailMessage(subject,message3,from_email,[professional_email,professional_gn_email])
                                                msg3.content_subtype = "html"
                                                msg3.send()
						#Send Activity Email to GoNaturalistic
 			                       	activity_subject = "GoNaturalistic Consultation Purchase"
						activity_to = emailObj.activity_email
                                                html4 = emailObj.activity_purchase
                                                t4 = Template(html4)
                                                con4 = Context(c)
                        			activity_message = t4.render(con4)
                        			msg4 = EmailMessage(activity_subject,activity_message,from_email,[activity_to])
                        			msg4.content_subtype = "html"
                        			msg4.send()
						#############################
						respond['payment'] = "ok"
                        			return self.render_to_json_response(respond)
                			except stripe.error.CardError, e:
						saveConsultation.delete()
						body = e.json_body
						err  = body['error']
						stripeError = Stripe_Error(user=request.user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
						stripeError.save()
                        			respond['payment'] = "fail"
                        			return self.render_to_json_response(respond)
					except stripe.error.InvalidRequestError, e:
  					# Invalid parameters were supplied to Stripe's API
                                                saveConsultation.delete()
                        			body = e.json_body
                        			err  = body['error']
                        			stripeError = Stripe_Error(user=request.user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
                        			stripeError.save()
                        			respond['payment'] = "wrong"
                        			return self.render_to_json_response(respond)
					except stripe.error.AuthenticationError, e:
  					# Authentication with Stripe's API failed
  					# (maybe you changed API keys recently)
                                                saveConsultation.delete()
                        			body = e.json_body
                        			err  = body['error']
                        			stripeError = Stripe_Error(user=request.user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
                        			stripeError.save()
                        			respond['payment'] = "wrong"
                        			return self.render_to_json_response(respond)
					except stripe.error.APIConnectionError, e:
  					# Network communication with Stripe failed
                                                saveConsultation.delete()
                        			body = e.json_body
                        			err  = body['error']
                        			stripeError = Stripe_Error(user=request.user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
                        			stripeError.save()
                        			respond['payment'] = "wrong"
                        			return self.render_to_json_response(respond)
					except stripe.error.StripeError, e:
  					# Display a very generic error to the user, and maybe send
  					# yourself an email
                                                saveConsultation.delete()
                        			body = e.json_body
                        			err  = body['error']
                        			stripeError = Stripe_Error(user=request.user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
                        			stripeError.save()
                        			respond['payment'] = "wrong"
                        			return self.render_to_json_response(respond)
					except Exception, e:
  					# Something else happened, completely unrelated to Stripe
                                                saveConsultation.delete()
                        			stripeError = Stripe_Error(user=request.user,json_data="Something else happened, completely unrelated to Stripe")
                        			stripeError.save()
                        			respond['payment'] = "wrong"
                        			return self.render_to_json_response(respond)
				else:
					respond['payment'] = "gone"
					return self.render_to_json_response(respond)
			else:
				pass
                return HttpResponse("done")

        def get_context_data(self, **kwargs):
                context = super(ConsultationPageView, self).get_context_data(**kwargs)
                self.object.hit()
                context['form'] = self.get_form(self.form_class)
                context['consultationCategories']= self.object.consultation_category_set.all()
		if self.user.is_authenticated():
			context['inWishlist'] = str(User_Consultation_Wishlist.objects.filter(user=self.user,consultation=self.object).exists()).lower()
                if self.object.s_article == "y":
                        if self.user.is_superuser:
                                context['suggestedArticles']= self.object.consultation_suggested_article_set.all()
                        else:
                                context['suggestedArticles']= self.object.consultation_suggested_article_set.filter(s_article__article_status="p")
                if self.object.s_consultation == "y":
                        if self.user.is_superuser:
                                context['suggestedConsultations']= self.object.consultation_suggested_consultation_set.all()
                        else:
                                context['suggestedConsultations']= self.object.consultation_suggested_consultation_set.filter(s_consultation__consultation_status="p")
		if settings.STRIPE_MODE == "TEST":
			context['stripePubKey'] = settings.STRIPE_TEST_PUB_KEY 
		elif settings.STRIPE_MODE == "LIVE":
                        context['stripePubKey'] = settings.STRIPE_LIVE_PUB_KEY
                return context


