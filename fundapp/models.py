from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AllFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_campaign')
    sno = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="fundapp/images", default="upload-image")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    required = models.DecimalField(max_digits=19, decimal_places=10)
    have = models.DecimalField(max_digits=19, decimal_places=10)
    
    def __str__(self):
        return f'{self.title} --by {self.user}'