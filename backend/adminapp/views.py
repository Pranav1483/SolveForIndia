import mimetypes
from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from rest_framework.parsers import JSONParser
from rest_framework import status
from adminapp.serializers import ReportSerializer
from userapp.models import Block, Reports
from rest_framework.decorators import api_view
import json
from hashlib import sha256
from django.db import IntegrityError
from datetime import datetime
import qrcode
import requests
from requests.structures import CaseInsensitiveDict
import pathlib
import os

QR_DIR = os.path.join(pathlib.Path(__file__).resolve().parent.parent, 'qrcodes')
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

@api_view(['POST'])
def create_product(request):
    data = json.loads(request.body.decode("utf-8"))
    pd_id = data['pd_id']
    batch_id = data['batch_id']
    timestamp = str(datetime.now())
    product_details = data['product_details']
    if pd_id and batch_id and timestamp and product_details:
        tmp = Hashing(pd_id, batch_id, timestamp, product_details, 0, 0)
        block_obj = Block(owner='N/A', num=0, pd_id=tmp.pd_id, batch_id=tmp.batch_id, timestamp=tmp.timestamp, product_details=tmp.product_details, hash_code=tmp.hash)
        try:
            block_obj.save()
            hashcode = block_obj.hash_code
            img = qrcode.make(hashcode)
            filename = hashcode + '.png'
            filepath = os.path.join(QR_DIR, filename)
            img.save(filepath)
            return JsonResponse({'msg': 'Product Added Successfully', 'path': filepath})
        except IntegrityError:
            return JsonResponse({'msg': 'Similiar Product Exists'})
    else:
        return JsonResponse({'msg': 'NULL'})

@api_view(['GET'])
def reports(request):
    res = {'reports': []}
    for obj in Reports.objects.all():
        res['reports'].append(ReportSerializer(obj).data)
    return JsonResponse(res)

@api_view(['GET'])
def indv_reports(request, id):
    res = {'reports': []}
    for obj in Reports.objects.all():
        if obj.username == id:
            res['reports'].append(ReportSerializer(obj).data)
    return JsonResponse(res)


def login(request):
    template = loader.get_template('admin_login.html')
    return HttpResponse(template.render({}, request))


def logincheck(request):
    if not request.session.get('Logged', False):
        pwd = request.POST.get('Password', False)
        if not pwd or pwd != 'admin':
            return HttpResponseRedirect(reverse('login'))
        request.session['Logged'] = 1
    template = loader.get_template('admin_dashboard.html')
    return HttpResponse(template.render({}, request))   


def show_reports(request):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    username = request.POST.get('Uname', False)
    if username:
        # if request.is_secure():
        #     security = 'https://'
        # else:
        #     security = 'http://'
        # host = request.get_host()
        # url = security + host + '/adminapp/api/admin/reports/' + username
        # res = json.loads(get_data(url))
        try:
            res = Reports.objects.get(username=username)
        except Reports.DoesNotExist:
            res = {}
        template = loader.get_template('admin_reports.html')
        return HttpResponse(template.render({'rpts': res}, request))
    else:
        # if request.is_secure():
        #     security = 'https://'
        # else:
        #     security = 'http://'
        # host = request.get_host()
        # url = security + host + '/adminapp/api/admin/reports'
        # res = json.loads(get_data(url))
        res = Reports.objects.all().values()
        template = loader.get_template('admin_reports.html')
        return HttpResponse(template.render({'rpts': res}, request))
    

def createpdt(request):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    template = loader.get_template('admin_createpdt.html')
    return HttpResponse(template.render({}, request))


def createpdtfn(request):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    pd_id = request.POST.get('pd_id', False)
    batch_id = request.POST.get('batch_id', False)
    item = request.POST.get('item', False)
    size = request.POST.get('size', False)
    colour = request.POST.get('colour', False)
    data = {'pd_id': pd_id, 'batch_id': batch_id, 'product_details': {'Item': item, 'Size': size, 'Colour': colour}}
    # if request.is_secure():
    #         security = 'https://'
    # else:
    #     security = 'http://'
    # host = request.get_host()
    # url = security + host + '/adminapp/api/admin/product/'
    # res = json.loads(post_data(url, data))
    pd_id = data['pd_id']
    batch_id = data['batch_id']
    timestamp = str(datetime.now())
    product_details = data['product_details']
    if pd_id and batch_id and timestamp and product_details:
        tmp = Hashing(pd_id, batch_id, timestamp, product_details, 0, 0)
        block_obj = Block(owner='N/A', num=0, pd_id=tmp.pd_id, batch_id=tmp.batch_id, timestamp=tmp.timestamp, product_details=tmp.product_details, hash_code=tmp.hash)
        try:
            block_obj.save()
            hashcode = block_obj.hash_code
            img = qrcode.make(hashcode)
            filename = hashcode + '.png'
            filepath = os.path.join(QR_DIR, filename)
            img.save(filepath)
            res = {'msg': 'Product Added Successfully', 'path': filepath}
        except IntegrityError:
            res = {'msg': 'Similiar Product Exists'}
    else:
        res = {'msg': 'NULL'}
    if res['msg'] in ['Similiar Product Exists', 'NULL']:
        return HttpResponseRedirect(reverse('createpdt'))
    filepath = res['path']
    path = open(filepath, 'rb')
    mime_type , _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=img.png"
    return response 


def showpdt(request):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    username = request.POST.get('Uname', False)
    if username:
        res = {'blocks': []}
        for obj in Block.objects.all():
            if obj.owner == username:
                res['blocks'].append(obj)
        template = loader.get_template('admin_products.html')
        return HttpResponse(template.render({'block': res['blocks']}, request))
    else:
        res = {'blocks': []}
        for obj in Block.objects.all():
            res['blocks'].append(obj)
        template = loader.get_template('admin_products.html')
        return HttpResponse(template.render({'block': res['blocks']}, request))


def deletepdt(request, id):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    try:
        obj = Block.objects.get(id=id)
        f = pathlib.Path("qrcodes/" + obj.hash_code + ".png")
        f.unlink(missing_ok=True)
        obj.delete()
        return HttpResponseRedirect(reverse('showpdt'))
    except Block.DoesNotExist:
        return HttpResponseRedirect(reverse('showpdt'))


def delete_reports(request, id):
    if not request.session.get('Logged', False):
        return HttpResponseRedirect(reverse('login'))
    try:
        obj = Reports.objects.get(id=id)
        obj.delete()
        return HttpResponseRedirect(reverse('show_reports'))
    except Block.DoesNotExist:
        return HttpResponseRedirect(reverse('show_reports'))


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('login'))


def back(request):
    return HttpResponseRedirect(reverse('dashboard'))
    





        
        
    
    

