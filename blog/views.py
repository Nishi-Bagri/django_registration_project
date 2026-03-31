from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Blog, Like
from users.models import CustomUser
from django.contrib import messages
from .models import SiteSettings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from blog.models import Blog, Comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommentForm

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request,*args,**kwargs):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('login')
        
        user = CustomUser.objects.get(id=user_id)

        if user.role != 'admin':
            return HttpResponse("Access Denied")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def blog_list(request):
    query = request.GET.get('q')

    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        blogs = Blog.objects.all()

    # ✅ Fix like state
    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)
    for blog in blogs:
        if user_id:
            blog.is_liked = Like.objects.filter(
                user_id=user_id,
                blog=blog
            ).exists()
        else:
            blog.is_liked = False
        
    return render(request, 'blog/blog_list.html', {'blogs': blogs, 'user' : user })

def create_blog(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')
    

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary')

        print("SUMMARY:", summary)

        user = CustomUser.objects.get(id=user_id)

        Blog.objects.create(
            user=user,
            title=title,
            content=content,
            summary = summary
        )

        return redirect('my_blogs')
    
    return render(request, 'blog/create_blog.html')


def my_blogs(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')
    
    blogs = Blog.objects.filter(user_id=user_id)

    return render(request, 'blog/my_blogs.html',{'blogs':blogs})


def edit_blog(request, id):
    
    blog = get_object_or_404(Blog, id=id)

    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(id=user_id)

    if blog.user.id != user.id and user.role != 'admin':
        return HttpResponse("You can not edit this blog")    
 

    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.summary = request.POST.get('summary')
        blog.save()

        return redirect('blog_list')
    
    return render(request, 'blog/edit_blog.html',{'blog':blog})

def delete_blog(request, id):

    blog = get_object_or_404(Blog, id=id)

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    # Permission check
    if blog.user.id != user.id and user.role != 'admin':
        return HttpResponse("You cannot delete this blog")

    if request.method == "POST":
        blog.delete()

        if user.role == 'admin':
            return redirect('admin_blog_list')
        else:
            return redirect('my_blogs')

    return HttpResponse("Invalid request")


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    user_id = request.session.get('user_id')
    user = None

    if user_id:
        user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if not user:
            return redirect('login')

        if content:
            Comment.objects.create(
                user=user,   # ✅ FIXED
                blog=blog,
                content=content
            )

        return redirect('blog_detail', id=id)

    comments = Comment.objects.filter(blog=blog).order_by('-id')

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'user': user   # ✅ VERY IMPORTANT
    })

@admin_required
def pending_blogs(request):
    blogs = Blog.objects.filter(status='pending')

    return render(request, 'blog/pending_blogs.html', {'blogs': blogs})

@admin_required
def approve_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    blog.status = 'approved'
    blog.save()

    return redirect('pending_blogs')


@admin_required
def reject_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        reason = request.POST.get('reason')

        blog.status = 'rejected'
        blog.rejection_reason = reason
        blog.save()

        messages.success(request,"Blog Rejected")
        return redirect('admin_dashboard')
    
    return HttpResponse("Invalid Request")

@admin_required
def admin_dashboard(request):

    total_blogs = Blog.objects.count()
    pending_blogs = Blog.objects.filter(status = 'pending').count()
    approved_blogs = Blog.objects.filter(status = 'approved').count()
    rejected_blogs = Blog.objects.filter(status = 'rejected').count()

    context = {
        'total_blogs': total_blogs,
        'pending_blogs': pending_blogs,
        'approved_blogs': approved_blogs,
        'rejected_blogs': rejected_blogs
    }

    return render(request, 'dashboards/admin_dashboard.html', context)

@admin_required
def admin_blog_list(request):

    blogs = Blog.objects.all().order_by('-created_at')

    return render(request, 'blog/admin_blog_list.html', {'blogs':blogs})

@admin_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})

@admin_required
def upload_logo(request):

    settings = SiteSettings.objects.first()

    if request.method == "POST":

        print(request.FILES)
        
        logo = request.FILES.get('logo')  # 👈 THIS IS KEY

        if logo:  # 👈 ADD THIS CHECK
            if settings:
                settings.logo = logo
                settings.save()
            else:
                SiteSettings.objects.create(logo=logo)

            return redirect('upload_logo')  # reload page

    return render(request, 'blog/upload_logo.html', {'settings': settings})

def toggle_like(request, blog_id):

    if request.method == "POST":

        # ✅ FIXED AUTH CHECK
        if 'user_id' not in request.session:
            return JsonResponse({'error': 'login required'}, status=403)

        user_id = request.session.get('user_id')
        user = CustomUser.objects.get(id=user_id)

        blog = Blog.objects.get(id=blog_id)

        like = Like.objects.filter(user=user, blog=blog).first()

        if like:
            like.delete()
            liked = False
        else:
            Like.objects.create(user=user, blog=blog)
            liked = True

        count = Like.objects.filter(blog=blog).count()

        return JsonResponse({
            'liked': liked,
            'count': count
        })

    return JsonResponse({'error': 'invalid request'}, status=400)

def search_suggestions(request):
    query = request.GET.get('q', '')
    print("QUERY:",query)
    
    if query:
        blogs = Blog.objects.filter(title__icontains=query)[:5]
        print("RESULT:",blogs)
        suggestions = [blog.title for blog in blogs]
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})

@login_required
def edit_comment(request, comment_id):
    # Get the comment
    comment = get_object_or_404(Comment, id=comment_id)

    # Get logged-in user from session
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    # ✅ Permission check (VERY IMPORTANT)
    if comment.user != user:
        return HttpResponse("You cannot edit this comment")

    # Handle form submission
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            comment.content = content
            comment.save()

        return redirect('blog_detail', id=comment.blog.id)

    # Show edit form
    return render(request, 'blog/edit_comment.html', {
        'comment': comment
    })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    # ✅ Permission check
    if comment.user != user:
        return HttpResponse("You cannot delete this comment")

    # ✅ Only allow POST (important for security)
    if request.method == "POST":
        blog_id = comment.blog.id
        comment.delete()
        return redirect('blog_detail', id=blog_id)

    return HttpResponse("Invalid request")