import json
from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from professionals.models import Professional
from articles.models import Article
from consultations.models import Consultation
from django.contrib.auth.forms import AuthenticationForm

class IndexView(ListView, FormView):
        template_name = 'professionals/professionalIndexPage.html'
        context_object_name = 'professional_list'
        form_class = AuthenticationForm
        paginate_by = 5

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
                perPage = request.GET.get('perPage', None)
                if perPage:
                        self.paginate_by = int(perPage)
                else:
                        pass
                return super(IndexView, self).get(request, *args, **kwargs)

        def get_queryset(self):
                return Professional.objects.all().order_by('professional_full_name')

        def get_context_data(self, **kwargs):
                context = super(IndexView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['url'] = self.url
                return context

class ProfessionalPageView(FormView, DetailView):
        model = Professional
        template_name = 'professionals/professionalPage.html'
        form_class = AuthenticationForm

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
                return super(ProfessionalPageView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(ProfessionalPageView, self).get_context_data(**kwargs)
                self.object.hit()
                context['form'] = self.get_form(self.form_class)
                if self.object.s_article == "y":
                        if self.user.is_superuser:
                                #context['suggestedArticles']= self.object.professional_suggested_article_set.all()
				context['articles']= Article.objects.filter(article_author=self.object).order_by('article_hits')[:12]
                        else:
                                #context['suggestedArticles']= self.object.professional_suggested_article_set.filter(s_article__article_status="p")
                                context['articles']= Article.objects.filter(article_author=self.object,article_status="p").order_by('article_hits')[:12]
                if self.object.s_consultation == "y":
                        if self.user.is_superuser:
                                #context['suggestedConsultations']= self.object.professional_suggested_consultation_set.all()
				context['consultations']= Consultation.objects.filter(consultation_professional=self.object).order_by('consultation_hits')[:12]
                        else:
                                #context['suggestedConsultations']= self.object.professional_suggested_consultation_set.filter(s_consultation__consultation_status="p")
                                context['consultations']= Consultation.objects.filter(consultation_professional=self.object,consultation_status="p").order_by('consultation_hits')[:12]
                return context
