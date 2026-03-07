from typing import Any
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views import View

from .models import UserReview, Post
from .forms import UserReviewForm


# Create your views here.
class HomePageView(ListView):
    template_name = "blog/home_page.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-date"]
    
    def get_queryset(self):
        query_set= super().get_queryset()
        data = query_set[:3]
        return data

   
class PostView(ListView):
    model = Post
    template_name = "blog/posts.html"
    context_object_name = "posts"
    ordering = ["-date"]
    

class BlogPageView(View):
    def check_readlater(self, request, post_id):
        stored_page = request.session.get("read_later")
        if stored_page != None:
            in_later = post_id in stored_page
        else:
            in_later = False

        return in_later

    def get(self, request, slug):
        post_detail = get_object_or_404(Post, slug=slug)
        tags = post_detail.tags.all()
        form = UserReviewForm()
        comments = post_detail.comment.all()
        later = self.check_readlater(request, post_detail.id)
        return render(request, "blog/topic.html", {"post_details":post_detail, 
                                                   "tags":tags, "form":form, 
                                                   "comments":comments,"later":later,})
    
    def post(self, request, slug):
        form_value = request.POST
        post_detail = get_object_or_404(Post, slug=slug)
        tags = post_detail.tags.all()
        form = UserReviewForm(form_value)

        if form.is_valid():
            form = form.save(commit=False)
            form.post = post_detail
            form.save()
            return HttpResponseRedirect(reverse("BlogPage", args=[slug]))
        
        else:
            later =self.check_readlater(request, post_detail.id)
            comments = post_detail.comment.all()
            return render(request, "blog/topic.html", {"post_details":post_detail, 
                                                       "tags":tags, "form":form, 
                                                       "comments":comments,
                                                       "later":later,})


class ReadLaterView(View):
    def get(self, request):
        later_session = request.session.get("read_later")
        context = {}

        if later_session == None or later_session == []:
            context["later"] = []
            context["exist"] = False

        else:
            context["later"]= Post.objects.filter(id__in=later_session)
            context["exist"] = True

        return render(request, "blog/read-later.html", context)

    def post(self, request):
        later_session = request.session.get("read_later")

        if later_session == None :
            later_session = []

        if int(request.POST["post id"]) not in later_session:
            later_session.append(int(request.POST["post id"]))

        else:
            later_session.remove(int(request.POST["post id"]))

        request.session["read_later"] = later_session

        return HttpResponseRedirect("/")





# function based views
def home_page(request):
    sorted_post = Post.objects.order_by("-date")[:3]
    return render(request, "blog/home_page.html", {"posts":sorted_post})

def post(request):
    sorted_post = Post.objects.order_by("date")
    return render(request, "blog/posts.html", {"posts":sorted_post})

def blog_page(request, slug):
    post_detail = get_object_or_404(Post, slug=slug)
    tags = post_detail.tags.all()
    return render(request, "blog/topic.html", {"post_details":post_detail, "tags":tags})
    """try:
        #next(post for post in titles if post[slug]==title)
        ww=""
        for i in posts:
            post_details = i["slug"]
            if titles==post_details:
                return render(request, "blog/topic.html", {"post_details":i})
            else:
                ww= None
        if ww==None:
            raise Exception
    except Exception:
        return render(request, "404.html")"""
    