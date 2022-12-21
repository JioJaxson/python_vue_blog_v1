from django.shortcuts import render, HttpResponse, redirect
from App01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from App01.models import UserInfo
from App01.models import *
from App01.utils.sub_comment import sub_comment_list
from App01.utils.pagination import Pagination
from django.db.models import F


# from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


# 类似router
# Create your views here.
def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    frontend_list = Articles.objects.filter(category=1)[:6]
    backend_list = Articles.objects.filter(category=2)[:6]
    # 分页器
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=1,
        pager_page_count=9
    )
    print(pager.start, pager.end, pager.page_html())
    # 切片
    article_list = article_list[pager.start:pager.end]

    advert_list = Advert.objects.filter(is_show=True)

    return render(request, 'index.html', locals())


# 搜索
def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    tag = request.GET.get('tag', '')
    word = request.GET.getlist('word')
    query_params = request.GET.copy()
    article_list = Articles.objects.filter(title__contains=search_key)
    # 字数搜索
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)
    if tag:
        article_list = article_list.filter(tag__title=tag)
    if order:
        try:
            article_list = article_list.order_by(order)

        except Exception:
            pass


    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7
    )
    print(pager.start, pager.end, pager.page_html())
    # 切片
    article_list = article_list[pager.start:pager.end]
    query_params.urlencode()

    return render(request, 'search.html', locals())


# 文章
def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    article_query.update(look_count=F('look_count')+1) #浏览文章次数加1
    if not article_query:
        return redirect('/')
    article = article_query.first()
    comment_list = sub_comment_list(nid)

    return render(request, 'article.html', locals())

# 新闻
def news(request):
    return render(request, 'news.html')

# 心情
def moods(request):
    # 查询所有头像
    avatar_list = Avatars.objects.all()
    moods_list = Moods.objects.all()
    return render(request, 'moods.html', locals())


# 登陆
def login(request):
    return render(request, 'login.html')


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    # 将random_code返回的验证码写入session
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def sign(request):
    return render(request, 'sign.html')


def logout(request):
    # 注销
    auth.logout(request)
    # 跳转
    return redirect('/')


# 后台
def backstage(request):
    if not request.user.username:
        # 未登录
        return redirect('/')

    return render(request, 'backstage/backstage.html', locals())


# 添加文章
def add_article(request):
    # 拿到所有的分类,标签,封面
    category_list = Articles.category_choice
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid,
        })
    return render(request, 'backstage/add_article.html', locals())


# 修改头像
def edit_avatar(request):
    return render(request, 'backstage/edit_avatar.html', locals())


# 重置密码
def reset_password(request):
    return render(request, 'backstage/reset_password.html', locals())


# 编辑文章
def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    # 拿到所有的分类,标签,封面
    tag_list = Tags.objects.all()
    category_list = Articles.category_choice
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            'url': cover.url.url,
            'nid': cover.nid,
        })

    return render(request, 'backstage/edit_article.html', locals())


def admin_home(request):
    return render(request, 'admin_home.html')
