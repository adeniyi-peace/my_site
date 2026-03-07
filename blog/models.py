from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Author(models.Model):
    first_name = models.CharField( max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField( max_length=254)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


    
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"
    
    

class Post(models.Model):
    title = models.CharField( max_length=250)
    excerpt = models.CharField(max_length=250)
    image_name = models.ImageField(upload_to="blog image", height_field=None, width_field=None, max_length=None, null=True)
    date = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    

    def __str__(self):
        return f"{self.title}"
    
    
class UserReview(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField( max_length=254)
    usercomment = models.TextField()
    post = models.ForeignKey(Post,  on_delete=models.CASCADE, editable=False, related_name="comment")