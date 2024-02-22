from django.contrib import admin
from .models import AllFund, EsewaClaim, KhaltiClaim, BankClaim

# Register your models here.
admin.site.register(AllFund)
admin.site.register(EsewaClaim)
admin.site.register(KhaltiClaim)
admin.site.register(BankClaim)