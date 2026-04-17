from django.db import models

# Create your models here.
class AddBlog(models.Model):
    Image = models.ImageField(upload_to='Blogs/')
    Name = models.CharField(max_length=100)
    Title = models.CharField(max_length=300)
    Summery = models.TextField()
    Time = models.DateTimeField(auto_now=True)
    Up_time = models.DateTimeField(auto_now_add=True)




class UserDetails(models.Model):
    Email = models.EmailField(max_length=100, default=None)
    Username = models.CharField(max_length=100, default=None)
    Password = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = 'UserDetails'
