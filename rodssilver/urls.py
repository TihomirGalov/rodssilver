"""rodssilver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rodssilver.views import HomeView, AllProductsView, CategoryView, ProductView, CheckoutView, FinishOrder, about_us, contact_us
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('products/', AllProductsView.as_view(), name='products'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', ProductView.as_view(), name='product'),
    path('finish-order/', FinishOrder.as_view(), name='finish'),
    path('about/', about_us, name='about'),
    path('contact/', contact_us, name='contact'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

]


urlpatterns += (
        i18n_patterns(path(r"", admin.site.urls), prefix_default_language=False)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
