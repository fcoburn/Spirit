# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from ...core.utils import json_response
from ..models import Comment
from .models import CommentBuy
from .forms import BuyForm


@login_required
def gobuy(request, comment_id):
    comment = get_object_or_404(Comment.objects.exclude(user=request.user), pk=comment_id)

    if request.method == 'POST':
        form = BuyForm(user=request.user, comment=comment, data=request.POST, amount=request.POST.get("amount",default=0))
        amount = form.data.get("amount",default=0)

        if form.is_valid():
            buy = form.save()
            buy.comment.increase_comment_value(amount)

            return redirect(request.POST.get('next', comment.get_absolute_url()))
    else:
        form = BuyForm()

    context = {
        'form': form,
        'comment': comment
    }

    return render(request, 'spirit/comment/like/gobuy.html', context)