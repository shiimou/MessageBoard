#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file: forms.py
from django import forms

class ArticlesForm(forms.Form):
    title = forms.CharField(required=True)

class CommentForm(forms.Form):
    content = forms.CharField(required=True)
