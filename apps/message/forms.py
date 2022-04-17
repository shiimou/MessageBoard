#!/usr/bin/env python
# -*- coding:utf-8 -*-
# file: forms.py
from django import forms



class CommentForm(forms.Form):
    content = forms.CharField(required=True)
