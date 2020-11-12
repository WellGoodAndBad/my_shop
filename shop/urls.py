from django.urls import path
from .views import (AddToCartView,
                    HomePageView,
                    MyCartView,
                    DeleteFromCartView,
                    AllCartsView,
                    GetData,
                    PDFCreaView)


app_name = "shop"

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('mycart/<int:id>/', MyCartView.as_view(), name='mycart'),
    path('all-carts/', AllCartsView.as_view(), name='all_carts'),
    path('add-to-cart/<int:id>/<int:item_shop>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<int:id>/<str:item_shop>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('get_data/', GetData.as_view(), name='get_data'),
    path('pdf/<int:id>/', PDFCreaView.as_view(), name='pdf_data'),
]