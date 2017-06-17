import json
from django.http import StreamingHttpResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from articles.models import Article
from django.utils.text import Truncator
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm

class JSONResponseMixin(object):
        def render_to_json_response(self, context, **response_kwargs):
                data = json.dumps(context)
                response_kwargs['content_type'] = 'application/json'
                return HttpResponse(data, **response_kwargs)

class IndexView(ListView, FormView):
        template_name = 'articles/articleIndexPage.html'
        context_object_name = 'latest_article_list'
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
					return Article.objects.order_by('-article_hits')
				else:
					return Article.objects.order_by('-article_pubdate')
			else:
				return Article.objects.order_by('-article_pubdate')
		else:
			if self.sortBy:
                                if self.sortBy == "p":
                                        return Article.objects.filter(article_status="p").order_by('-article_hits')
                                else:
                                        return Article.objects.filter(article_status="p").order_by('-article_pubdate')
                        else:
				return Article.objects.filter(article_status="p").order_by('-article_pubdate')

	def get_context_data(self, **kwargs):
     		context = super(IndexView, self).get_context_data(**kwargs)
		context['form'] = self.get_form(self.form_class)
    		context['url'] = self.url
		context['sortBy'] = self.sortBy
		return context


class ArticlePageView(JSONResponseMixin, FormView, DetailView):
        model = Article
        template_name = 'articles/articlePage.html'
        form_class = AuthenticationForm

        def get(self, request, *args, **kwargs):
                self.user = request.user
                self.url = request.path
                return super(ArticlePageView, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
                context = super(ArticlePageView, self).get_context_data(**kwargs)
                self.object.hit()
                context['form'] = self.get_form(self.form_class)
                context['articleCategories']= self.object.article_category_set.all()
                if self.object.s_article == "y":
                        if self.user.is_superuser:
                                context['suggestedArticles']= self.object.article_suggested_article_set.all()
                        else:
                                context['suggestedArticles']= self.object.article_suggested_article_set.filter(s_article__article_status="p")
                if self.object.s_consultation == "y":
                        if self.user.is_superuser:
                                context['suggestedConsultations']= self.object.article_suggested_consultation_set.all()
                        else:
                                context['suggestedConsultations']= self.object.article_suggested_consultation_set.filter(s_consultation__consultation_status="p")
                return context

