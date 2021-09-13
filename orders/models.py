from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import Item, ItemVariation


class OrderStatus(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")


class ShippingAddress(models.Model):
    street_address = models.CharField(max_length=100, verbose_name=_("Street Address"))
    phone_number = models.CharField(max_length=100, verbose_name=_("Phone"))
    contact = models.CharField(max_length=100, verbose_name=_("Contact"))
    zip = models.CharField(max_length=10, verbose_name=_("ZIP code"))
    city = models.CharField(max_length=100, verbose_name=_("City"))

    def __str__(self):
        return f"{self.zip} {self.city} {self.street_address}"

    class Meta:
        verbose_name = _("Shipping Address")
        verbose_name_plural = _("Shipping Addresses")


class Order(models.Model):
    status = models.ForeignKey(OrderStatus, related_name='orders', on_delete=models.CASCADE, verbose_name=_('Status'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    shipping_address = models.ForeignKey(ShippingAddress, related_name='orders', on_delete=models.CASCADE,
                                         verbose_name=_("Shipping Address"))

    @property
    def total(self):
        return self.items.all().aggregate(models.Sum('item__price'))['item__price__sum'] or 0

    def __str__(self):
        return f"{_('Order')} № {self.pk} {self.date.strftime('%x')}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_("Order"))
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE, verbose_name=_('Item'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    item_variation = models.ForeignKey(ItemVariation, related_name='order_items', verbose_name=_("Variation"),
                                       on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.item_variation or '-'} {self.item}"

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
