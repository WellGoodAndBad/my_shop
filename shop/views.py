from django.http import HttpResponseRedirect
from django.views.generic.list import ListView, View
from django.views.generic.detail import DetailView
from users.models import User
from django.shortcuts import render
from .models import ItemShop, UserCart
from .mixins import EditDeletMixin, ManagerCheckMixin, BaseCartMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import parse_task, crt_pdf


class HomePageView(ListView):
    model = ItemShop
    template_name = "shop/home.html"
    context_object_name = "shop_items"


class MyCartView(LoginRequiredMixin, EditDeletMixin, DetailView):
    model = UserCart
    template_name = 'shop/my_cart.html'
    context_object_name = 'shop_items'

    def get(self, request, *args, **kwargs):

        user = User.objects.get(id=self.kwargs['id'])
        cart = self.model.objects.get(owner=user)
        context = {
            'cart': cart
        }
        return render(request, 'shop/my_cart.html', context)


class AddToCartView(BaseCartMixin, View):

    def get(self, request, *args, **kwargs):
        user_cart, item = super().get(request, *args, **kwargs)
        user_cart.items.add(item)
        user_cart.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromCartView(BaseCartMixin, View):

    def get(self, request, *args, **kwargs):
        user_cart, item = super().get(request, *args, **kwargs)
        user_cart.items.remove(item)
        user_cart.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PDFCreaView(LoginRequiredMixin, EditDeletMixin, View):

    def get(self, request, *args, **kwargs):
        user_id, item_shop = kwargs.get('id'), kwargs.get('item_shop')
        crt_pdf.delay(user_id, item_shop)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AllCartsView(LoginRequiredMixin, ManagerCheckMixin, ListView):
    model = UserCart
    template_name = "shop/all_carts.html"
    context_object_name = "carts"


class GetData(View):

    def get(self, request, *args, **kwargs):
        parse_task.delay()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


