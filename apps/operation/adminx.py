import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserFavorite


class UserAskAdmin(object):
    list_display = ['name', 'course', 'mobile', 'add_time']
    list_filter = ['name', 'course', 'mobile', 'add_time']
    search_fields = ['name', 'course', 'mobile']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    list_filter = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_type', 'fav_id', 'add_time']
    list_filter = ['user', 'fav_type', 'fav_id', 'add_time']
    search_fields = ['user', 'fav_type', 'fav_id']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)


