# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import UserInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 用户管理相关的视图函数

# 用户登录
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        print('用户：', user) 
        # 如果登录成功，返回token
        token, created = Token.objects.get_or_create(user=user)
        # 用户信息
        user_info = {
            'username': user.username,
            'email': user.email,
            'token': token.key
        }
        return Response({'msg': '登录成功', 'data': user_info})
    else:
        return Response({'msg': '登录失败'})


# 用户登出
@api_view(['GET'])
def user_logout(request):
    logout(request)
    return Response({'msg': '账号已下线'})

# 用户注册
@api_view(['POST'])
def user_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # 如果没有传入邮箱，则为空
    email = request.data.get('email') or ''
    # 判断用户名是否已经存在
    if User.objects.filter(username=username).exists():
        return Response({'msg': '用户已存在'})
    # 创建用户
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    if user:
        return Response({'msg': '注册成功'})
    else:
        return Response({'msg': '注册失败'})
    

@api_view(['GET'])
def test(request):
    return Response({'msg': '测试模块'})

# 返回所有用户信息
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    user_list = getUserInfo(users)
    return Response({'msg': '获取所有用户列表成功', 'data': user_list})

# 修改用户信息
@api_view(['POST'])
def user_update(request):

    uid = request.data.get('id')
    name = request.data.get('name')
    email = request.data.get('email')
    is_admin = request.data.get('is_superuser')
    gender = request.data.get('gender')
    phone = request.data.get('phone')
    
    # 获取用户信息
    user = User.objects.get(id=uid)
    user.username = name
    user.email = email
    # 如果权限为是，则为管理员
    if is_admin == '是':
        user.is_superuser = True
    else:  
        user.is_superuser = False
    
    # 获取用户信息，如果没有则创建
    if not UserInfo.objects.filter(user=user).exists():
        UserInfo.objects.create(user=user)
    user_info = UserInfo.objects.get(user=user)
    user_info.gender = gender
    user_info.phone = phone
    user_info.save()
    user.save()
    return Response({'msg': '修改用户信息成功'})

# 添加用户
@api_view(['POST'])
def user_add(request):
    name = request.data.get('name')
    email = request.data.get('email')
    is_admin = request.data.get('is_superuser')
    gender = request.data.get('gender')
    phone = request.data.get('phone')
    password = request.data.get('password')
    # 判断用户名是否已经存在
    if User.objects.filter(username=name).exists():
        return Response({'msg': '用户已存在'})
    # 创建用户
    user = User.objects.create_user(username=name, password=password, email=email)
    # 如果权限为是，则为管理员
    if is_admin == '是':
        user.is_superuser = True
    else:
        user.is_superuser = False
    user.save()
    # 获取用户信息，如果没有则创建
    if not UserInfo.objects.filter(user=user).exists():
        UserInfo.objects.create(user=user)
    user_info = UserInfo.objects.get(user=user)
    user_info.gender = gender
    user_info.phone = phone
    user_info.save()
    return Response({'msg': '添加用户成功'})

# 删除用户
@api_view(['POST'])
def user_delete(request):
    uid = request.data.get('id')
    user = User.objects.get(id=uid)
    user.delete()
    return Response({'msg': '删除用户成功'})

# 根据用户名搜索用户
@api_view(['GET'])
def getUser(request):
    name = request.GET.get('name')
    # 分页
    page = request.GET.get('page')

    if not name:
        user = User.objects.all()
    else:
        # 模糊查询
        user = User.objects.filter(username__contains=name)
    
    total = user.count()
    # 分页
    paginator = Paginator(user, 5)

    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)

    user_list = getUserInfo(user_list)
    return Response({'msg': '获取用户成功', 'data': user_list, 'total': total})

# 整理用户信息
def getUserInfo(users):
    user_list = []
    for user in users:
        # 获取用户信息，如果没有则创建
        if not UserInfo.objects.filter(user=user).exists():
            UserInfo.objects.create(user=user)
        user_info = UserInfo.objects.get(user=user)
        user_info = {
            'id': user.id, # 用户id
            'name': user.username,
            'email': user.email,
            # 返回 是 或 否
            'is_admin': '是' if user.is_superuser else '否',
            'gender': user_info.gender,
            'phone': user_info.phone
        }
        user_list.append(user_info)
    return user_list
