from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from post.models import Post
from post.forms import Form, SignUpForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home_page(request):
    return HttpResponse('<h1> Home </h1>')


def post_list(request):
    queryset = Post.objects.order_by('-id')
    paginator = Paginator(queryset, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        'title': 'Post list',
        'object_list': queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'post_list.html', context)


def post_create(request):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = Form(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Post created!!!')
         

    context = {
        'title': 'Post create',
        'form': form
    }
    return render(request, 'create.html', context)


def post_update(request, id):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = Form(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href = '#'>Post created!!!</a> ", extra_tags='safe_html')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': 'Post update',
        'form': form
    }
    return render(request, 'create.html', context)


def post_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect('post:post_list')


def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        'title': 'Post detail',
        'object': instance
    }
    return render(request, 'detail.html', context)




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post:post_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})







