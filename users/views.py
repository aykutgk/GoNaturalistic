import json
import stripe
from django.views.generic import FormView, CreateView, ListView, DetailView
from django.views.generic.edit import UpdateView
from django import forms
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from users.forms import UserLoginForm, UserAccountForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from articles.models import Article
from consultations.models import Consultation
from categories.models import Category
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from users.models import User_Account, User_Consultation_Wishlist, User_Consultation_Purchase
from stripe_payment.models import Stripe_Error
import datetime
import time
import pytz
from django.conf import settings
from home.models import Gonaturalistic, Activity
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from django.template import Context, Template
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class JSONResponseMixin(object):
        def render_to_json_response(self, context, **response_kwargs):
                data = json.dumps(context)
                response_kwargs['content_type'] = 'application/json'
                return HttpResponse(data, **response_kwargs)

#User Signup
class UserSignupView(JSONResponseMixin, CreateView):
        model = User
        template_name = 'users/userSignupPage.html'
        form_class = UserCreationForm

	#@csrf_protect
	#@never_cache
        @method_decorator(user_passes_test(lambda u: u.is_anonymous(),login_url="/",redirect_field_name=None))
        def dispatch(self, *args, **kwargs):
                return super(UserSignupView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                self.url = request.path
                return super(UserSignupView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserSignupView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['url'] = self.url
		context['terms'] = Gonaturalistic.objects.all()[0].terms
                return context

        def post(self, request, *args, **kwargs):
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        username = form.clean_username()
			user_full_name = form.cleaned_data['first_name']
                        password = form.clean_password2()
                        form.save()
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        userAccount = User_Account(pk=user.pk,user=user,user_full_name=user_full_name)
                        userAccount.save()
			registration_subject = Activity.objects.all()[0].registration_email_subject
			registration_email_from = Activity.objects.all()[0].registration_email_from
                        registration_content = Activity.objects.all()[0].registration_email_message
			activity_content = Activity.objects.all()[0].activity_registration
			activity_to = Activity.objects.all()[0].activity_email
			serverTZ = pytz.timezone(settings.TIME_ZONE)
                	serverToday = serverTZ.localize(datetime.datetime.now())
                        c = {
                        	'username': request.user.first_name.title(),
                                'articles_url': reverse('articles:index'),
                                'consultations_url': reverse('consultations:index'),
                                'professionals_url': reverse('professionals:index'),
                                'categories_url': reverse('categories:index'),
				'contact_url': reverse('home:contactus'),
                                'user_email': request.user.username, 
                                'from_email': registration_email_from,
				'current_date': serverToday
                        }
                        html = registration_content
                        t = Template(html)
                        con = Context(c)
                        message = t.render(con)
			#No need to make a connection
			#connection = get_connection(fail_silently=False,host="mail.gonaturalistic.com",port="465",username="team@gonaturalistic.com",password="team666666",use_tls=True)
			#msg = EmailMessage(registration_subject,message,registration_email_from,[username],connection=connection)
			msg = EmailMessage(registration_subject,message,registration_email_from,[username])
                        msg.content_subtype = "html"
                        msg.send()

			activity_subject = "GoNaturalistic New Member"
                        html = activity_content
                        t = Template(html)
                        con = Context(c)
			activity_message = t.render(con) 
                        msg2 = EmailMessage(activity_subject,activity_message,registration_email_from,[activity_to])
                        msg2.content_subtype = "html"
                        msg2.send()
			
                        if self.request.is_ajax():
                                data = {'user': 'created'}
                                return self.render_to_json_response(data)
                else:
                        if self.request.is_ajax():
                                #data = {'user': 'exist'}
                                return self.render_to_json_response(form.errors)

#User Login
class UserLoginView(JSONResponseMixin, FormView):
        model = User
        template_name = 'users/userLoginPage.html'
        form_class = AuthenticationForm

        @method_decorator(user_passes_test(lambda u: u.is_anonymous(),login_url="/",redirect_field_name=None))
        def dispatch(self, *args, **kwargs):
                return super(UserLoginView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                self.url = request.path
                return super(UserLoginView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserLoginView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['url'] = self.url
                return context

        def post(self, request, *args, **kwargs):
                form = self.get_form(self.form_class)
                if form.is_valid():
                        login(request, form.get_user())
                        if not request.POST.get('rememberMe', None):
                                request.session.set_expiry(0)
                        if self.request.is_ajax():
                                data = {'user': 'valid'}
                                return self.render_to_json_response(data)
                else:
                        if self.request.is_ajax():
                                return self.render_to_json_response(form.errors)

#User LogOut 
@never_cache
def UserLogoutView(request):
        logout(request)
        return HttpResponseRedirect('/')

#User Search
class UserSearchView(JSONResponseMixin, ListView):
        model = User
        template_name = 'users/userSearchPage.html'

        @method_decorator(never_cache)
        def dispatch(self, *args, **kwargs):
                return super(UserSearchView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                searchKey = request.GET.get('searchKey', None)
                if self.request.is_ajax():
                        searchArray = {}
                        x = []
                        #articleObjs = Article.objects.filter(Q(article_title__istartswith=searchKey))[:3]
			articleObjs = Article.objects.filter(article_status="p",article_title__istartswith=searchKey)[:3]
                        for obj in articleObjs:
                                y = {}
                                y['title'] = obj.article_title
                                y['href'] = obj.slug
                                x.append(y)
                        searchArray['articleSearch'] = x
                        x = []
                        categoryObjs = Category.objects.filter(category_name__istartswith=searchKey)[:3]
                        for obj in categoryObjs:
                                y = {}
                                y['title'] = obj.category_name.title()
                                y['href'] = obj.slug
                                x.append(y)
                        searchArray['categorySearch'] = x
                        x = []
                        consultationObjs = Consultation.objects.filter(consultation_status="p",consultation_title__istartswith=searchKey)[:3]
                        for obj in consultationObjs:
                                y = {}
                                y['title'] = obj.consultation_title
                                y['href'] = obj.slug
                                x.append(y)
                        searchArray['consultationSearch'] = x
                        return self.render_to_json_response(searchArray)
		return super(UserSearchView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserSearchView, self).get_context_data(**kwargs)
                return context 


class UserAccountView(JSONResponseMixin, UpdateView):
        model = User_Account
        template_name = 'users/userAccountPage.html'
        form_class = UserAccountForm
	success_url = '.'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserAccountView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
		if self.get_object().user.pk != request.user.pk:
			return HttpResponseRedirect(reverse('users:account', args=(request.user.pk,)))			
                return super(UserAccountView, self).get(request, *args, **kwargs)

    	def form_valid(self, form):
		full_name = form.cleaned_data['user_full_name']
		self.request.user.first_name = full_name
		self.request.user.save()
        	return super(UserAccountView, self).form_valid(form)

	#def form_invalid(self, form):
	#	return super(UserAccountView, self).form_invalid(form)

        def get_context_data(self, **kwargs):
                context = super(UserAccountView, self).get_context_data(**kwargs)
                return context

class UserWishlistView(JSONResponseMixin, UpdateView):
        model = User_Account
        template_name = 'users/userWishlistPage.html'
        form_class = UserAccountForm

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserWishlistView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('users:account', args=(request.user.pk,)))
		key = request.GET.get('key', None)
                cId = request.GET.get('cId', None)
		if self.request.is_ajax():
			if key and cId:
				if key == "add":
					cObj = Consultation.objects.get(pk=cId)
					wl = User_Consultation_Wishlist(user=request.user,consultation=cObj)
					wl.save()
					time.sleep(0.5)
					return self.render_to_json_response({"status":"added"})
				elif key == "delete":
					cObj = Consultation.objects.get(pk=cId)
					wl = User_Consultation_Wishlist.objects.get(user=request.user,consultation=cObj)
					wl.delete()
                                        time.sleep(0.5) 
					return self.render_to_json_response({"status":"deleted"})

                return super(UserWishlistView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserWishlistView, self).get_context_data(**kwargs)
		context['wishlists'] = self.object.user.user_consultation_wishlist_set.all()
                return context


class UserConsultationView(JSONResponseMixin, DetailView):
        model = User_Account
        template_name = 'users/userConsultationPage.html'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserConsultationView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('users:account', args=(request.user.pk,)))
                self.sortBy = request.GET.get('sortBy', None)
		self.perPage = request.GET.get('perPage', None)
		if not self.perPage:
			self.perPage = 2
		else:
			self.perPage = int(self.perPage)

                self.cPage = request.GET.get('cPage', None)
                if not self.cPage:
                        self.cPage = 1
                else:
                        self.cPage = int(self.cPage)

                return super(UserConsultationView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserConsultationView, self).get_context_data(**kwargs)

		if self.sortBy:
			if self.sortBy == 'u':
				my_consultations = self.object.user.user_consultation_purchase_set.filter(consultation_status="u").order_by('-professional_purchased_consultation__date')
			elif self.sortBy == 's':
                                my_consultations = self.object.user.user_consultation_purchase_set.filter(consultation_status="s").order_by('-professional_purchased_consultation__date')
			elif self.sortBy == 'c':
                                my_consultations = self.object.user.user_consultation_purchase_set.filter(consultation_status="c").order_by('-professional_purchased_consultation__date')
			else:
				my_consultations = self.object.user.user_consultation_purchase_set.all().order_by('order','-professional_purchased_consultation__date')
		else:
			my_consultations = self.object.user.user_consultation_purchase_set.all().order_by('order','-professional_purchased_consultation__date')

		paginator = Paginator(my_consultations, self.perPage)				
		#context['myconsultations'] = self.object.user.user_consultation_purchase_set.all().order_by('-professional_purchased_consultation__date')
		try:
                	context['myconsultations'] = paginator.page(self.cPage).object_list
			context['page_obj'] = paginator.page(self.cPage)
		except PageNotAnInteger:
                        context['myconsultations'] = paginator.page(1).object_list
                        context['page_obj'] = paginator.page(1)
		except EmptyPage:
                        context['myconsultations'] = paginator.page(paginator.num_pages).object_list
                        context['page_obj'] = paginator.page(paginator.num_pages)
			
		context['sortBy'] = self.sortBy
                return context

class UserConsultationNotesView(JSONResponseMixin, DetailView):
        model = User_Consultation_Purchase
        template_name = 'users/userConsultationNotesPage.html'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserConsultationNotesView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('home:index'))
                return super(UserConsultationNotesView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(UserConsultationNotesView, self).get_context_data(**kwargs)
                return context

class UserConsultationMethodDetailsView(JSONResponseMixin, DetailView):
        model = User_Consultation_Purchase
        template_name = 'users/userConsultationMethodDetailsPage.html'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserConsultationMethodDetailsView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('home:index'))
                return super(UserConsultationMethodDetailsView, self).get(request, *args, **kwargs)

        def getCurrentTime(self,tz):
                serverTZ = pytz.timezone(settings.TIME_ZONE)
                #.replace(day=24,hour=10,minute=30,second=0,microsecond=0)
                serverToday = serverTZ.localize(datetime.datetime.now())
                timezone = pytz.timezone(tz)
                return serverToday.astimezone(timezone)

        def moreThan24Hours(self,timeZone, pObj):
                appDate = pObj.consultation_day.available_day
                appTime = pObj.consultation_time.consultation_24hour_start_time
                serverTZ = pytz.timezone(timeZone)
                appDatetime = serverTZ.localize(datetime.datetime.combine(appDate,appTime))
                currentDatetime = self.getCurrentTime(timeZone)
                timedelta = appDatetime - currentDatetime

                if timedelta.days == 0:
                        if timedelta.seconds >=0:
                                return "no"
                        else:
                                return "expired"
                elif timedelta.days > 0:
                        return "yes"
                else:
                        return "expired"

                return timedelta.days

        def get_context_data(self, **kwargs):
                context = super(UserConsultationMethodDetailsView, self).get_context_data(**kwargs)
                obj = self.object
                pObj = obj.professional_purchased_consultation
                dObj = obj.consultation_order_detail
                #before 24 hour
                tz = dObj.consultation_time_zone
                if obj.consultation_status == "u":
                        status = self.moreThan24Hours(tz,pObj)
                else:
                        status = 'none'
                context['status'] = status
                return context

class UserConsultationMethodChangeView(JSONResponseMixin, DetailView):
        model = User_Consultation_Purchase
        template_name = 'users/userConsultationMethodChangePage.html'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserConsultationMethodChangeView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('home:index'))
                return super(UserConsultationMethodChangeView, self).get(request, *args, **kwargs)

        def getCurrentTime(self,tz):
                serverTZ = pytz.timezone(settings.TIME_ZONE)
                #.replace(day=24,hour=10,minute=30,second=0,microsecond=0)
                serverToday = serverTZ.localize(datetime.datetime.now())
                timezone = pytz.timezone(tz)
                return serverToday.astimezone(timezone)

        def moreThan24Hours(self,timeZone, pObj):
                appDate = pObj.consultation_day.available_day
                appTime = pObj.consultation_time.consultation_24hour_start_time
                serverTZ = pytz.timezone(timeZone)
                appDatetime = serverTZ.localize(datetime.datetime.combine(appDate,appTime))
                currentDatetime = self.getCurrentTime(timeZone)
                timedelta = appDatetime - currentDatetime

                if timedelta.days == 0:
                        if timedelta.seconds >=0:
                                return "no"
                        else:
                                return "expired"
                elif timedelta.days > 0:
                        return "yes"
                else:
                        return "expired"

                return timedelta.days

        def post(self, request, *args, **kwargs):
                method = request.POST.get('methodName', None)
                if self.request.is_ajax() and method:
                        obj = self.get_object()
                        pObj = obj.professional_purchased_consultation
                        dObj = obj.consultation_order_detail
                        #before 24 hour
                        tz = dObj.consultation_time_zone
                        status = self.moreThan24Hours(tz,pObj)
                        payment = pObj.payment
                        if not status == "expired":
                                methodObj = pObj.professional.consultation_method_set.get(consultation_method_name=method)
                                pObj.consultation_method = methodObj
                                dObj.consultation_method_name = methodObj.consultation_method_name
                                pObj.save()
                                dObj.save()
				#Send Emails#####
                                serverTZ = pytz.timezone(settings.TIME_ZONE)
                                serverToday = serverTZ.localize(datetime.datetime.now())
                                c = {
                                        'username': request.user.first_name.title(),
                                        'user_email': request.user.username,
                                        'user_phone': request.user.user_account_set.all()[0].user_phone,
                                        'professional': pObj.professional.professional_full_name,
                                        'professional_email': pObj.professional.professional_email,
                                        'consultation': dObj.consultation_name,
                                        'duration': dObj.consultation_duration,
                                        'method': dObj.consultation_method_name,
                                        'date': dObj.consultation_date,
                                        'time': dObj.consultation_time_period,
                                        'timezone': tz,
                                        'link': reverse('users:consultationMethodDetails', args=[obj.pk]),
                                        'change_date': serverToday
                                }
				emailObj = Activity.objects.all()[0] 
				change_email_from = emailObj.consultation_change_method_from
				change_email_subject = emailObj.consultation_change_method_email_subject 
				change_email_user_to = request.user.username
				change_email_professional_to = pObj.professional.professional_email 
				change_email_professional_gn_to = pObj.professional.professional_gn_email
				change_email_user_message_html = emailObj.consultation_change_method_email_message_to_user
				change_email_professional_message_html = emailObj.consultation_change_method_email_message_to_professional
                                #Send Email to User
                                t = Template(change_email_user_message_html)
                                con = Context(c)
                                message = t.render(con)
                                msg = EmailMessage(change_email_subject,message,change_email_from,[change_email_user_to])
                                msg.content_subtype = "html"
                                msg.send()
                                #Send Email to Professional
                                t = Template(change_email_professional_message_html)
                                con = Context(c)
                                message = t.render(con)
                                msg = EmailMessage(change_email_subject,message,change_email_from,[change_email_professional_to,change_email_professional_gn_to])
                                msg.content_subtype = "html"
                                msg.send()
                                data = {'status': 'changed'}
                                return self.render_to_json_response(data)
                        else:
                                data = {'status': 'expired'}
                                return self.render_to_json_response(data)

        def get_context_data(self, **kwargs):
                context = super(UserConsultationMethodChangeView, self).get_context_data(**kwargs)
		obj = self.object
                pObj = obj.professional_purchased_consultation
                dObj = obj.consultation_order_detail
                #before 24 hour
                tz = dObj.consultation_time_zone
                if obj.consultation_status == "u":
                        status = self.moreThan24Hours(tz,pObj)
                else:
                        status = "none"
                context['status'] = status
		# consultation_method_quarter_hour_allowed consultation_method_half_hour_allowed consultation_method_hour_allowed
		duration = self.object.consultation_order_detail.consultation_duration
		if duration == 'h':
			context['availableMethods'] = self.object.professional_purchased_consultation.professional.consultation_method_set.filter(consultation_method_status='y',consultation_method_hour_allowed='y')
		elif duration == 'hh':
                        context['availableMethods'] = self.object.professional_purchased_consultation.professional.consultation_method_set.filter(consultation_method_status='y',consultation_method_half_hour_allowed='y')
		elif duration == 'qh':
                        context['availableMethods'] = self.object.professional_purchased_consultation.professional.consultation_method_set.filter(consultation_method_status='y',consultation_method_quarter_hour_allowed='y')
                context['selectedMethod'] = self.object.professional_purchased_consultation.consultation_method.consultation_method_name
                return context

class UserConsultationCancelView(JSONResponseMixin, DetailView):
        model = User_Consultation_Purchase
        template_name = 'users/userConsultationCancelPage.html'

        @method_decorator(login_required(redirect_field_name=None,login_url='/user/login/'))
        def dispatch(self, *args, **kwargs):
                return super(UserConsultationCancelView, self).dispatch(*args, **kwargs)

        def get(self, request, *args, **kwargs):
                if self.get_object().user.pk != request.user.pk:
                        return HttpResponseRedirect(reverse('home:index'))
                return super(UserConsultationCancelView, self).get(request, *args, **kwargs)


        def getCurrentTime(self,tz):
                serverTZ = pytz.timezone(settings.TIME_ZONE)
		#.replace(day=24,hour=10,minute=30,second=0,microsecond=0)
                serverToday = serverTZ.localize(datetime.datetime.now())
                timezone = pytz.timezone(tz)
                return serverToday.astimezone(timezone)  

	def moreThan24Hours(self,timeZone, pObj):
		appDate = pObj.consultation_day.available_day
		appTime = pObj.consultation_time.consultation_24hour_start_time
                serverTZ = pytz.timezone(timeZone)
		appDatetime = serverTZ.localize(datetime.datetime.combine(appDate,appTime))
		currentDatetime = self.getCurrentTime(timeZone)
		timedelta = appDatetime - currentDatetime

		if timedelta.days == 0:
			if timedelta.seconds >=0:
				return "no"
			else:
				return "expired"
		elif timedelta.days > 0:
			return "yes"
		else:
			return "expired"

		return timedelta.days

	def saveStripeError(self,user,e):
        	body = e.json_body
        	err  = body['error']
        	stripeError = Stripe_Error(user=user,json_data=body,status=e.http_status,type=err.get('type',""),code=err.get('code',""),param=err.get('param',""),message=err.get('message',""))
        	stripeError.save()

        def post(self, request, *args, **kwargs):
        	if self.request.is_ajax():
                        obj = self.get_object()
                        pObj = obj.professional_purchased_consultation
			dObj = obj.consultation_order_detail
			#before 24 hour
			tz = dObj.consultation_time_zone
			status = self.moreThan24Hours(tz,pObj)
			payment = pObj.payment
			if not status == "expired": 
				if status == "no":
					refundPercent = "50"
					refundedAmount = payment - payment/2
				elif status == "yes":
					refundPercent = "20"
                                        refundedAmount = payment - payment/5
				#Get Stripe
		                if settings.STRIPE_MODE == "TEST":
                		        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
                		elif settings.STRIPE_MODE == "LIVE":
                        		stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY

                        	chargeId = pObj.stripe_charge
				try:
					ch = stripe.Charge.retrieve(chargeId)
					stripeRefundedAmount = int(refundedAmount)*100
					ch.refund(amount=stripeRefundedAmount)
				except stripe.error.InvalidRequestError, e:
					self.saveStripeError(request.user,e)
                        		data = {'status': 'error'}
                        		return self.render_to_json_response(data)
				except stripe.error.AuthenticationError, e:
                                	self.saveStripeError(request.user,e)
                                	data = {'status': 'error'}
                                	return self.render_to_json_response(data)
				except stripe.error.APIConnectionError, e:
                                	self.saveStripeError(request.user,e)
                                	data = {'status': 'error'}
                                	return self.render_to_json_response(data)
				except stripe.error.StripeError, e:
                                	self.saveStripeError(request.user,e)
                                	data = {'status': 'error'}
                                	return self.render_to_json_response(data)
				except Exception, e:
                                	self.saveStripeError(request.user,e)
                                	data = {'status': 'error'}
                                	return self.render_to_json_response(data)

                        	#Change User Purchase from upcoming to cancelled
                        	obj.consultation_status = 'c'
				obj.order = 5
                        	obj.save()
                        	#Change Professionals Purchase info from sold to cancelled 
                        	pObj.consultation_time_status = 'c'
                        	pObj.consultation_day = None
                        	pObj.consultation_time = None
				pObj.refunded_payment = refundedAmount
				pObj.after_refunded_payment = payment - refundedAmount
                        	pObj.save()
				#Send Emails to User, Professional and GN CEO
                        	serverTZ = pytz.timezone(settings.TIME_ZONE)
                        	serverToday = serverTZ.localize(datetime.datetime.now())
                        	c = {
                                	'username': request.user.first_name.title(),
					'user_email': request.user.username,
					'user_phone': request.user.user_account_set.all()[0].user_phone,
					'professional': pObj.professional.professional_full_name,
					'professional_email': pObj.professional.professional_email,
                                        'consultation': dObj.consultation_name,
                                        'duration': dObj.consultation_duration,
					'method': dObj.consultation_method_name,
                                        'date': dObj.consultation_date,
                                        'time': dObj.consultation_time_period,
                                        'timezone': tz,
                                        'link': reverse('users:consultations', args=[request.user.pk]),
                                        'initial_payment': str(payment),
					'refunded_payment': str(pObj.refunded_payment),
					'refund_percent': refundPercent,
                                        'final_payment': str(pObj.after_refunded_payment),
                                	'cancel_date': serverToday
                        	}
				emailObj = Activity.objects.all()[0]
				cancel_subject = emailObj.consultation_cancel_purchase_email_subject
				cancel_message_from = emailObj.consultation_cancel_purchase_from
				user_cancel_to = request.user.username
				professional_cancel_to = pObj.professional.professional_email
				professional_cancel_gn_to = pObj.professional.professional_gn_email
				activity_cancel_to = emailObj.activity_email
				user_cancel_message_html = emailObj.consultation_cancel_purchase_email_message_to_user
				professional_cancel_message_html = emailObj.consultation_cancel_purchase_email_message_to_professional
				activity_cancel_message_html = emailObj.activity_cancel_purchase
				#Send Email to User
                	        t = Template(user_cancel_message_html)
        	                con = Context(c)
	                        message = t.render(con)
                	        msg = EmailMessage(cancel_subject,message,cancel_message_from,[user_cancel_to])
        	                msg.content_subtype = "html"
	                        msg.send()
				#Send Email to Professional
                                t = Template(professional_cancel_message_html)
                                con = Context(c)
                                message = t.render(con)
                                msg = EmailMessage(cancel_subject,message,cancel_message_from,[professional_cancel_to,professional_cancel_gn_to])
                                msg.content_subtype = "html"
                                msg.send()
				#Send Email to Activity
                                t = Template(activity_cancel_message_html)
                                con = Context(c)
                                message = t.render(con)
                                msg = EmailMessage(cancel_subject,message,cancel_message_from,[activity_cancel_to])
                                msg.content_subtype = "html"
                                msg.send()
				############### 
                        	data = {'status': 'cancelled'}
                        	return self.render_to_json_response(data)
			else:
                                data = {'status': 'expired'}
                                return self.render_to_json_response(data)				

        def get_context_data(self, **kwargs):
                context = super(UserConsultationCancelView, self).get_context_data(**kwargs)
                obj = self.object
                pObj = obj.professional_purchased_consultation
                dObj = obj.consultation_order_detail
                #before 24 hour
                tz = dObj.consultation_time_zone
		if obj.consultation_status == "u":
                	status = self.moreThan24Hours(tz,pObj)
		else:
			pass
		context['status'] = status 
                return context
