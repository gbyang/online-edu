"""MxOnline URL Configuration

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
import xadmin
from django.conf.urls import url, include
from django.views.static import serve

from MxOnline.settings import MEDIA_ROOT
from users.views import IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^', include('users.urls')),
    url(r'^user/', include('users.urls')),
    url('^image/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 为MEDIA_URL设置静态路径
    # 配置DEBUG为False后，不会再去staticfiles_dirs中寻找static文件，要自己配置，跟配置图片文件方式一样
    # url('^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    url(r'^org/', include('organization.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^course/', include('courses.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]


# 全局404页面配置
"""
1. 编写处理的函数
2. 修改setting中DEBUG和ALLOW_HOSTS
3. 为static文件夹设置处理路径（url和static_root）
4. 配置handler404
"""
handler404 = 'users.views.page_not_found'
# 全局404页面配置
handler500 = 'users.views.page_error'
