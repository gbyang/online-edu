import json

from django.shortcuts import render, redirect, reverse, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from utils.email_send import send_register_email
from .models import EmailVerifyCode,UserProfile,Banner
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm,UserInfoForm
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course,Teacher
from organization.models import CourseOrg


# 重写用户认证判断(增加邮箱登陆)
class CustomAuth(ModelBackend): # 需要继承ModelBackend，完成该类编写后配置settings中的AUTHENTICATION_BACKENDS字段即可
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    """
    登出
    """
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

# 使用类来处理view
class LoginView(View):
    """
    登陆
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        # 调用form对象校验表格
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 确认是否存在用户
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')  # 登陆成功后跳转回首页
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form}) # 返回form的信息，可在HTML中校验

# def login_view(request):
#     if request.method == 'POST':
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         # 确认是否存在用户
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html', {})
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误'})
#
#     else:
#         return render(request, 'login.html', {})


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(pass_word)  # 将密码转换为密文再保存
            user_profile.is_active = False
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "注册成功！"
            user_message.save()

            # 发送验证邮件
            send_register_email(email, "register")
            return redirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    """
    邮箱账号激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
                return redirect(reverse('users:login'))
        else:
            return render(request, 'active_fail.html')


class ForgetView(View):
    """
    忘记密码
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', "")
            try:
                user = UserProfile.objects.get(email=email)
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            except Exception as e:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, "msg": '用户不存在'})
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """
    重置密码
    """
    def get(self, request, reset_code):
        all_records = EmailVerifyCode.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    """
    修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            email = request.POST.get('email', "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


# 登陆才能进入
class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心
    """
    def get(self, request):
        current_page = 'info'
        return render(request, 'usercenter-info.html', {
            'current_page':current_page
        })
    def post(self, request):
        """
        修改用户信息
        """
        user_form = UserInfoForm(request.POST, instance=request.user) # 修改实例一般要指定instance，新数据则不用

        if user_form.is_valid():
            user_form.save() # 一步提交
        else:
            return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


# 登陆才能进入
class UserUploadImageView(LoginRequiredMixin,View):
    """
    专门处理图像上传的View
    """
    def post(self, request):
        # 获取image（文件获取要用request.FILES）
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # 参数中指明了instance（必须是ModelForm对应model的实例），可直接save
            image_form.save()
            # 参数中未指明instance时，使用下面代码，cleaned_data是已经通过验证的字段字典数据
            # request.user.image = image_form.cleaned_data['image']
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserUpdatePwdView(View):
    """
    用户信息更新
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', "")
            pwd2 = request.POST.get('password2', "")
            if pwd1 != pwd2:
                return HttpResponse('{"msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(pwd1)
            request.user.save()
            return HttpResponse('{"status":"success","msg":"密码修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class UserUpdateEmailSendView(LoginRequiredMixin, View):
    """
    修改邮箱发送邮件
    """
    def get(self, request):
        email = request.GET.get('email',"")

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        else:
            send_register_email(email, 'update_em')
            return HttpResponse('{"status":"success"}', content_type='application/json')


class UserUpdateEmailView(LoginRequiredMixin, View):
    """
    邮箱验证
    """
    def post(self, request):
        code = request.POST.get('code',"")
        email = request.POST.get('email',"")

        evfs = EmailVerifyCode.objects.filter(code=code)
        if evfs:
            if evfs[0].email == email:
                request.user.email = email
                request.user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"email":"邮箱与验证码不匹配"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码不存在"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    """
    用户学习的课程
    """
    def get(self, request):
        current_page = 'course'
        user_courses = UserCourse.objects.filter(user=request.user)
        courses_id = [c.course_id for c in user_courses]
        courses = Course.objects.filter(id__in=courses_id)
        return render(request, 'usercenter-mycourse.html', {
            'current_page':current_page,
            'courses':courses
        })


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户收藏的机构
    """
    def get(self, request):
        org_list = list()
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav in user_favs:
            org_id = fav.fav_id
            org_list.append(CourseOrg.objects.get(id=org_id))
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户收藏的教师
    """
    def get(self, request):
        teacher_list = list()
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav in user_favs:
            teacher_id = fav.fav_id
            teacher_list.append(Teacher.objects.get(id=teacher_id))
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list
        })


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户收藏的课程
    """
    def get(self, request):
        course_list = list()
        user_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav in user_favs:
            course_id = fav.fav_id
            course_list.append(Course.objects.get(id=course_id))
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list
        })


class UserMessageView(LoginRequiredMixin, View):
    """
    用户收到的站内信
    """
    def get(self, request):
        # 获取个人消息及全站消息
        all_messages = UserMessage.objects.filter(Q(user=0)|Q(user=request.user.id))
        # 将用户消息设置为已读
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # page
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages, 1, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':messages
        })


class IndexView(View):
    """
    官网首页
    """
    def get(self, request):
        # 500页面测试
        # print(1/0)
        all_banner = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banner':all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 全局404处理函数
def page_not_found(request):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


# 全局500处理函数
def page_error(request):
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response
