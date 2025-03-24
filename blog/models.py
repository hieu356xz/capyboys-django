from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=511)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    cover_img = models.ImageField(max_length=511, upload_to="blog/", blank=True, null=True)
    blog_type = models.ForeignKey('BlogType', on_delete=models.CASCADE)
    publish_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title
    
class BlogType(models.Model):
    name = models.CharField(max_length=511)
    slug = models.SlugField(max_length=255, unique=True)
    blogs = models.ManyToManyField('Blog', related_name='blog_types')

    def __str__(self):
        return self.name