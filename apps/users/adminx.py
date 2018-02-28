import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVerifyCode, Banner


class GlobalSetting(object):
    # 设置左上角brand
    site_title = 'gbyang的后台'
    # 设置footer的显示
    site_footer = 'gbyang的网站'
    # 折叠app的数据表
    menu_style = 'accordion'


class EmailVerifyCodeAdmin(object):
    # 后台展示的数据(字段名)
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 添加可过滤的字段
    list_filter = ['code', 'email', 'send_type', 'send_time']
    # 添加可搜索的字段
    search_fields = ['code', 'email', 'send_type']
    # xadmin 后台图标替换
    model_icon = 'fa fa-envelope'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    # xadmin 后台图标替换
    model_icon = 'fa fa-bullhorn'


xadmin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)  # 注册设置