from django.shortcuts import render
from django.db.models import Q
from blog.models import Blog, BlogType

def blog_list(request, blog_type_slug):
    BLOG_PER_PAGE = 10
    offset = int(request.GET.get('page', default=1))

    start = max((offset - 1) * BLOG_PER_PAGE, 0)
    end = start + BLOG_PER_PAGE

    blog_types = BlogType.objects.all()
    current_blog_type = BlogType.objects.get(slug=blog_type_slug)
    blogs = current_blog_type.blog_set.all()[start:end]
    total_blogs = current_blog_type.blog_set.count()

    context = {
        "blog_types": blog_types,
        "current_blog_type": current_blog_type,
        "blog_type_slug": blog_type_slug,
        "blogs": blogs,
        "current_page": offset,
        "total_page": total_blogs // BLOG_PER_PAGE + 1
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_type_slug, blog_slug):
    blog = Blog.objects.get(Q(slug=blog_slug) & Q(blog_type__slug=blog_type_slug))
    
    context = {
        "blog": blog
    }

    return render(request, 'blog/blog_detail.html', context)