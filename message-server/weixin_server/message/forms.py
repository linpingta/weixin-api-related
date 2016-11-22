#-*- coding: utf-8 -*-
from django import forms


class WatchContentForm(forms.Form):
    CHOICES = (('1', '是'), ('0', '否'))
    account_spent = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True, initial='1', label="账户余额")
    creative_status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True, initial='1', label="创意据登")
    frequency = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True, initial='0', label="频率控制")
    other = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True, initial='0', label="其它监控")


class TaskContentForm(forms.Form):
    name = forms.CharField(label="名称", required=True, max_length=100)
    AD_CHOICES = (('1', 'campaign'), ('2', 'account'), ('3', 'user-defined'))
    ad_type = forms.ChoiceField(choices=AD_CHOICES, widget=forms.RadioSelect, required=True, initial='1', label="对象类别")
    condition = forms.CharField(label="对象", required=True, max_length=100)
    roi = forms.IntegerField(label="利润率", required=True)
    CHECK_CHOICES = (('1', 'daily'), ('2', 'lifetime'))
    check_type = forms.ChoiceField(choices=CHECK_CHOICES, widget=forms.RadioSelect, required=True, initial='1', label="时间范围")
