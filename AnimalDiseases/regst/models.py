from django.db import models

# Create your models here.
class User(models.Model):
    """
        User model.
        For more information about creating models and working with them check Django documentation.
    """

    username = models.CharField(max_length=50, unique=True)
    us_password = models.TextField()
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    agent = models.TextField()
    identifier = models.CharField(max_length=15, default='010' * 5)