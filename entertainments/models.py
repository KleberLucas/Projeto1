from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

# Create your models here.
class Entertaiment(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    note = models.IntegerField()
    company = models.CharField(max_length=25)
    review = models.TextField()
    review_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='entertainments/cover/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# slug
# title 
# description
# note
# company
# review
# created_at updated_at
# is_published
# author (Relação)
# category (Relação)

