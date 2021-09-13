from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext

from orders.models import Order, OrderItem, OrderStatus, ShippingAddress
from orders.forms import ChangeStatusForm


admin.site.register(OrderStatus)
admin.site.register(ShippingAddress)


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    list_display = ['order', 'total', 'date', 'status', 'order_actions']

    def order(self, obj):
        return str(obj)

    def change_status(self, request, order_id):
        return self.process_action(
            request=request,
            order_id=order_id,
            action_form=ChangeStatusForm,
            action_title=_("Change Status"),
        )

    def process_action(self, request, order_id, action_form, action_title):
        obj = self.get_object(request, order_id)
        if request.method != "POST":
            form = action_form(obj=obj)
        else:
            form = action_form(request.POST, obj=obj)
            if form.is_valid():
                form.save(obj, request.user)
                self.message_user(request, _("Status changed"))
                url = reverse(
                    "admin:orders_order_changelist",
                    current_app=self.admin_site.name,
                )
                return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context["opts"] = self.model._meta
        context["form"] = form
        context["recipe"] = obj
        context["title"] = action_title
        return TemplateResponse(
            request,
            "admin/order/run_action.html",
            context,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<order_id>.+)/change_status/$",
                self.admin_site.admin_view(self.change_status),
                name="change-status",
            )
        ]
        return custom_urls + urls

    def order_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">' + gettext("Change Status") + "</a>",
            reverse("admin:change-status", args=[obj.pk]),
            )

    order.short_description = _('Order')
