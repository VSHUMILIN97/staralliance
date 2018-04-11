"""PiedPiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth import views as auth_views

from Exchanges import views
from Exchanges.views import custom_login


class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('Exchanges.urls'), name="home"),
    url(r'^accounts/', include('registration.urls')),
    url(r'^login', custom_login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # registration by using only unique email
    url(r'^user/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),
    url(r'^accounts/profile/$', views.profile, name='profile')


]
(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/static/admin/css/'}),
