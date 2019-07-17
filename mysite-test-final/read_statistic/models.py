from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')

class ReadDetail(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    objecxt_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)


class ReadNumExpand():
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(self)
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0
# #         # 如果查询没有值返回的是抛出异常 当没有值时返回0
# #         # Rlog有ReadNum的小写其具有的方法 对象.get_read_num就可以获得其值



