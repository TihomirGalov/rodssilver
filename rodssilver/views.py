from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.conf import settings

from orders.models import ShippingAddress, OrderItem, Order, OrderStatus
from products.models import Item, Category, ItemVariation
from .forms import CheckoutForm


class HomeView(ListView):
    model = Item
    paginate_by = 3
    template_name = "index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = list()
        for category in Category.objects.all().order_by('-products__order_items__quantity').distinct()[:3]:
            if category.products.all().count():
                context['categories'].append({
                    'title': category.title,
                    'photo': category.products.all().order_by('-order_items__quantity')[0].images.first().image.url,
                    'slug': category.slug
                })
        return context


class AllProductsView(ListView):
    model = Item
    paginate_by = 9
    template_name = "shop.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.filter(products__isnull=False).distinct()
        context['all'] = True

        return context


class CategoryView(ListView):
    model = Item
    paginate_by = 9
    template_name = "shop.html"

    def get_queryset(self):
        title = self.kwargs['slug'].replace('-', ' ')
        queryset = self.model._default_manager.filter(category__title=title)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = list()
        selected_category = Category.objects.get(title=self.kwargs['slug'].replace('-', ' '))
        if not selected_category:
            context['all'] = True
        for category in Category.objects.filter(products__isnull=False).distinct():
            context['categories'].append({
                "title": category.title,
                "slug": category.slug,
                'selected': category == selected_category
            })

        return context


class ProductView(DetailView):
    model = Item
    template_name = 'shop-single.html'

    def get(self, request, *args, **kwargs):
        self.object = Item.objects.get(title=self.kwargs['slug'].replace('-', ' '))
        context = self.get_context_data(object=self.object)
        context['pages'] = list()
        context['pages'].append(list())
        index = 0
        images = list(self.object.images.all())
        for counter, image in enumerate(images):
            context['pages'][index].append(image)
            if (counter + 1) % 3 == 0 and not images[-1] == image:
                index += 1
                context['pages'].append(list())
        print(context['pages'])
        try:
            context['item_variations'] = self.object.variations.item_variations.all().values_list('name', flat=True)
        except ObjectDoesNotExist:
            context['item_variations'] = None

        context['related'] = Item.objects.filter(category__title=self.object.category.title).exclude(id=self.object.pk)[
                             :3]
        return self.render_to_response(context)


class CheckoutView(View):

    def get(self, *args, **kwargs):
        data = self.request.GET
        print(data)
        price = Item.objects.get(title=data['product-title']).price
        context = dict()
        context['form'] = CheckoutForm()
        context['product'] = {
            'title': data['product-title'],
            'variation': data.get('variation_value', None),
            'quantity': data['product-quantity'],
            'price': price,
            'total': price * int(data['product-quantity']),
            'total_with_shipping': price * int(data['product-quantity']) + settings.SHIPPING_FEE,
        }

        return render(self.request, "checkout.html", context)


class FinishOrder(View):

    @csrf_exempt
    def post(self, *args, **kwargs):
        data = self.request.POST
        address = ShippingAddress.objects.create(
            street_address=data['street_address'],
            phone_number=data['phone'],
            contact=data['contact'],
            zip=data['zip'],
            city=data['city']
        )
        order = Order.objects.create(
            status=OrderStatus.objects.first(),
            shipping_address=address
        )
        item_var = None
        if data.get('variation', None):
            item_var = ItemVariation.objects.get(name=data['variation'], variation__item=Item.objects.get(title=data['title']))
        order_item = OrderItem.objects.create(
            order=order,
            item=Item.objects.get(title=data['title']),
            quantity=int(data['quantity']),
            item_variation=item_var,
        )
        return render(self.request, 'index.html', {})


def about_us(request):
    return render(request, 'about.html', {})


def contact_us(request):
    return render(request, 'contact.html', {})
