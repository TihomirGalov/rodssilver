from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))

    @property
    def slug(self):
        return self.title.replace(' ', '-')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Item(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Price"))
    description = models.TextField(verbose_name=_("Description"))
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name=_("Category"))

    @property
    def slug(self):
        return self.title.replace(' ', '-')

    @property
    def main_photo(self):
        return self.images.first().image

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Image'))
    item = models.ForeignKey(Item, related_name='images', verbose_name=_("Image"), on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Variation(models.Model):
    name = models.CharField(verbose_name=_('Title'), max_length=255)
    item = models.OneToOneField(Item, related_name='variations', on_delete=models.CASCADE, verbose_name=_("Item"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Variation")
        verbose_name_plural = _("Variations")


class ItemVariation(models.Model):
    variation = models.ForeignKey(Variation, related_name='item_variations', on_delete=models.CASCADE, verbose_name=_("Variation"))
    name = models.CharField(verbose_name=_('Title'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item Variation")
        verbose_name_plural = _("Item Variations")
