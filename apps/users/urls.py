from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'), # 调用as_view()
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),  # 调用as_view()
    url(r'^register/', views.RegisterView.as_view(), name='register'),  # 调用as_view()
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name='active'),
    url(r'^forget/$', views.ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>.*)/$', views.ResetView.as_view(), name='reset'),
    url(r'^modify_pwd/$', views.ModifyPwdView.as_view(), name='modifypwd'),
    url(r'^info', views.UserInfoView.as_view(), name='user_info'),
    url(r'^user_course', views.UserCourseView.as_view(), name='user_course'),
    url(r'^upload_image/$', views.UserUploadImageView.as_view(), name='user_upload_image'),
    url(r'^update_pwd/$', views.UserUpdatePwdView.as_view(), name='user_update_pwd'),
    url(r'^update_email_send/$', views.UserUpdateEmailSendView.as_view(), name='user_update_email_send'),
    url(r'^update_email/$', views.UserUpdateEmailView.as_view(), name='user_update_email_send'),
    url(r'^myfav/org/$',views.UserFavOrgView.as_view(), name='user_fav_org'),
    url(r'^myfav/teacher/$', views.UserFavTeacherView.as_view(), name='user_fav_teacher'),
    url(r'^myfav/course/$', views.UserFavCourseView.as_view(), name='user_fav_course'),
    url(r'^mymessage/$', views.UserMessageView.as_view(), name='user_message'),
]