from django.urls import path
from . import views

urlpatterns = [
    # base urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Car urls
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
    path('cars/<int:car_id>/add_washing/',
         views.add_washing, name='add_washing'),
    path('cars/<int:car_id>/assoc_acessory/<int:accessory_id>/',
         views.assoc_accessory, name='assoc_accessory'),
    path('cars/<int:car_id>/remove_accessory/<int:accessory_id>/',
         views.remove_accessory, name='remove_accessory'),
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),

    # toy urls
    path('accessories/', views.accessories_index, name='all_accessories'),
    path('accessories/<int:accessory_id>/',
         views.accessory_detail, name='accessory_detail'),
    path('accessories/create/', views.Create_Accessory.as_view(),
         name='create_accessory'),
    path('accessories/<int:pk>/update/',
         views.Update_Accessory.as_view(), name='update_accessory'),
    path('accessories/<int:pk>/delete/',
         views.Delete_Accessory.as_view(), name='delete_accessory'),
]
