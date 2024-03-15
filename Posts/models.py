from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Tags(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, null=True,blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    tags = models.ManyToManyField(Tags)
    time_to_read = models.IntegerField(default=0)
    trending = models.BooleanField(default=False)
    hero = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def get_posted_info(self):
        return f"Creado por {self.author} - {self.time_to_read} min. de lectura"

class ContactForm(models.Model):
    STATUS = (
        ("Read", "Leido"),
        ("Unread", "No leido"),
        ("Answered", "Respondido")
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Unread")

    def __str__(self):
        return f"Mensaje de {self.name} - {self.email}"