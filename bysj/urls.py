"""
Bysj_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/source.11/topics/http/urls/
Examples:
Function views
    source. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    source. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    source. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from bysj.views import auth, show

urlpatterns = [
    url(r'^login/', auth.login, name='login'),
    url(r'^logout/', auth.logout, name='logout'),
    url(r'^reg/', auth.reg, name='reg'),
    url(r'^ge/', auth.ge, name='ge'),
    url(r'^userinfo/', auth.userinfo_change, name='userinfo'),
    url(r'^index/', show.index, name='index'),
    url(r'^my_book_list/', show.my_book_list, name='my_book_list'),
    url(r'^book_list/*', show.book_list, name='book_list'),
    url(r'^book_update/', show.book_update, name='book_update'),
    url(r'^annunciate/', show.annunciate, name='annunciate'),
    url(r'^comment/', show.comment, name='comment'),


]
