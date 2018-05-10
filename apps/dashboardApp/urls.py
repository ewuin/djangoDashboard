from django.conf.urls import url
from . import views           # This line is new!


urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^signin$', views.signin, name= "signin"),
    url(r'^process_signin$', views.process_signin, name="process_signin"),
    url(r'^register$',views.register,name="register"),
    url(r'^process_registraion$', views.process_registraion, name="process_registraion"),
    url(r'^logout$',views.logout, name="logout"),
    url(r'^add_by_admin$',views.add_by_admin, name="add_by_admin"),
    url(r'^process_addbyadmin$', views.process_addbyadmin, name="process_addbyadmin"),
    url(r'^edit_user/(?P<user_id>\d+)$',views.edit_user, name="edit_user"),
    url(r'^dashboard/(?P<user_id>\d+)$', views.see_dashboard, name="see_dashboard"),
    url(r'^process_edit/(?P<user_id>\d+)$',views.process_edit, name="process_edit"),
    ]
