from django.shortcuts import render, reverse, redirect
from .forms import *
from read_statistic.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.core.cache import cache
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from blog.models import *
import datetime


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(content_type=blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    # seven_hot_data=get_7_days_hot_blogs()
    # 获取7天热门博客的缓存数据
    hot_blog_for_seven_days = cache.get('hot_blog_for_seven_days')
    if hot_blog_for_seven_days is None:
        hot_blog_for_seven_days = get_7_days_hot_blogs()
        cache.set('hot_blog_for_seven_days', hot_blog_for_seven_days, 3600)
    context = {'read_nums': read_nums, 'dates': dates,
               'today_hot_data': today_hot_data,
               'yesterday_hot_data': yesterday_hot_data,
               'seven_hot_data': hot_blog_for_seven_days
               }
    return render(request, 'blogger/home.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.clean()
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse("blog:home")))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'blogger/login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.clean_username()
            email = reg_form.clean_email()
            password=reg_form.clean_password_again()
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse("blooger:home")))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'blogger/register.html', context)
