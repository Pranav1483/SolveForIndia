from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from userapp.models import Block, User, Reports
from userapp.serializers import BlockSerializer, UserSerializer
from rest_framework.decorators import api_view
import json
from hashlib import sha256
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import requests
from requests.structures import CaseInsensitiveDict
from django.conf import settings
from django.core.mail import send_mail
import random
from django.middleware import csrf
import qrcode
import cv2
from datetime import datetime

class Hashing:
    
    def __init__(self, pd_id, batch_id, timestamp, product_details, block_num, prev_hash) -> None:
        self.block_num = block_num
        self.pd_id = pd_id
        self.batch_id = batch_id
        self.timestamp = timestamp
        self.product_details = product_details
        self.hash = self.compute_hash()
        self.prev_hash = prev_hash
        
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


def post_data(url, data):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data=data)
    return resp.text

def get_data(url):
    resp = requests.get(url)
    return resp.text


@api_view(['GET'])
def get_product(request, id):
    try:
        block = Block.objects.get(hash_code=id)
    except Block.DoesNotExist:
        return JsonResponse({'msg': 'Fake Product'})
    
    if block.owner != 'N/A':
        if request.method == 'GET':
            tmp = Hashing(block.pd_id, block.batch_id, block.timestamp, block.product_details, block.num, 0)
            if tmp.hash == block.hash_code:
                pdt_serializer = BlockSerializer(block)
                res = pdt_serializer.data
                res['msg'] = 'Success'
                return JsonResponse(res)
            else:
                return JsonResponse({'msg': 'Fake Product'})
    if block.owner == 'N/A':
        if request.method == 'GET':
            return JsonResponse({'msg': 'Register this ' + str(block.product_details['Item']) + ' to access more details'})

@api_view(['GET'])
def get_user(request, id):
    try:
        user = User.objects.get(username=id)
    except User.DoesNotExist:
        return JsonResponse({'msg': 'No User Found'})
    user_serializer = UserSerializer(user)
    res = user_serializer.data
    pdts = {}
    num = 0
    for i in Block.objects.all():
        if i.owner == user.username:
            pdts[num] = {'product_details': i.product_details, 'timestamp': i.timestamp}
            num += 1
    res['products'] = pdts
    res['msg'] = 'Success'
    return JsonResponse(res)

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        user_name = received_json_data['username']
        first_name = received_json_data['first_name']
        last_name = received_json_data['last_name']
        email = received_json_data['email']
        password = received_json_data['password']
        mobile = received_json_data['mobile']
        if user_name and first_name and last_name and email and password and mobile:
            try:
                user = User(username=user_name, first_name=first_name, last_name=last_name, email=email, password=sha256(password.encode()).hexdigest(), mobile=mobile)
                user.save()
                return JsonResponse({'msg': 'User Registered Successfully'})
            except IntegrityError:
                return JsonResponse({'msg': 'Username or Email Already in Use'})
        else:
            return JsonResponse({"msg": "Please Enter Your Details"})

@api_view(['POST'])
def add_product(request):
    data = json.loads(request.body.decode('utf-8'))
    idx = data['hash']
    username = data['username']
    if idx and username:
        try:
            user_obj = User.objects.get(username=username)
            block_obj = Block.objects.get(hash_code=idx)
            if block_obj.owner == 'N/A':
                tmp = Hashing(block_obj.pd_id, block_obj.batch_id, block_obj.timestamp, block_obj.product_details, 0, 0)
                if tmp.hash == block_obj.hash_code:
                    block_obj.owner = username
                    block_obj.save()
                    return JsonResponse({'msg': 'Product Added Successfully'})
                else:
                    return JsonResponse({'msg': 'Not Authentic'})
            else:
                return JsonResponse({'msg': 'Product already Registered'})
        except (Block.DoesNotExist):
            return JsonResponse({'msg': 'Not Authentic'})
        except User.DoesNotExist:
            return JsonResponse({'msg': 'No User Found'})
    else:
        return JsonResponse({'msg': 'Upload Image'})

@api_view(['POST'])
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']
    if not username or not password:
        return JsonResponse({'msg': 'Please Enter Username & Password'})
    try:
        user = User.objects.get(username=username, password=sha256(password.encode()).hexdigest())
        user_serializer = UserSerializer(user)
        res = user_serializer.data
        pdts = []
        for i in Block.objects.all():
            if i.owner == user.username:
                pdts.append({'product_details': i.product_details, 'timestamp': i.timestamp})
        res['products'] = pdts
        res['msg'] = 'Successful'
        return JsonResponse(res)
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'msg': 'Wrong Password !'})
        except User.DoesNotExist:
            return JsonResponse({'msg': 'User not registered !'})

@api_view(['POST'])
def report_product(request):
    data = json.loads(request.body.decode('utf-8'))
    user = data['username']
    location_of_purchase = data['location']
    report = data['report']
    if user and location_of_purchase and report:
        timestamp = str(datetime.now())
        obj = Reports(username=user, loc=location_of_purchase, report=report, timestamp=timestamp)
        obj.save()
        return JsonResponse({'msg': 'Report Successful'})
    else:
        return JsonResponse({'msg': 'Type Your Complaint'})

@api_view(['POST'])
def send_otp(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    otp = data['otp']
    if not email or not otp:
        return JsonResponse({'msg': 'NULL'})
    try:
        obj = User.objects.get(email=email)
        send_mail('Reset Password', 'Here is your OTP to reset your password :\n' + otp, settings.EMAIL_HOST_USER, [obj.email,])
        return JsonResponse({'msg': 'Successful'})
    except User.DoesNotExist:
        return JsonResponse({'msg': 'No User Exists'})

@api_view(['POST'])
def check_otp(request):
    data = json.loads(request.body.decode('utf-8'))
    otp_from_user = data['otp_from_user']
    otp = data['otp']
    if not otp_from_user or not otp:
        return JsonResponse({'msg': 'Type OTP'})
    if otp_from_user != otp:
        return JsonResponse({'msg': 'OTP Mismatch'})
    else:
        return JsonResponse({'msg': 'Success'})

@api_view(['POST'])
def edit_password(request):
    data = json.loads(request.body.decode('utf-8'))
    new_password = data['new_password']
    email = data['email']
    if not new_password or not email:
        return JsonResponse({'msg': 'Type Password'})
    obj = User.objects.get(email=email)
    obj.password = sha256(new_password.encode()).hexdigest()
    obj.save()
    return JsonResponse({'msg': 'Success'})


# Templates

def dashboard(request):
    username = request.POST.get('Uname', False)
    password = request.POST.get('Password', False)
    if username and password:
        request.session['Uname'] = username
        request.session['Password'] = password
    else:
        username = request.session.get('Uname', False)
        password = request.session.get('Password', False)
    data = {"username": username, "password": password}
    username = data['username']
    password = data['password']
    if not username or not password:
        res = {'msg': 'NULL'}
    else:
        try:
            user = User.objects.get(username=username, password=sha256(password.encode()).hexdigest())
            user_serializer = UserSerializer(user)
            res = user_serializer.data
            pdts = []
            for i in Block.objects.all():
                if i.owner == user.username:
                    pdts.append({'product_details': i.product_details, 'timestamp': i.timestamp})
            res['products'] = pdts
            res['msg'] = 'Successful'
        except User.DoesNotExist:
            res = {'msg': 'Credentials do not match'}
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/login/'
    # res = json.loads(post_data(url, data))
    if res['msg'] == 'NULL':
        return HttpResponseRedirect(reverse('user_login'))
    elif res['msg'] == 'Credentials do not match':
        return HttpResponseRedirect(reverse('user_login'))
    template = loader.get_template('user_dashboard.html')
    context = {
        'obj': res
    }
    return HttpResponse(template.render(context, request))

def user_login(request):
    template = loader.get_template('user_login.html')
    return HttpResponse(template.render({}, request))

def register(request):
    request.session.flush()
    template = loader.get_template('user_register.html')
    return HttpResponse(template.render({}, request))

def registration(request):
    username = request.POST.get('Uname', False)
    fname = request.POST.get('Fname', False)
    lname = request.POST.get('Lname', False)
    email = request.POST.get('Email', False)
    password = request.POST.get('Password', False)
    mobile = request.POST.get('Mobile', False)
    request.session.flush()
    data = {'username': username, 'first_name': fname, 'last_name': lname, 'password': password, 'email': email, 'mobile': mobile}
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/register/'
    # res = json.loads(post_data(url, data))
    user_name = data['username']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']
    mobile = data['mobile']
    if user_name and first_name and last_name and email and password and mobile:
        try:
            user = User(username=user_name, first_name=first_name, last_name=last_name, email=email, password=sha256(password.encode()).hexdigest(), mobile=mobile)
            user.save()
            res = {'msg': 'User Registered Successfully'}
        except IntegrityError:
            res = {'msg': 'Username or Email already in use'}
    else:
        res = {"msg": "NULL"}
    if res['msg'] == 'Username or Email already in use' or res['msg'] == 'NULL':
        return HttpResponseRedirect(reverse('user_register'))
    return HttpResponseRedirect(reverse('user_login'))

def report_page(request):
    if not request.session.get('Uname', False):
        return HttpResponseRedirect(reverse('user_login'))
    template = loader.get_template('user_report.html')
    return HttpResponse(template.render({}, request))

def report_page_submit(request):
    if not request.session.get('Uname', False):
        return HttpResponseRedirect(reverse('user_login'))
    user = request.session.get('Uname', False)
    loc = request.POST.get('Location', False)
    report = request.POST.get('Report', False)
    data = {'username': user, 'location': loc, 'report': report}
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/report/'
    # res = json.loads(post_data(url, data))
    user = data['username']
    location_of_purchase = data['location']
    report = data['report']
    if user and location_of_purchase and report:
        obj = Reports(username=user, loc=location_of_purchase, report=report)
        obj.save()
        res = {'msg': 'Report Successful'}
    else:
        res = {'msg': 'NULL'}
    if res['msg'] == 'NULL':
        return HttpResponseRedirect(reverse('report_page'))
    return HttpResponseRedirect(reverse('user_dashboard'))

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('user_login'))

def forgotpwd(request):
    request.session.flush()
    template = loader.get_template('user_forgotpwd.html')
    return HttpResponse(template.render({}, request))


def forgotpwd_mail(request):
    email = request.session.get('email', False)
    otp = request.session.get('otp', False)
    if not otp:
        otp = str(random.randint(100000, 999999))
    if not email:
        email = request.POST.get('email', False)
    data = {'email': email, 'otp': otp}
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/sendotp/'
    # res = json.loads(post_data(url, data))
    email = data['email']
    otp = data['otp']
    if not email or not otp:
        res = {'msg': 'NULL'}
    else:
        try:
            obj = User.objects.get(email=email)
            send_mail('Reset Password', 'Here is your OTP to reset your password :\n' + otp, settings.EMAIL_HOST_USER, [obj.email,])
            res = {'msg': 'Successful'}
        except User.DoesNotExist:
            res = {'msg': 'No User Exists'}
    if res['msg'] == 'No User Exists':
        return HttpResponseRedirect(reverse('forgotpwd'))
    request.session['email'] = email
    request.session['otp'] = otp
    template = loader.get_template('user_otpform.html')
    return HttpResponse(template.render({}, request))


def verify_otp(request):
    if not request.session.get('email', False) or not request.session.get('otp', False):
        return HttpResponseRedirect(reverse('forgotpwd'))
    otp_from_user = request.POST.get('otp', False)
    # data = json.dumps({'otp_from_user': otp_from_user, 'otp': request.session['otp']})
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/verifyotp/'
    # print(post_data(url, data, request))
    # res = json.loads(post_data(url, data, request))
    res = {}
    if not otp_from_user:
        res['msg'] = 'NULL'
    elif otp_from_user != request.session['otp']:
        res['msg'] = 'OTP Mismatch'
    else:
        res['msg'] = 'Successful'
    if res['msg'] == 'NULL' or res['msg'] == 'OTP Mismatch':
        return HttpResponseRedirect(reverse('forgotpwd_mail'))
    template = loader.get_template('user_newpwdform.html')
    return HttpResponse(template.render({}, request))


def change_password(request):
    if not request.session.get('email', False):
        return HttpResponseRedirect(reverse('forgotpwd'))
    new_password = request.POST.get('password', False)
    # data = json.dumps({'new_password': new_password, 'email': request.session['email']})
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/changepwd/'
    # res = json.loads(post_data(url, data))
    res = {}
    if not new_password:
        res['msg'] = 'NULL'
    else:
        obj = User.objects.get(email=request.session['email'])
        obj.password = sha256(new_password.encode()).hexdigest()
        obj.save()
        res['msg'] = 'Successful'
    if res['msg'] == 'NULL':
        return HttpResponseRedirect(reverse('forgotpwd_mail'))
    return HttpResponseRedirect(reverse('user_login'))


def resend_otp(request):
    request.session.pop('otp')
    print(request.session.get('email', False))
    return HttpResponseRedirect(reverse('forgotpwd_mail'))


def addproduct(request):
    if not request.session.get('Uname', False):
        return HttpResponseRedirect(reverse('user_login'))
    template = loader.get_template('user_addproduct.html')
    return HttpResponse(template.render({}, request))


def addproduct_fn(request):
    if not request.session.get('Uname', False):
        return HttpResponseRedirect(reverse('user_login'))
    img = request.FILES.get('myFile', False)
    if not img:
        return HttpResponseRedirect(reverse('addproductpage'))
    with open('qrcodes/testimg.png', 'wb') as f:
        f.write(img.read())
    img = cv2.imread("qrcodes/testimg.png")
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(img)
    data = {'username': request.session['Uname'], 'hash': val}
    # if request.is_secure():
    #     security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/userapp/api/user/addpdt/'
    # res = json.loads(post_data(url, data))
    idx = data['hash']
    username = data['username']
    if idx and username:
        try:
            user_obj = User.objects.get(username=username)
            block_obj = Block.objects.get(hash_code=idx)
            if block_obj.owner == 'N/A':
                tmp = Hashing(block_obj.pd_id, block_obj.batch_id, block_obj.timestamp, block_obj.product_details, 0, 0)
                if tmp.hash == block_obj.hash_code:
                    block_obj.owner = username
                    block_obj.save()
                    res = {'msg': 'Product Added Successfully'}
                else:
                    res = {'msg': 'Not Authentic'}
            else:
                res = {'msg': 'Product already Registered'}
        except Block.DoesNotExist:
            res = {'msg': 'Not Authentic'}
        except User.DoesNotExist:
            res = {'msg': 'No User Found'}
    else:
        res = {'msg': 'NULL'}
    if res['msg'] in ['Not Authentic', 'Product already Registered', 'NULL']:
        return HttpResponseRedirect(reverse('addproductpage'))
    else:
        return HttpResponseRedirect(reverse('user_dashboard'))





    
    

    
    












     
    
        

        
    
    

