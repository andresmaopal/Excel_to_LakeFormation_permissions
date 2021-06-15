'''
Lambda Python 3.8 
Excel to Lake Formation Bulk Permissions
Use together with provided Lambda Layer and S3 Put trigger over the desired bucket

'''
import json
import awswrangler as wr
import pandas as pd
import boto3
import uuid
import sys
import re
import numpy
import math
import urllib.parse


def lambda_handler(event, context):
    
    print("Start Reading New Excel file from S3...")
    
    #Get the current s3 Bucket and Key, triggered by S3 PUT Trigger
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    #Validate S3 bucket and key
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        
    except Exception as e:
        print(e)
        print('ERROR getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    
    #Create input Excel path
    excel_path = "s3://"+bucket+"/"+key
    print("READING S3 file from "+excel_path)
    print("-----------------------------------")
    
    client = boto3.client('sts')
    
    #Read Excel
    df = wr.s3.read_excel(excel_path, header=0, sheet_name="Sheet1")
    df.dropna(axis=0, thresh=4, inplace=True) 
    df.fillna("", inplace=True)
    
    #Declare Lists for GRANT and REVOKE entries
    _EntriesGrant = []
    _EntriesRevoke = []
    
    #Loop to iterate to all DataFrame rows (coming from Excel rows) 
    
    for index, _df in df.iterrows():


        #If the ResourceElements is a table(colum1,colum2) definition replace "," with ";" within parenthesis to avoid conflicts
        if "(" in _df["ResourceElements"]:

            _df["ResourceElements"] = re.sub(r'\(.*?\)', replace, _df["ResourceElements"])
        
        list_elements = _df["ResourceElements"].split(",")
        num_tables = len(list_elements)

            
        # Get Number of Principals to give permission   
        
        if _df["TargetPrincipals"] != "":
            
            list_principals = _df["TargetPrincipals"].split(",")
            num_principals = len(list_principals)
            
        else: 
            print("Error: need at least 1 target principal in TargetPrincipals")
            return None
        
        #Loop to iterate each TargetPrincipals (principals) and each ResourceElements (elements) within a row that was separated by comma
        for principal in list_principals:
            for element in list_elements:
            
                _Resource = {}

                #-Build DataLakePrincipals Object
                
                if principal != "":
                    
                    principal = principal.strip()
                    element = element.strip()
                    
                    client = boto3.client('sts')
                    account_number = client.get_caller_identity()['Account']
                
                    #If element is a USER
                    if "u:" in principal:
                        
                        pr = principal.split(":",1)
                        pr = pr[1]

                        _Principal = {"DataLakePrincipalIdentifier": "arn:aws:iam::" + account_number + ":user/" + pr}
                        
                    #If element is a IAM_ALLOWED_PRINCIPALS
                    elif principal == 'IAM_ALLOWED_PRINCIPALS': 
                        _Principal = {"DataLakePrincipalIdentifier": principal }
                    
                    #If element is an ACCOUNT    
                    elif "a:" in principal:
                        a = principal.split(":")
                        a_account = a[1]
                        _Principal = {"DataLakePrincipalIdentifier": a_account }
                        
                    #If element is an ORGANIZATION     
                    elif "o:" in principal:
                        o = principal.split(":")
                        o_account = o[1]
                        o_id = o[2]
                        _Principal = {"DataLakePrincipalIdentifier": "arn:aws:organizations::" + o_account + ":organization/" + o_id}
                    
                    #If element is an ORGANIZATION UNIT  
                    elif "ou:" in principal:
                        ou = principal.split(":")
                        ou_account = ou[1]
                        ou_id = ou[2]
                        _Principal = {"DataLakePrincipalIdentifier": "arn:aws:organizations::" + ou_account + ":ou/" + ou_id}
                                                
                    #If element is ROLE (without any prefix)  
                    else:
                        _Principal = {"DataLakePrincipalIdentifier": "arn:aws:iam::" + account_number + ":role/" + principal}
                        
                        
                else: 
                    print("ERROR: At least one DataLakePrincipals is expected ")
                    return None

                #-Build Resource Object
                
                if _df["ResourceLocationDatabase"] != "":
                    
                    _Resource = {} 
                    
                    db = _df["ResourceLocationDatabase"]
                    
                    #If ResourceLocationDatabase is an S3 Path  
                    if db.startswith("s3://"):
                        
                        dloc = db.split("s3://",1)
                        s3_arn = "arn:aws:s3:::" + dloc[1]
                        
                        _Resource['DataLocation'] = {"CatalogId": client.get_caller_identity()['Account'], "ResourceArn": s3_arn }
                        
                    #If ResourceLocationDatabase is a Glue Catalog Object 
                    else:
                        
                         #-Table/Tag build
                        if _df["ResourceElements"] != "":
        
                            #Verify if the Element is a Tag
                            if ":" in element:
                                
                                tg = element.split(":", 1)
                                if len(tg) == 2:
                                    
                                    _Resource['Database'] = {"CatalogId": client.get_caller_identity()['Account'], "Name": db}
                                    _Resource['LFTag'] = {"CatalogId": client.get_caller_identity()['Account'], 'TagKey': tg[0], "TagValues": [ tg[1] ]   }
        
                                else: 
                                    print("Error: At least one key:value Tag policy is expected")
                                    return None
                                
                            #Verify if element is All tables * wildcard
                            elif element == "*":
                                
                                _Resource['Table'] = { "DatabaseName": db, "TableWildcard": {} }
                                    
                            #Verify if element is Tables with Columns definition
                            elif "(" in element:
                                
                                tcol = element.split("(")
                                
                                if len(tcol) == 2:
                                        
                                    tcol[1] = tcol[1].replace(")","")
                                    cols_string = tcol[1]
                                    tcol[1] = tcol[1].replace("-","")
                                    lcols = tcol[1].split(";")
        
                                    account_num = client.get_caller_identity()['Account']
        
                                        
                                    if cols_string.startswith("-"):
                                        _Resource['TableWithColumns'] = {"CatalogId": account_num ,"DatabaseName": db, "Name": tcol[0], "ColumnWildcard": { 'ExcludedColumnNames': lcols } } 
                                    else:
                                        _Resource['TableWithColumns'] = {"CatalogId": account_num ,"DatabaseName": db, "Name": tcol[0], "ColumnNames": lcols }
                                        
                                        
                                else: 
                                    print("ERROR: A Table with Columns in ResourcePermissions is expected with the format: tablename(col1,col2...) ")
                                    return None
                                
                            #Verify if element is Table WITHOUT Columns 
                            else:
                                
                                _Resource['Table'] = {"CatalogId": client.get_caller_identity()['Account'], "DatabaseName": db, "Name": element }
        
        
                        else:
                            
                            #-Database build
        
                            _Resource['Database'] = {"CatalogId": client.get_caller_identity()['Account'], "Name": db}

                                        
                else:
                    print("Error, ResourceLocationDatabase can not be empty")
                    return None
                        

                # Permissions
                
                _Permissions = []
                
                if _df["ResourcePermissions"] != "":

                    l_permission = []
                   
                    pcol = _df["ResourcePermissions"].split(",")
                   
                    for perm in pcol:
                   
                        if perm == "*":
                            l_permission.append("ALL") 
                        if perm == "S":
                            l_permission.append("SELECT")
                        if perm == "I":
                            l_permission.append("INSERT")
                        if perm == "A":
                            l_permission.append("ALTER")
                        if perm == "DR":
                            l_permission.append("DROP")
                        if perm == "DL":
                            l_permission.append("DELETE")
                        if perm == "DS":
                            l_permission.append("DESCRIBE")
                        if perm == "CT":
                            l_permission.append("CREATE_TABLE")
                        if perm == "CD":
                            l_permission.append("CREATE_DATABASE")
                        if perm == "DLA":
                            l_permission.append("DATA_LOCATION_ACCESS")
                        if perm == "AT":
                            l_permission.append("ASSOCIATE_TAG")
                        if perm == "CTG":
                            l_permission.append("CREATE_TAG")
                            
                    _Permissions = l_permission
                            
                # Grant Permissions
                
                _PermissionsWithGrantOption = []
                
                if _df["ResourceGrantPermissions"] != "":
                   
                    l_g_permission = []
                   
                    pgcol = _df["ResourceGrantPermissions"].split(",")
                   
                    for gperm in pgcol:
                   
                        if gperm == "*":
                            l_g_permission.append("ALL") 
                        if gperm == "S":
                            l_g_permission.append("SELECT")
                        if gperm == "I":
                            l_g_permission.append("INSERT")
                        if gperm == "A":
                            l_g_permission.append("ALTER")
                        if gperm == "DR":
                            l_g_permission.append("DROP")
                        if gperm == "DL":
                            l_g_permission.append("DELETE")
                        if gperm == "DS":
                            l_g_permission.append("DESCRIBE")
                        if gperm == "CT":
                            l_g_permission.append("CREATE_TABLE")
                        if gperm == "CD":
                            l_g_permission.append("CREATE_DATABASE")
                        if gperm == "DLA":
                            l_g_permission.append("DATA_LOCATION_ACCESS")
                        if gperm == "AT":
                            l_g_permission.append("ASSOCIATE_TAG")
                        if gperm == "CTG":
                            l_g_permission.append("CREATE_TAG")
                            
                    _PermissionsWithGrantOption = l_g_permission

                
                _Entry = {
                    'Id': str(uuid.uuid4()),
                    'Principal': _Principal,
                    'Resource': _Resource,
                    'Permissions': _Permissions,
                    'PermissionsWithGrantOption': _PermissionsWithGrantOption
                    }
                
                if _df["Action"] != "":

                    if _df["Action"].upper().strip() == "GRANT":
                        _EntriesGrant.append(_Entry)
                    elif _df["Action"].upper().strip() == "REVOKE":
                        _EntriesRevoke.append(_Entry)
                    else:
                        print("ERROR: Invalid value on Action, please specify a GRANT or REVOKE value")
                        return None
                else:
                    print("ERROR: No Action was specified, please specify if it is an GRANT or REVOKE action")
                    return None
        
    if _EntriesGrant:
        response = apply_lake_formation_permissions(_EntriesGrant, "GRANT")

                
    if _EntriesRevoke:
        response = apply_lake_formation_permissions(_EntriesRevoke, "REVOKE")
                   
                       
    return response
            
                    

def apply_lake_formation_permissions(_Entries, Action):
    lake_formation = boto3.session.Session().client('lakeformation')
    
    num_l_perm = len(_Entries)
    num_chunks = math.ceil(num_l_perm/19) #19 is the Lake Formation Batch API Limit for number of entries.
    print("num_chunks "+str(num_chunks))
    print("Entry type " + str(type(_Entries)))
    print(_Entries)
    print("1...................")
    l_entries = list(split_list(_Entries, num_chunks))
    #l_entries = numpy.array_split(_Entries,num_chunks)
    print(l_entries[0])
    print("2...................")
    dict_response = []
   
    if Action == "REVOKE":
 
        for entry in l_entries:
            response = lake_formation.batch_revoke_permissions(Entries=entry)
            result_dict = json.dumps(response)
            result_dict = json.loads(result_dict)
            dict_response.append(result_dict['Failures'])
        
        response = [item for sublist in dict_response for item in sublist]
        print("REVOKE EXECUTED! IN CASE OF FAILURES ON API SEE THE JSON BELOW:")
        print(json.dumps(response))
        
    elif Action == "GRANT":
        
        #response = lake_formation.batch_grant_permissions(Entries=_Entries )
        for entry in l_entries:
            response = lake_formation.batch_grant_permissions(Entries=entry)
            result_dict = json.dumps(response)
            result_dict = json.loads(result_dict)
            dict_response.append(result_dict['Failures'])
        
        response = [item for sublist in dict_response for item in sublist]
        print("GRANT EXECUTED! IN CASE OF FAILURES ON API SEE THE JSON BELOW:")
        print(json.dumps(response))

    else:
        print("ERROR: Invalid argument in apply_lake_formation_permissions, must be GRANT or REVOKE ")
        pass
    
    return response

def replace(g):
    return g.group(0).replace(',', ';')


def split_list(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]



