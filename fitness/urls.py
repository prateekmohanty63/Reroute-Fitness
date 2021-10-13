from django.urls import path
from. import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name='index'),
    path('index',views.index,name="index"),
    path('contact',views.contact,name='contact'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path("logout/",views.logout,name="logout"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("handlerequest/",views.handlerequest,name="HandleRequest"),
    path("payment",views.payment,name="payment"),
    path("about/",views.about,name="about"),
    path("gallery/",views.gallery,name="gallery"),
    path("event/",views.event,name="event"),


]