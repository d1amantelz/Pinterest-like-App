from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='pins'),
    path('pin/<int:pin_id>/', ShowPin.as_view(), name='pin'),
    path('collections/', CollectionsPage.as_view(), name='collections'),
    path('collection/<int:collection_id>/', ShowCollection.as_view(), name='collection'),
    path('add_project/', AddProject.as_view(), name='add_project'),
    path('profile/<int:profile_id>/', ProfilePage.as_view(), name='profile'),
    path('search/', SearchPage.as_view(), name='search'),
    path('change_profile/', ChangeProfile.as_view(), name='change_profile'),
]
