import os
import ipfsapi
from django.shortcuts import render
from .models import ipfs_details
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests

def input(request):
    return render(request, 'ipfs/input.html')
@csrf_exempt
def node_status(request):
    try:
        request = requests.get('http://0.0.0.0:5001/webui')
        if request.status_code == 200:
            return HttpResponse("IPFS Daemon is running")
        else:
            return HttpResponse("IPFS Daemon is not running")
    except requests.ConnectionError:  # 404, 500, etc..
        return HttpResponse("IPFS Daemon is not running")

@csrf_exempt
def result_upload(request):
    if request.method == 'POST':
        ipfs_entry = ipfs_details()
        user_id = request.POST.get('User_Id', None)
        file_type = request.POST.get('File_type', None)
        file_name = request.POST.get('File_name', None)
        file = request.FILES['File']
        try:
            request = requests.get('http://0.0.0.0:5001/webui')
            if request.status_code == 200:
                api = ipfsapi.connect('0.0.0.0', 5001)            
        except requests.ConnectionError:  # 404, 500, etc..
            return HttpResponse("IPFS Daemon is not running")        
        
        res = api.add(file)
        hash = res['Hash']
        size = res['Size']
        status = os.system('ipfs pin add ' + hash)
        ipfs_entry.User_ID = user_id
        ipfs_entry.File_Name = file_name
        ipfs_entry.File_Type = file_type
        ipfs_entry.File_Hash = hash
        ipfs_entry.File_Size = size
        ipfs_entry.URL = "https://gateway.ipfs.io/ipfs/" + hash + "/"
        if status == 0:
            ipfs_entry.Pin_Status = "Added"
        else:
            ipfs_entry.Pin_Status = "Not added"
        ipfs_entry.save()
        data = {}
        data['ipfs user id'] = user_id
        data['file name'] = file_name
        data['file type'] = file_type
        data['hash'] = hash
        data['pin status'] = ipfs_entry.Pin_Status
        data['url'] = ipfs_entry.URL
        os.system('ipfs swarm peers|wc -l > ' + hash)
        file = open(hash, "r")
        for line in file:
            data['No. of peers'] = line[:-1]
            break
        os.remove(hash)
        json_data = json.dumps(data, sort_keys=True, indent=4)
        return HttpResponse(json_data)
    return HttpResponse("not a post request")


@csrf_exempt
def hash_upload(request):
    ans = "post works well"
    if request.method == 'POST':
        ipfs_entry = ipfs_details()
        user_id = request.POST.get('User_Id', None)
        file_type = request.POST.get('File_type', None)
        file_name = request.POST.get('File_name', None)
        hash = request.POST.get('File_hash', None)
        status = os.system('ipfs pin add ' + hash)
        ipfs_entry.User_ID = user_id
        ipfs_entry.File_Name = file_name
        ipfs_entry.File_Type = file_type
        ipfs_entry.File_Hash = hash

        ipfs_entry.URL = "https://gateway.ipfs.io/ipfs/" + hash + "/"
        if status == 0:
            ipfs_entry.Pin_Status = "Added"
        else:
            ipfs_entry.Pin_Status = "Not added"
        ipfs_entry.save()
        data = {}
        data['ipfs user id'] = user_id
        data['file name'] = file_name
        data['file type'] = file_type
        data['hash'] = hash
        data['pin status'] = ipfs_entry.Pin_Status
        data['url'] = ipfs_entry.URL
        os.system('ipfs swarm peers|wc -l > ' + hash)
        file = open(hash, "r")
        for line in file:
            data['No. of peers'] = line[:-1]
            break
        os.remove(hash)
        json_data = json.dumps(data, sort_keys=True, indent=4)
        return HttpResponse(json_data)

    return HttpResponse("not a post request")


@csrf_exempt
def result_delete(request):
    entry = None
    if request.method == 'POST':
        ipfs_entry = ipfs_details.objects.all()
        user_id = request.POST.get('User_Id', None)
        file_hash = request.POST.get('File_hash', None)
        for i in ipfs_entry:
            if i.User_ID == user_id and i.File_Hash == file_hash:
                entry = i
                break
        if entry is not None:
            data = {}
            data['ipfs user id'] = user_id
            data['file name'] = entry.File_Name
            data['pin status'] = entry.Pin_Status
            status = os.system('ipfs pin rm ' + entry.File_Hash)
            if status == 0:
                entry.Pin_Status = "Unpinned"
                entry.save()
                data['pin status'] = entry.Pin_Status
                json_data = json.dumps(data, sort_keys=True, indent=4)
                return HttpResponse(json_data)
            json_data = json.dumps(data, sort_keys=True, indent=4)
            return HttpResponse(json_data)
        return HttpResponse("Data not found")

    return HttpResponse("Not a post request")
