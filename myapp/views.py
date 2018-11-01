##########################################################################
#                              Imports                                   #
##########################################################################
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ipfsapi # ipfsapi is python api for accessing IPFS from python code
import MySQLdb # MySQL api
import sys
from myapp.models import ledger # model for database
from rest_framework.decorators import api_view	

import configparser

config = configparser.ConfigParser()
config.read('../config.ini')



##########################################################################
#                           IPFS Connection                              #
# ipfsapi.connect:                                                       #
#     Create a new Client instance and connect to the daemon to validate #
#     that its version is supported.                                     #
##########################################################################


# connection
api = ipfsapi.connect(config['ipfs']['ip'], config['ipfs']['port'])


##########################################################################
#                         Database Connectivity                          #
##########################################################################

db = MySQLdb.connect(user=config['mysql']['USER'], db=config['mysql']['NAME'],  passwd=config['mysql']['PASSWORD'], host=config['mysql']['HOST'])

cursor = db.cursor()


##########################################################################
#                              Endpoints                                 #
# 1. index: GET                                                          #
# 2. get_node_status(): GET                                              #
# 3. get_hash(user_id): GET                                              #
# 4. add_file() : POST                                                   #
# 5. delete_file(): POST
##########################################################################

# dummy endpoint for testing
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        response = cursor.execute('SELECT * FROM myapp_ledger')
        return HttpResponse(response, content_type='text/json')


# to get the status of the IPFS server
@api_view(['GET', 'POST'])
def get_node_status(request):
    if request.method == 'GET':
        try:
            node = api.id()
            peers  = api.swarm_peers()
            response = json.dumps([{ 'Error': False, 'Message': "Running", 'Number_of_peers': len(peers["Peers"]), 'ID': node["ID"]}])
        except:
            response = json.dumps([{ 'Error': True, 'Message': "Not Running"}])
        return HttpResponse(response, content_type='text/json')    


"""
	A utility endpoint which returns all the hashes saved under the given user_id
	Method: GET
	Input: user_id
	Returns: list of Hashes
"""
@api_view(['GET', 'POST'])
def get_url(request, user_id):
    if request.method == 'GET':
        try:
            data = ledger.objects.filter(user_id = user_id)
            transaction = []
            for item in data:
                transaction.append(item.url)
            response = json.dumps([{ 'Error': False, "Message": 'Hash found', 'data': transaction}])
        except:
            response = json.dumps([{ 'Error': True, "Message": 'No hash for this user_id'}])
    return HttpResponse(response, content_type='text/json')


# Function to add the details to API database and pin the hash
@api_view(['POST'])
@csrf_exempt
def add_file(request):
    if request.method == 'POST':

        # Get the data sent to the API by Application server
        payload = json.loads( request.body.decode('utf-8') )

        # get the hash in the request
        file_hash = payload["file_hash"]
        
        # What to do when we have the hash already in the database?
        hashExists = ledger.objects.filter(file_hash = file_hash).exists()

        if(hashExists):
            response = json.dumps([{ 'Error': True, "Message": 'HASH already exists!'}])
        else:
            user_id = payload['user_id']
            file_name = payload['file_name']
            file_extension = payload["file_extension"]
            file_type = payload["file_type"]

            # Here I am creating the URL from available data
            url= "cdn.domain.com/" + str(user_id) + "/" + str(file_type) + "/"+ str(file_name)+""+str(file_extension)
        
            # As this is the starting point, file_status will be available
            file_status = True

        
            # TO-DO
            # What to do when the hash is wrong or invalid?

            # api.pin_add may result in error if the given hash is not valid
            try:
                # Pin the given hash in our node
                api.pin_add(file_hash)

                # Once pinned, make the pin_status true 
                pin_status = True
            
            except:
                # This means pinning was not successfull
                # Make pin status false
                pin_status = False    


            # Time to save the data in API db

            try:
                status = ledger.objects.create(user_id = user_id, file_name=file_name, file_extension=file_extension, file_type=file_type, file_hash=file_hash, file_status=file_status, pin_status=pin_status, url=url)
                response = json.dumps([{ 'Error': False, 'Message': 'HASH added successfully!'}])
            except:
            	response = json.dumps([{ 'Error': True, 'Message': 'HASH could not be added!'}])
                

            # response = json.dumps([{ 'Error': user_id }])
    return HttpResponse(response, content_type='text/json')


# Function to delete the given file by unpinning it 
@api_view(['POST'])
@csrf_exempt
def delete_file(request):
    if request.method == 'POST':

        # Get the data sent to the API by Application server
        payload = json.loads( request.body.decode('utf-8') )
        

        user_id = payload['user_id']
        file_name = payload['file_name']
        file_type = payload["file_type"]
        
        try:
            # filter the databse according to the given data
            data = ledger.objects.filter(user_id = user_id).filter(file_name=file_name).filter(file_type=file_type)

            
            if(data[0].pin_status == 0):            
                response = json.dumps([{ 'Error': True, "Message" : "Nothing to unpin" }])
            else:
                # Take the first row and get the hash
                hashString = data[0].file_hash

                # unpin the hash from ipfs node
                pins = api.pin_rm(hashString)

                # take the primary key of the row to update the status
                pk = data[0].id

                # using filter, update the file_status and pin_status of this row
                ledger.objects.filter(id=pk).update(file_status=False, pin_status=False)

                response = json.dumps([{ 'Error': False, "Message": "Unpinned successfully" }])
        except:
            response = json.dumps([{ 'Error': True, "Message": "Failed to unpin" }])
               
            

    return HttpResponse(response, content_type='text/json') 

