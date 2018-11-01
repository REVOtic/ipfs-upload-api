# Django Rest Api For IPFS Storage
REST API written in Django for connecting to the IPFS nodes and basic operations

***

## Endpoints in this API

1. / : GET
2. get_node_status : GET
3. /<user_id>: GET
4. /add : POST
5. /delete: POST
---
## Servers to make this work

1. IPFS server
2. MySQL server
3. API server

## How to start those servers

### IPFS Server
`ipfs daemon`

### MySQL server
Make sure you have installed the mysql server and performed the migrations for my model (i.e. ledger)

#### To start the server
`sudo /etc/init.d/mysql start`

### To access the mysql shell
`/usr/bin/mysql -u root -p`

### API server
`python3 manage.py runserver`

***

## Endpoint Details (Only Important)
All our APIs take `JSON` data
### 1. Adding Files to IPFS
For this we have the endpoint: `/add`
This endpoint follows `POST` method (Try to access it using Postman)

#### It takes following parameters with specified name
1. `user_id` (integer) : id of the user sending the request 
2. `file_name` (string) : name of the file added by the user
3. `file_extension` (string) : extention of the added file (for example: in case of images it can be .jpeg or .png)
4. `file_type` (string) : Type of the file being added by the user (This can take values like image, video etc)
5. `file_hash`  (string) : hash of the file added by the user

#### Response
This returns `Error` = `False` after adding the file successfully to API database and Pinning it on IPFS node
Else it returns `Error` = `True` on errors.

Along with boolean status it also return `Message` with every response which indicates the status

### 2. Deleting Files from the IPFS
For this we have the endpoint: `/delete`
This endpoint follows `POST` method (Try to access it using Postman)

#### It takes following parameters with specified name
1. `user_id` (integer) : id of the user sending the request 
2. `file_name` (string) : name of the file to be deleted 
4. `file_type` (string) : Type of the file being deleted by the user (This can take values like image, video etc)

#### Response
This returns `Error` = `False` after deleting the file successfully to API database and unpinning it on IPFS node
Else it returns `Error` = `True` on errors.

Along with boolean status it also return `Message` with every response which indicates the status

### 3. Node Status
For this we have the endpoint: `/get_node_status`
This endpoint follows `GET` method.

#### It takes following parameters with specified name
None

#### Response
This returns `Error` = `False` and `ID` of the Node after successfully getting the status of the node
Else it returns `Error` = `True` on errors.

Along with boolean status it also return `Message` with every response which indicates the status

---

### Useful Links
1. [Django Models Documentations](https://docs.djangoproject.com/en/2.1/topics/db/queries/)
2. [Client API Reference](https://ipfs.io/ipns/QmZ86ow1byeyhNRJEatWxGPJKcnQKG7s51MtbHdxxUddTH/Software/Python/ipfsapi/api_ref.htmlsuccessfully)

