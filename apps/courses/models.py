from django.db import models
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构')
    name = models.CharField('课程名', max_length=50)
    desc = models.CharField('课程描述', max_length=100)
    detail = UEditorField('课程详情	',width=600, height=300, imagePath="course/ueditor/", filePath="course/ueditor/", default="")
    is_banner = models.BooleanField('是否轮播', default=False)
    course_type = models.CharField('课程类别', max_length=20, default='后端开发')
    degree = models.CharField('课程难度',max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')))
    learn_times = models.IntegerField('学习时长', default=0)
    students = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    image = models.ImageField('课程图片', upload_to='media/course')
    click_nums = models.IntegerField('点击数', default=0)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)
    teacher = models.ForeignKey(Teacher, verbose_name='教师', null=True, blank=True)
    tag = models.CharField('课程标签', default="", max_length=20)

    youneed_know = models.CharField('课程须知',max_length=300, default="")
    teacher_tell = models.CharField('老师告诉你',max_length=300, default="")
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_num(self):
        return self.lesson_set.all().count()
    get_lesson_num.short_description = '章节数'  # 为了在后台能正确显示

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.gbyang.cn" target="_blank">跳转链接</a>')  # make_safe后xadmin将其解析为html代码
    go_to.short_description = '跳转'  # 为了在后台能正确显示

    def get_students_who(self):
        user_courses = self.usercourse_set.all()[0:5]
        return user_courses

    def get_lessons(self):
        return self.lesson_set.all()


# 代理一个表，使得一个表可以使用两个Admin进行管理
class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 关键参数，设置之后不会生成新的数据表


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('章节名', max_length=100)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField('视频名', max_length=50)
    url = models.CharField('视频链接', max_length=100, default="")
    learn_times = models.IntegerField('学习时长', default=0)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('资源名', max_length=50)
    download = models.FileField('资源文件',upload_to='media/resource', max_length=100)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name