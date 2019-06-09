from django.shortcuts import render,reverse,redirect
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from .models import *
from comment.forms import CommentForm
from django.http import JsonResponse
def update_comment(request):
    refer = request.META.get('HTTP_REFERER', reverse('blooger:home'))
    #返回给前端的数据
    data = {}
    comment_form=CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment=Comment()
        comment.user=comment_form.cleaned_data['user']
        comment.text=comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']
        comment.save()
        #return redirect(refer)
        data['status']='SUCCESS'
        data['username']=comment.user.username
        data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M')
        data['text']=comment.text
    else:
        data['status']='ERROR'
        data['message']=list(comment_form.errors.values())[0]
       # return render(request, 'blogger/error.html', {'message': comment_form.errors, 'redirect_to': refer})
    return JsonResponse(data)