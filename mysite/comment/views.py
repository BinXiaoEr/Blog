from comment.forms import CommentForm
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import *
from django.conf import settings
def update_comment(request):
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
        #发送邮件通知
        comment.send_mail()
        #返回数据
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