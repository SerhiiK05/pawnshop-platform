from django.contrib import admin

from pawnshop.models import ReferralBonus, Item, Loan, Payment


admin.site.register(Item)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(ReferralBonus)

