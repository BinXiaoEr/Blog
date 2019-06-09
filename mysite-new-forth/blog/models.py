from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from read_statistic.models import *
from django.contrib.contenttypes.fields import GenericRelation
#from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField
class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpand):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = MDTextField()
    read_details=GenericRelation(ReadDetail)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-create_time']
