from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
class Comment(models.Model):
    #contenttype可以关联任意字段
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text=models.TextField()
    comment_time=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)

    root=models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',null=True,related_name='parent_comment',on_delete=models.CASCADE)
    reply_to=models.ForeignKey(User,null=True,related_name='replies',on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    class Meta:
        ordering=['-comment_time']
