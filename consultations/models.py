from django.db import models

#Consultation Model##############
class Consultation(models.Model):
        consultation_title = models.CharField("Title", max_length=100,unique=True)
        consultation_professional = models.ForeignKey("professionals.Professional", verbose_name="Professional")
        consultation_description = models.TextField("Description")
        consultation_meta_description = models.TextField("Meta Description")
        consultation_keywords = models.CharField("Keywords for  Search", max_length=100,blank=True)
        consultation_content = models.TextField("Consultation Content", help_text="HTML Content")
        slug = models.SlugField("Url",max_length=110,help_text="female-hormone-balance",unique=True)
        consultation_small_picture_url = models.CharField("Small Picture Url",max_length=50,help_text="a_small.jpg",default="default1_consultation_small.jpeg")
        consultation_medium_picture_url = models.CharField("Medium Picture Url",max_length=50,help_text="a_medium.jpg",blank=True,default="default1_consultation_medium.jpeg")
        consultation_large_picture_url = models.CharField("Large Picture Url",max_length=50,help_text="a_large.jpg",blank=True,default="default1_consultation_large.jpeg")
        consultation_pubdate = models.DateField("Published Date")
        consultation_hits = models.PositiveIntegerField("Hits",default=0)
        STATUS_CHOICES = (
                ('d', 'Draft'),
                ('p', 'Published'),
                ('w', 'Withdrawn'),
        )
        consultation_status = models.CharField("Status",max_length=1,choices=STATUS_CHOICES,default="d",help_text="Draft, Published, Withdrawn")
        S_CHOICES = (
                ('y', 'Yes'),
                ('n', 'No'),
        )
        s_article = models.CharField("Suggested Article Allowed?",max_length=1,choices=S_CHOICES,default="n")
        s_consultation = models.CharField("Suggested Consultation Allowed?",max_length=1,choices=S_CHOICES,default="n")
        s_ads = models.CharField("Suggested Ads by Google?",max_length=1,choices=S_CHOICES,default="n")

        class Meta:
                ordering = ('consultation_title',)

        def hit(self):
                self.consultation_hits = self.consultation_hits + 1
                self.save()

        def __unicode__(self):
                return self.consultation_title
##############################################

#Consultation Category####################
class Consultation_Category(models.Model):
        consultation = models.ForeignKey(Consultation)
        consultation_category = models.ForeignKey("categories.Category", related_name='%(app_label)s_%(class)s_related', verbose_name="Category")
        consultation_category_order = models.PositiveSmallIntegerField("Category Order?",default=1)

        class Meta:
                ordering = ('consultation_category_order',)
                verbose_name = "Consultation Category"
                verbose_name_plural = "Consultation Categories"
                unique_together = (("consultation", "consultation_category"),("consultation", "consultation_category_order"))

        def __unicode__(self):
                return self.consultation
###################################

#Suggested Consultation############################
class Consultation_Suggested_Consultation(models.Model):
        consultation = models.ForeignKey(Consultation)
        s_consultation = models.ForeignKey(Consultation, related_name='%(app_label)s_%(class)s_related', verbose_name="Consultation")
        s_consultation_order = models.PositiveSmallIntegerField("Consultation Order?",default=1)

        class Meta:
                ordering = ('s_consultation_order',)
                verbose_name = "Suggested Consultation"
                unique_together = (("consultation", "s_consultation"),("consultation", "s_consultation_order"))

        def __unicode__(self):
                return self.s_consultation
##########################################

#Suggested Article############################ 
class Consultation_Suggested_Article(models.Model):
        consultation = models.ForeignKey(Consultation)
        s_article = models.ForeignKey("articles.Article", related_name='%(app_label)s_%(class)s_related', verbose_name="Article")
        s_article_order = models.PositiveSmallIntegerField("Article Order?",default=1)

        class Meta:
                ordering = ('s_article_order',)
                verbose_name = "Suggested Article"
                unique_together = (("consultation", "s_article"),("consultation", "s_article_order"))

        def __unicode__(self):
                return self.s_article
#####################################
