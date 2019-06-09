from django.shortcuts import render,reverse,redirect
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from .models import *
def update_comment(request):
    user=request.user
    refer = request.META.get('HTTP_REFERER', reverse('blog:home'))
    #数据检查
    if not user.is_authenticated:
        return render(request, 'blogger/error.html', {'message': '用户未登录', 'redirect_to': refer})
    text=request.POST.get('text','')
    if text=="":
        return render(request, 'blogger/error.html', {'message': '评论内容为空', 'redirect_to': refer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        # 获取从前端传递评论的信息
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'blogger/error.html', {'message': '评论对象不存在', 'redirect_to': refer})
    #检查通过,保存数据
    comment=Comment()
    comment.user=user
    comment.text=text
    comment.content_object=model_obj
    comment.save()
    return redirect(refer)
