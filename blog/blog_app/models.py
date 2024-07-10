from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_namber = models.CharField(max_length=15)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    address = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='blog_app_user_set',  # Add this line
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='blog_app_user_set',  # Add this line
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self) -> str:
        return self.first_name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def last_img(self):
        return BlogImg.objects.filter(blog__id = self.id).last().img


class BlogImg(models.Model):
    img = models.ImageField(upload_to='blog-img/')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title

class BlogVideo(models.Model):
    video = models.FileField(upload_to='blog-vidos/')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username} -> {self.blog.title}"