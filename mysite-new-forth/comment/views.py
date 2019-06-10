from django.shortcuts import render,reverse,redirect
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from .models import *
from comment.forms import CommentForm
from django.http import JsonResponse
def update_comment(request):
   # refer = request.META.get('HTTP_REFERER', reverse('blooger:home'))
    #返回给前端的数据
    data = {}
    comment_form=CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment=Comment()
        comment.user=comment_form.cleaned_data['user']
        comment.text=comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']
        parent=comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root=parent.root if not parent.root is None else parent
            comment.parent=parent
            comment.reply_to=parent.user

        comment.save()
        #return redirect(refer)
        data['status']='SUCCESS'
        data['username']=comment.user.get_nickname_or_username()
        data['comment_time']=comment.comment_time.timestamp()
        data['text']=comment.text
        data['content_type']=ContentType.objects.get_for_model(comment).model
        if not  parent is None:
            data['reply_to']=comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to']=''
        data['pk']=comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status']='ERROR'
        data['message']=list(comment_form.errors.values())[0]
       # return render(request, 'blogger/error.html', {'message': comment_form.errors, 'redirect_to': refer})
    return JsonResponse(data)