from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    re_path(r'^about', views.about_request, name='about'),
    re_path(r'^contact', views.contact_request, name='contact'),
    
    #path(route='', view=views.get_dealerships, name='index'),
    path('dealership/', view=views.get_dealerships, name='dealerships'),
    path('dealership/<str:state>/', view=views.get_dealerships, name='dealershipsbystate'),
    path('review/<int:dealer_id>/', view=views.add_review, name='add_review'),
    path('reviews/<int:dealer_id>/', view=views.get_reviews, name='dealer_details'),
    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)