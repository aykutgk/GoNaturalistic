import json
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView
from home.models import Gonaturalistic, Slides, Popular_Articles, Popular_Consultations
from django.contrib.auth.forms import AuthenticationForm
from home.forms import ContactusForm
from django.core.mail import EmailMessage, BadHeaderError
import datetime
import random
from itertools import chain

class JSONResponseMixin(object):
        def render_to_json_response(self, context, **response_kwargs):
                data = json.dumps(context)
                response_kwargs['content_type'] = 'application/json'
                return HttpResponse(data, **response_kwargs)

class HomePageView(FormView):
        template_name = 'home/homePageIndex.html'
        form_class = AuthenticationForm

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
		return super(HomePageView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(HomePageView, self).get_context_data(**kwargs)
		Gonaturalistic.objects.all()[0].hit()
                context['form'] = self.get_form(self.form_class)

		if self.user.is_authenticated():
			context['slides'] = Slides.objects.exclude(custom_only_for='g')
		else:
			context['slides'] = Slides.objects.exclude(custom_only_for='m')

		context['gnTitle'] = Gonaturalistic.objects.all()[0].meta_title
		context['gnDescription'] = Gonaturalistic.objects.all()[0].meta_description
		popularArticlesCount = Popular_Articles.objects.all().count()
		popularConsultationCount = Popular_Consultations.objects.all().count()
		randomNumber = random.randint(0,popularArticlesCount)
		if randomNumber <= (popularArticlesCount - 4):
			nextNumber = randomNumber+4
			context['popularArticles'] = Popular_Articles.objects.all()[randomNumber:nextNumber]
		else:
			nextNumber = randomNumber + 4 - popularArticlesCount
			context['popularArticles'] = list(chain(Popular_Articles.objects.all()[randomNumber:popularArticlesCount],Popular_Articles.objects.all()[:nextNumber]))
		if randomNumber <= (popularConsultationCount-4):
			nextNumber = randomNumber+4
			context['popularConsultations'] = Popular_Consultations.objects.all()[randomNumber:nextNumber]			
		else:
			nextNumber = randomNumber + 4 - popularConsultationCount
			context['popularConsultations'] = list(chain(Popular_Consultations.objects.all()[randomNumber:popularConsultationCount],Popular_Consultations.objects.all()[:nextNumber]))
                context['url'] = self.url
                return context

class TermsPageView(FormView):
        template_name = 'home/termsPage.html'
        form_class = AuthenticationForm

        def get_context_data(self, **kwargs):
                context = super(TermsPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
	        context['terms'] = Gonaturalistic.objects.all()[0].terms
                return context

class PrivacyPageView(FormView):
        template_name = 'home/privacyPage.html'
        form_class = AuthenticationForm

        def get_context_data(self, **kwargs):
                context = super(PrivacyPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['privacy'] = Gonaturalistic.objects.all()[0].privacy_policy
                return context

class PoliciesPageView(FormView):
        template_name = 'home/policiesPage.html'
        form_class = AuthenticationForm

        def get_context_data(self, **kwargs):
                context = super(PoliciesPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['policies'] = Gonaturalistic.objects.all()[0].policies
                return context

class AboutusPageView(FormView):
        template_name = 'home/aboutusPage.html'
        form_class = AuthenticationForm

        def get_context_data(self, **kwargs):
                context = super(AboutusPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['aboutus'] = Gonaturalistic.objects.all()[0].about_us
                return context

class HelpcenterPageView(FormView):
        template_name = 'home/helpcenterPage.html'
        form_class = AuthenticationForm

        def get_context_data(self, **kwargs):
                context = super(HelpcenterPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['helpcenter'] = Gonaturalistic.objects.all()[0].help_center
                return context

class ContactusPageView(JSONResponseMixin,FormView):
        template_name = 'home/contactusPage.html'
        form_class = AuthenticationForm

        def post(self, request, *args, **kwargs):
                form = ContactusForm(request.POST)
		if request.user.is_authenticated():
			to = Gonaturalistic.objects.all()[0].contact_us_member_to
		else:
			to = Gonaturalistic.objects.all()[0].contact_us_guest_to
                if form.is_valid():
			sender = form.cleaned_data['sender']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			from_email = 'noreply@gonaturalistic.com'
			timeNow = datetime.datetime.now().strftime("%B %d, %Y at %H:%M")
			html = '<table>'
			html += '<tr><td style="width:100px;"><strong>Sender:</strong></td><td><strong>'+sender+'</strong></td></tr>'
			html += '<tr><td valign="top" style="width:100px;"><strong>Message:</strong></td><td>'+message+'</td></tr>'
			html += '<tr><td style="width:100px;"><strong>Sent Date:</strong></td><td>'+timeNow+'</td></tr>'
			html += '</table>'
			try:
				msg = EmailMessage(subject,html,from_email,[to])
				msg.content_subtype = "html"
				msg.send()
				return self.render_to_json_response({'status':'ok'})
			except BadHeaderError:
				return self.render_to_json_response({'status':'fail'})
		else:									
			return self.render_to_json_response({'status':'fail'})

        def get_context_data(self, **kwargs):
                context = super(ContactusPageView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
		context['contactus_form'] = ContactusForm
                context['contactus'] = Gonaturalistic.objects.all()[0].contact_us_content
                return context

