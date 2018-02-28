from django.conf.urls import url

from .views import OrgListView, UserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,\
    AddFavView,TeacherListView,TeacherDetailView

app_name = 'org'
urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    url(r'^ask/$', UserAskView.as_view() , name='user_ask'),
    url(r'^home/(?P<org_id>\d+)$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name='org_teacher'),
    # 收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView  .as_view(), name='teacher_detail'),
]