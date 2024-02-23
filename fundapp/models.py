from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import localtime, now
from django.utils.text import slugify
from datetime import date
# Create your models here.
class AllFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_campaign')
    sno = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="fundapp/images", default="upload-image")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    campaignType = models.CharField(max_length=100)
    required = models.DecimalField(max_digits=19, decimal_places=10)
    have = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    slug = models.CharField(max_length=130,unique=True, blank=True)
    timeStamp = models.DateField(auto_now_add=True, blank=True)
    
    # to slugify the Campaign
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            index = 1

            while AllFund.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{index}"
                index += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.slug} --by {self.user}'
    
    
class EsewaClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esewa_claim_user')
    phoneNumber = models.CharField(max_length=15)
    receivingAddress = models.CharField(max_length = 200)
    
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
    
class KhaltiClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='khalti_claim_user')
    phoneNumber = models.CharField(max_length=15)
    receivingAddress = models.CharField(max_length = 200)
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
    
class BankClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_claim_user')
    bankName = models.CharField(max_length=180)
    accountNumber = models.CharField(max_length = 150)
    receivingName = models.CharField(max_length = 100)
    accountName = models.CharField(max_length =100)
    receivingAddress = models.CharField(max_length = 200)
    phoneNumber = models.CharField(max_length=15)
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
class Transaction(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user_donator')
    medium = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=3)
    amountReceiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user_receiver')
    campaignTitle = models.ForeignKey(AllFund, on_delete=models.CASCADE, related_name = 'transaction_campaign_title')
    # Address (sai confirmation)
    
    def __str__(self):
        return f'Transaction of -- {self.user}'