from django.shortcuts import render,redirect, reverse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments,UserCourse


# Create your views here.
class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        # 默认最新排序
        all_courses = Course.objects.all().order_by('-add_time')

        # 热门课程列表
        hot_courses = Course.objects.all().order_by('-fav_nums')[:3]

        # 课程搜索
        keyword = request.GET.get("keywords", "")
        all_courses = all_courses.filter(Q(name__icontains=keyword)| # __icontains  i表示忽略大小写
                                         Q(desc__icontains=keyword)|Q(detail__icontains=keyword))

        # 数据排序
        sort = request.GET.get("sort",'')
        if sort == 'hot':
            all_courses = all_courses.order_by('-fav_nums')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')


        # 将经过上面筛选的数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 3, request=request) # 3表示一页显示多少个数据
        courses = p.page(page)  # 获取第page页的数据
        return render(request, 'course-list.html', {
            'courses':courses,
            'sort': sort,
            'hot_courses':hot_courses,
            'keywords': keyword
        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 点击数+1
        course.click_nums += 1
        course.save()

        # 根据tag获取相关课程
        relate_courses = Course.objects.filter(tag=course.tag)[:1]
        if relate_courses:
            pass
        else:
            relate_courses = []

        has_fav_course = False
        has_fav_org = False
        # 若用户已登陆，检测该课程及相关机构是否已收藏，并发送回前端页面进行数据渲染
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })


class CourseVideoView(View):
    """
    课程视频
    """
    def get(self, request, course_id):
        # 未登录不能学习
        if not request.user.is_authenticated():
            return redirect(reverse('users:login'))

        course = Course.objects.get(id=int(course_id))
        uc_is_exist = UserCourse.objects.filter(course=course,user=request.user)
        if not uc_is_exist:
            # 将user与course绑定到USERCOURSE表
            user_course = UserCourse(course=course,user=request.user)
            user_course.save()

        # 获取学过这个课程的人学过的其他课程
        user_courses = UserCourse.objects.filter(course=course)
        all_users = [uc.user.id for uc in user_courses]
        temp_user_courses = UserCourse.objects.filter(user_id__in=all_users)
        learn_courses_id = [uc.course.id for uc in temp_user_courses]
        learn_courses = Course.objects.filter(id__in=learn_courses_id)
        resources = CourseResource.objects.all().filter(course=course)

        return render(request, 'course-video.html', {
            'course':course,
            'resources':resources,
            'learn_courses':learn_courses
        })


class AddCommentView(View):
    """
    添加评论
    """
    def post(self, request):
        # 首先判断是否已经登陆，未登录无法评论
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json') # content-type
        else:
            # 获取post中的id和comment
            course_id = int(request.POST.get("course_id", 0)) # 注意转为int
            comment = request.POST.get("comments", "")
            if course_id > 0 and comment: # 测试数据是否合法
                course_comments = CourseComments()
                course_comments.user = request.user
                course_comments.course = Course.objects.get(id=course_id)
                course_comments.comments = comment
                course_comments.save()
                return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class CourseCommentView(View):
    """
    课程评论
    """
    def get(self, request, course_id):
        if not request.user.is_authenticated():
            return redirect(reverse('users:login'))

        course = Course.objects.get(id=int(course_id))
        uc_is_exist = UserCourse.objects.filter(course=course,user=request.user)
        if not uc_is_exist:
            # 将user与course绑定到USERCOURSE表
            user_course = UserCourse(course=course,user=request.user)
            user_course.save()

        # 获取学过这个课程的人学过的其他课程
        user_courses = UserCourse.objects.filter(course=course)
        all_users = [uc.user.id for uc in user_courses]
        temp_user_courses = UserCourse.objects.filter(user_id__in=all_users)
        learn_courses_id = [uc.course.id for uc in temp_user_courses]
        learn_courses = Course.objects.filter(id__in=learn_courses_id)
        resources = CourseResource.objects.all().filter(course=course)

        # 获取课程相关资源
        resources = CourseResource.objects.all().filter(course=course)
        # 获取评论并按最新时间排列
        comments = course.coursecomments_set.all().order_by('-add_time')
        return render(request, 'course-comment.html', {
            'course': course,
            'resources': resources,
            'comments':comments,
            'learn_courses': learn_courses
        })