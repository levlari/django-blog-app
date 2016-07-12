from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from . import views


app_name = 'blog'

urlpatterns = [
    # *** Content ***:
    url(r'^$', views.BlogHome.as_view(), name='home'),
    url(r'^read/(?P<slug>\S+)/$', views.ReadPost.as_view(), name='read_post'),    # TODO: capture `pk` also
    url(r'^write/$', views.WritePost.as_view(), name='write_post'),
    url(r'^delete/(?P<slug>\S+)/$', views.DeletePost.as_view(), name='delete_post'),

    # *** Authentication ***:
    url(r'^login/$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    # url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^logout/$', auth_views.logout_then_login, {'login_url': 'blog:login'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/confirm/$', views.register_confirm, name='register_confirm'),
    url(r'^register/check/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.register_check, name='register_check'),
    url(r'^register/done/$', views.register_done, name='register_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
