# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone


class CommentBuy(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='st_comment_buys')
    comment = models.ForeignKey('spirit_comment.Comment', related_name='comment_buys')

    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(_("amount"), max_digits=19,decimal_places=2, default=0)

    class Meta:
        ordering = ['-date', '-pk']
        verbose_name = _("buy")
        verbose_name_plural = _("buys")

