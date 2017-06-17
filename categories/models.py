from django.db import models

#Category Model##############
class Category(models.Model):
        category_name = models.CharField(max_length=40, verbose_name="Name",unique=True)
	category_description = models.CharField("Description",max_length=100)
        category_style = models.CharField("Style", max_length=40,default="primary")
	slug = models.SlugField("Url",max_length=50,help_text="allergies",unique=True)
        category_hits = models.PositiveIntegerField("Hits",default=0)

        class Meta:
                ordering = ('category_style',)

        def hit(self):
                self.category_hits = self.category_hits + 1
                self.save()

        def __unicode__(self):
                return self.category_name
##########################################
