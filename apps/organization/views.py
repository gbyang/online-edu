from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg,CityDict
from .forms import UserAskFrom
from operation.models import UserFavorite
from organization.models import Teacher
from courses.models import Course


# Create your views here.
class OrgListView(View):
    """
    机构列表页
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()

        # 教师搜索
        keyword = request.GET.get("keywords", "")
        all_orgs = all_orgs.filter(Q(name__icontains=keyword) |  # __icontains  i表示忽略大小写
                                           Q(desc__icontains=keyword))

        # toplist
        top_list = all_orgs.order_by('-student_nums')[0:3]

        # city
        city_id = request.GET.get("city", '')
        if city_id:  # url中有city参数则进行筛选
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # category
        category = request.GET.get("ct", "")
        if category:  # url中有city参数则进行筛选
            all_orgs = all_orgs.filter(category=category)


        org_nums = all_orgs.count()

        # sort
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-student_nums')
            if sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'sort': sort,
            'top_list': top_list,
            'keywords':keyword
        })


class UserAskView(View):
    """
    用户学习框
    """
    def post(self, request):
        userask_form = UserAskFrom(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 可以将上面的commit改为false来获取model实例，再如下面的代码修改实例属性再save
            # user_ask.name = 'haha'
            # user_ask.save()

            # json的key和value都要用双引号
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # json的key和value都要用双引号
            return HttpResponse('{"status":"fail", "msg":"信息有误"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.filter(id=org_id)[0]
        courses = org.course_set.all()[0:3]
        teachers = org.teacher_set.all()[0:1]
        # 点击数+1
        org.click_nums += 1
        org.save()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            'courses': courses,
            'org': org,
            'teachers': teachers,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    """
    机构课程页
    """
    def get(self, request, org_id):
        current_page = 'course'
        org = CourseOrg.objects.filter(id=org_id)[0]
        courses = org.course_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'courses': courses,
            'org': org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    """
    机构描述页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.filter(id=org_id)[0]

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.filter(id=org_id)[0]
        teachers = org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'teachers': teachers,
            'current_page':current_page,
            'has_fav':has_fav
        })


class AddFavView(View):
    """
    添加收藏
    """
    def post(self,request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        else:
            fav = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if fav: # 若收藏记录已存在，则取消收藏
                fav.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                if fav_id > 0 and fav_type > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()

                    if fav_type == 1:
                        course = Course.objects.get(id=fav_id)
                        course.fav_nums += 1
                        course.save()
                    elif fav_type == 2:
                        org = CourseOrg.objects.get(id=fav_id)
                        org.fav_nums += 1
                        org.save()
                    elif fav_type == 3:
                        teacher = Teacher.objects.get(id=fav_id)
                        teacher.fav_nums += 1
                        teacher.save()
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师页面
    """

    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 教师搜索
        keyword = request.GET.get("keywords", "")
        all_teachers = all_teachers.filter(Q(name__icontains=keyword)| # __icontains  i表示忽略大小写
                                         Q(work_company__icontains=keyword)|Q(work_position__icontains=keyword))


        # sort by hot
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by('-click_nums')

        # hot teacher list
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html',{
            'all_teachers':teachers,
            'sort': sort,
            'sorted_teachers':sorted_teachers,
            'keywords': keyword
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.filter(id=teacher_id)[0]
        all_courses = teacher.course_set.all()

        # 点击数+1
        teacher.click_nums += 1
        teacher.save()
        # page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses, 1, request=request)
        courses = p.page(page)

        hot_teachers = Teacher.objects.filter(org=teacher.org).order_by('-click_nums')

        has_fav_teacher = False
        has_fav_org = False
        # 若用户已登陆，检测该课程及相关机构是否已收藏，并发送回前端页面进行数据渲染
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=1):
                has_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org': has_fav_org,
            'courses':courses,
            'hot_teachers':hot_teachers
        })