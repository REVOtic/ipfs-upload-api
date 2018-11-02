# Master Branch
## Input Output Structure:
#### 1.Upload a file: 
You need to enter your ipfs id, file name, file type and the file itself. The file is stored in ipfs. The output shows all the values that are stored in the database

 - User Id
 - File name and extension
 - File type
 - File hash
 - File upload and File Pin status
 - URL to gateway.ipfs.io/ipfs/hash where the image can be seen for now. I will make the required changes here. 
 
#### 1.Delete a file: 
You need to enter your ipfs id, file name and the file type that you wnt to delete. The file will be unpinned from the local repository.The output shows all the values that are stored in the database

 - User Id
 - File name and extension
 - File type
 - File hash
 - File upload and File Pin status

# Workflow
#### File Upload
  The given file is stored in ipfs using the ipfs add command and is also pinned to the local repository. The user is then given a hash of the file that is stored. All the data is being stored in the local database for now. The user is also shown a dummy url where he/she can view the uploaded file for now.
#### File Delete
  The given file is unpinned from the local repository and the data is accordingly changed in the database. The dummy url is however still active(Will have to make the necessary changes here).

# Command_Line Branch

Two extra features are added. The user can check if ipfs daemon is running or not. Also, the user can enter a file hash and the file will be pinned to the local repository.
 Another small change is made in the file delete portion. Now, you need to enter the file hash and the file will be deleted.
 
 The api can also be accessed from the command line using the following commands:
 
 ## Check the node status
 curl -X POST http://13.66.133.71:8000/node_status
 ## Upload a file
 curl -X POST -F 'User_Id=QmZtmKSApr3v9pxY95dd25kq5BRMF5saLtRwTBTuazhpjU' -F 'File_type=picture' -F 'File_name=cat.jpg' -F 'File=@cat.jpg'  13.66.133.71:8000/result_upload
 ## Upload a file with hash
 curl -X POST -F 'User_Id=QmZtmKSApr3v9pxY95dd25kq5BRMF5saLtRwTBTuazhpjU' -F 'File_type=picture' -F 'File_name=cat.jpg' -F 'File_hash=Qmd286K6pohQcTKYqnS1YhWrCiS4gz7Xi34sdwMe9USZ7u' 13.66.133.71:8000/hash_upload
 ## delete a file
 curl -X POST -F 'User_Id=QmZtmKSApr3v9pxY95dd25kq5BRMF5saLtRwTBTuazhpjU' -F 'File_hash=QmWbzGVtKmB8zZ8znqBqK1vJkQfHKL9iQ3f7xdcvSPiEWG' 13.66.133.71:8000/result_delete
 
 The result can be seen in a json format