from django.db import models

from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.text import slugify
import uuid


class MovieManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(MovieManager, self).filter(draft=False)


def upload_location(instance, filename):
    MovieModel = instance.__class__
    obj_exist = MovieModel.objects.order_by("id").last()
    new_id = 1
    if obj_exist: 
        new_id = obj_exist.id + 1


    return "%s%s"%(new_id,filename)


class MovieModel(models.Model):

    CHOICES = {
        ('Action','Action'),
        ('Animation','Animation'),
        ('Drama','Drama'),
        ('Crime','Crime'),
    }
    title = models.TextField()
    description = models.TextField()
    cover = models.ImageField(upload_to=upload_location, blank=True, null=True)
    realesedYear = models.TextField()
    RunningTime = models.TextField()
    Age = models.IntegerField()
    genre = models.CharField(max_length=10, choices=CHOICES)
    movie = models.FileField(upload_to=upload_location, blank=True,null=True)

    objects = MovieManager()

    def create_slug(instance, new_slug=None):
        slug = slugify(instance.title)
        if new_slug is not None:
            slug = new_slug

            qs = MovieModel.objects.filter(slug=slug).order_by('-id')
            exits = qs.exists()

            if exits:
                new_slug = "%s-%s" %(slug, qs.first().id)
            return slug


