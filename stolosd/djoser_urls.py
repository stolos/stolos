from django.conf.urls import url
from djoser import views


urlpatterns = (
    url(r'^me/$', views.UserView.as_view(), name='user'),
    url(r'^password/$', views.SetPasswordView.as_view(), name='set_password'),
    url(r'^password/reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^$', views.RootView.as_view(urls_extra_mapping={'login': 'login', 'logout': 'logout'}), name='root'),
)
