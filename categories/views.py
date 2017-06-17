import json
from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from categories.models import Category
from articles.models import Article_Category
from consultations.models import Consultation_Category
from django.utils.text import Truncator
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm

class IndexView(ListView, FormView):
        template_name = 'categories/categoryIndexPage.html'
        context_object_name = 'latest_category_list'
        form_class = AuthenticationForm
        paginate_by = 100

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
        	if self.sortBy:
                	if self.sortBy == "p":
                        	return Category.objects.order_by('-category_hits')
                        else:
                                return Category.objects.order_by('category_name')
                else:
                                return Category.objects.order_by('category_name')

        def get_context_data(self, **kwargs):
                context = super(IndexView, self).get_context_data(**kwargs)
                context['form'] = self.get_form(self.form_class)
                context['url'] = self.url
                context['sortBy'] = self.sortBy
                return context

class CategoryPageView(FormView, DetailView):
        model = Category
        template_name = 'categories/categoryPage.html'
        form_class = AuthenticationForm

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
                return super(CategoryPageView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(CategoryPageView, self).get_context_data(**kwargs)
                self.object.hit()
                context['form'] = self.get_form(self.form_class)
                context['articles']= Article_Category.objects.filter(article_category=self.object,article__article_status="p")
                context['consultations']= Consultation_Category.objects.filter(consultation_category=self.object,consultation__consultation_status="p")
                #if self.user.is_superuser:
                	#context['suggestedArticles']= self.object.article_suggested_article_set.all()
                #else:
                       	#context['suggestedArticles']= self.object.article_suggested_article_set.filter(s_article__article_status="p")
                return context

