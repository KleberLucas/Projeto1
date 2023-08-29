from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name

# Create your models here.
class Entertaiment(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    note = models.IntegerField()
    company = models.CharField(max_length=25)
    review = models.TextField()
    review_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='entertainments/cover/%Y/%m/%d/')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, 
                                 blank=True, default=None)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)


class Likers(models.Model):
    post = models.ForeignKey(Entertaiment, on_delete=models.SET_NULL, null=True, 
                                 blank=True, default=None)

    liker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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

