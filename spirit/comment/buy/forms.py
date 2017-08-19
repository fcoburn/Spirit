# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CommentBuy
from spirit.user.models import UserProfile


class BuyForm(forms.ModelForm):

    class Meta:
        model = CommentBuy
        fields = []

    def __init__(self, user=None, comment=None, amount=None, *args, **kwargs):
        super(BuyForm, self).__init__(*args, **kwargs)
        self.user = user
        self.comment = comment
        self.amount = amount

    def clean(self):
        cleaned_data = super(BuyForm, self).clean()

        user = UserProfile.objects.filter(user=self.user).first()
        amount = float(self.data.get("amount",default=0))
        user_bank_account = float(getattr(user.check_bank_account(amount).first(),'bank_account'))
        
        if (( amount > 0 ) and (user_bank_account - amount > 0)):
        
            user.debit_bank_account(amount)
        else:
            raise forms.ValidationError(_("You cannot buy this comment"))

        return cleaned_data

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.comment = self.comment
            self.instance.amount = self.amount

        return super(BuyForm, self).save(commit)
