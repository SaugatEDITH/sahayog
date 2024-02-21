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
    
    
class EsewaClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='esewa_claim_user')
    phoneNumber = models.CharField(max_length=15)
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
    
class KhaltiClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='khalti_claim_user')
    phoneNumber = models.CharField(max_length=15)
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
    
class BankClaim(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_claim_user')
    bankName = models.CharField(max_length=180)
    accountNumber = models.CharField(max_length = 150)
    ReceivingName = models.CharField(max_length = 100)
    # phoneNumber (sai confirmation)
    
    def __str__(self):
        return f'Caimed by -- {self.user}'
    
class Transaction(models.Model):
    sno = models.AutoField(primary_key=True)
    amountDonator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user_donator')
    medium = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=3)
    amountReceiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user_receiver')
    campaignTitle = models.ForeignKey(AllFund, on_delete=models.CASCADE, related_name = 'transaction_campaign_title')
    # Address (sai confirmation)
    
    def __str__(self):
        return f'Transaction of -- {self.user}'