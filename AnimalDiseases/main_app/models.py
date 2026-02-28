from django.db import models
from regst.models import User

# Create your models here.

class UsersActions(models.Model):
    """
        Model that will store users request of each user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.CharField(max_length=30)
    result = models.TextField(default='Healthy')
    prediction_date = models.DateTimeField(auto_now_add=True)
