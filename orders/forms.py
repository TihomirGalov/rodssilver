from django import forms
from utils.forms import ActionForm
from orders.models import OrderStatus
from django.utils.translation import gettext_lazy as _


class ChangeStatusForm(ActionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['status'] = forms.ModelChoiceField(queryset=OrderStatus.objects.exclude(title=self.obj.status.title), label=_("Status"))

    def form_action(self, obj, user):
        obj.status = self.cleaned_data.get('status')
        obj.save()
