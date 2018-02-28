import xadmin

from .models import Course, Lesson, CourseResource, Video, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # list_display不仅可以传入对应Model的字段，也可以传入对应Model的函数
    # 只要配置函数的short_description字段就能显示在后台，不定义的话就会显示函数名
    list_display = ['name','get_lesson_num','go_to', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    # xadmin后台排序
    ordering = ['-click_nums']
    # xadmin后台只读字段
    readonly_fields = ['fav_nums']
    # xadmin后台隐藏字段
    exclude = ['click_nums']
    # xadmin后台内联表(在添加课程时，可同时添加章节及课程资源)
    inlines = [LessonInline, CourseResourceInline]
    # xadmin后台列表页可进行修改的数据（不必进入数据的详情页）
    list_editable = ['degree','name']
    # xadmin后台列表页自动刷新(单位：秒)
    refresh_times = [100,300,500]  # 多个数据将显示为可选项
    # 使用ueditor识别detail
    style_fields = {'detail': 'ueditor'}
    # 显示导入excel
    import_excel = True


    # xadmin后台展示列表可以通过重写queryset函数来修改
    def queryset(self):
        # 调用父类函数 以获得完整queryset
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs



class BannerCourseAdmin(object):
    list_display = ['name','get_lesson_num', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    # xadmin后台排序
    ordering = ['-click_nums']
    # xadmin后台只读字段
    readonly_fields = ['fav_nums']
    # xadmin后台隐藏字段
    exclude = ['click_nums']
    # xadmin后台内联表(在添加课程时，可同时添加章节及课程资源)
    inlines = [LessonInline, CourseResourceInline]

    # xadmin后台展示列表可以通过重写queryset函数来修改
    def queryset(self):
        # 调用父类函数 以获得完整queryset
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']
    search_fields = ['course', 'name']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    list_filter = ['lesson__name', 'name', 'add_time']
    search_fields = ['lesson', 'name']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']

# 为一个表绑定两个Admin
"""
1. models中BannerCourse继承Course，并设置proxy为True
2. 添加 BannerCourseAdmin 并重写queryset方法
3. 为CourseAdmin重写queryset方法
4. 注册Admin
"""
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)

xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)