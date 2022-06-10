from django.db import models
import uuid
from .apps import PororoConfig
# Create your models here.
from django.utils.text import slugify
from numpy import positive

def generate_unique_slug(klass, field):
    origin_slug = slugify(field, allow_unicode=True)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug

class BuildingData(models.Model):
    building_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, default=uuid.uuid1)
    building_loc = models.CharField(max_length=50)
    building_call = models.CharField(max_length=20)
    #building_time = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.building_name, allow_unicode=True) != self.slug:
                self.slug = generate_unique_slug(BuildingData, self.building_name)
            else:  # create
                self.slug = generate_unique_slug(BuildingData, self.building_name)
            super(BuildingData, self).save(*args, **kwargs)

class ReviewData(models.Model):
    building_name = models.CharField(max_length=50)
    review_content = models.TextField()
    #star_num = models.FloatField()

'''
def save(self, *args, **kwargs):
        self.slug = slugify(self.building_name, allow_unicode=True)
        try:
            return super().save(*args, **kwargs)
        except:
            print(f"the repeated slug is: `{self.slug}`")
            raise 
'''