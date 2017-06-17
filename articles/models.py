from django.db import models

#Article Model##############
class Article(models.Model):
        article_title = models.CharField("Title", max_length=100,unique=True)
        article_author = models.ForeignKey("professionals.Professional", verbose_name="Author")
        article_description = models.TextField("Description")
        article_meta_description = models.TextField("Meta Description")
        article_keywords = models.CharField("Keywords for Search",max_length=120,blank=True)
        article_content = models.TextField("Content", help_text="Article HTML Content.")
        article_sources_references = models.TextField("Sources and References",help_text="HTML Content",blank=True)
        article_pubdate = models.DateField("Published Date")
        slug = models.SlugField("Url",max_length=110,help_text="environmental-allergies",unique=True)
        article_small_picture_url = models.CharField("Small Picture Url",max_length=50,help_text="a_small.jpg",default="default1_article_small.jpeg")
        article_medium_picture_url = models.CharField("Medium Picture Url",max_length=50,help_text="a_medium.jpg",blank=True,default="default1_article_medium.jpeg")
        article_large_picture_url = models.CharField("Large Slide Picture Url",max_length=50,help_text="a_large.jpg",blank=True,default="default1_article_large.jpeg")
        STATUS_CHOICES = (
                ('d', 'Draft'),
                ('p', 'Published'),
                ('w', 'Withdrawn'),
        )
        article_status = models.CharField("Status",max_length=1,choices=STATUS_CHOICES,default="d",help_text="Draft, Published, Withdrawn")
        article_hits = models.PositiveIntegerField("Hits",default=0)
        #article right banners for suggestion or future ads
        S_CHOICES = (
                ('y', 'Yes'),
                ('n', 'No'),
        )
        s_article = models.CharField("Suggested Article Allowed?",max_length=1,choices=S_CHOICES,default="n")
        s_consultation = models.CharField("Suggested Consultation Allowed?",max_length=1,choices=S_CHOICES,default="n")
	s_ads = models.CharField("Suggested Ads by Google?",max_length=1,choices=S_CHOICES,default="n")

        class Meta:
                ordering = ('article_title',)

        def hit(self):
                self.article_hits = self.article_hits + 1
                self.save()

        def __unicode__(self):
                return self.article_title

#########################################

#Article Category####################
class Article_Category(models.Model):
        article = models.ForeignKey(Article)
        article_category = models.ForeignKey("categories.Category", related_name='%(app_label)s_%(class)s_related', verbose_name="Category")
        article_category_order = models.PositiveSmallIntegerField("Category Order?", default=1)

        class Meta:
                ordering = ('article_category_order',)
                verbose_name = "Article Category"
                verbose_name_plural = "Article Categories"
                unique_together = (("article", "article_category"),("article", "article_category_order"))

        def __unicode__(self):
                return self.article_category
###################################

#Suggested Article############################ 
class Article_Suggested_Article(models.Model):

        article = models.ForeignKey(Article)
        s_article = models.ForeignKey(Article, related_name='%(app_label)s_%(class)s_related', verbose_name="Article")
        s_article_order = models.PositiveSmallIntegerField("Article Order?",default=1) 

        class Meta:
                ordering = ('s_article_order',)
                verbose_name = "Suggested Article"
                unique_together = (("article", "s_article"),("article", "s_article_order"))

        def __unicode__(self):
                return self.s_article
#####################################

#Suggested Consultation############################
class Article_Suggested_Consultation(models.Model):
        article = models.ForeignKey(Article)
        s_consultation = models.ForeignKey("consultations.Consultation", related_name='%(app_label)s_%(class)s_related', verbose_name="Consultation")
        s_consultation_order = models.PositiveSmallIntegerField("Consultation Order?",default=1)

        class Meta:
                ordering = ('s_consultation_order',)
                verbose_name = "Suggested Consultation"
                unique_together = (("article", "s_consultation"),("article", "s_consultation_order"))

        def __unicode__(self):
                return self.s_consultation
##########################################
