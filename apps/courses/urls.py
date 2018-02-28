from django.conf.urls import url

from .views import CourseListView,CourseDetailView,CourseVideoView,CourseCommentView,AddCommentView


app_name = 'course'
urlpatterns = [
    url('^list/$', CourseListView.as_view(), name='course_list'),
    url('^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url('^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url('^add_comment/$', AddCommentView.as_view(), name='course_add_comment'),
    url('^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
]