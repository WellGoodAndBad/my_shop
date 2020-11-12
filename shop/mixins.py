from django.http import Http404
from users.models import User
from shop.models import ItemShop, UserCart
from django.contrib.auth.mixins import LoginRequiredMixin


class EditDeletMixin:

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        cart = UserCart.objects.get(owner=user)
        cart_owner = cart.owner
        if cart_owner != self.request.user and self.request.user.role != 'manager':
            raise Http404
        else:
            return super().dispatch(request, *args, **kwargs)


class BaseCartMixin(LoginRequiredMixin, EditDeletMixin,):

    def get(self, request, *args, **kwargs):
        user_id, item_shop = kwargs.get('id'), kwargs.get('item_shop')
        user = User.objects.get(pk=user_id)
        item = ItemShop.objects.get(pk=item_shop)
        user_cart = UserCart.objects.get(owner=user)
        return user_cart, item


class ManagerCheckMixin:

    def get(self, request, *args, **kwargs):
        if self.request.user.role == 'manager':
            return super().get(request, *args, **kwargs)
        else:
            raise Http404