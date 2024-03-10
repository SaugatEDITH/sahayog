from django.contrib import admin
from .models import AllFund, EsewaClaim, KhaltiClaim, BankClaim, Transaction, Usermessage

# Register your models here.
admin.site.register(AllFund)
admin.site.register(EsewaClaim)
admin.site.register(KhaltiClaim)
admin.site.register(BankClaim)
admin.site.register(Transaction)
admin.site.register(Usermessage)