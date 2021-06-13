![alt text](https://i.ibb.co/bF3Ts2F/excel-to-lf-logo.png)

 AWS Lambda to Grant and Revoke permissions in bulk to Lake Formation using an user-friendly Excel template

![alt text](https://i.ibb.co/xXgGv2Q/excel-to-lf-process.png")

### Excel template example

| ResourceLocationDatabase | TargetPrincipals | Action | ResourceElements | ResourcePermissions	| ResourceGrantPermissions |
| --- | --- | --- | --- | --- | --- |
|database1	|role1,role2,role3	|GRANT|		|CT,A,DR| |	
|database2	|role1, u:user1	|GRANT|	*	|S,I,U,DR|S,I,U,DR|
|database1	|role1|	GRANT	|table1,table2,table3|	*	| |
|database1	|role1,role2|	GRANT	|table1(col1,col2,col3,col4)|	S	| |
|s3://lf-data-lake-bucket|spectrumrole, u:user2	|GRANT	| |	DLA	| |
|database1	|role3, u:user2	|REVOKE|	*	|S,I,U,DR	|S,I,U,DR |

### Supported syntax

* **ResourceLocationDatabase** 
  * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"

* **TargetPrincipals**
  * Any IAM Principal: User, Role, Organization or Organization Unit to set permissions, to specify more than one use comma separation
 
  * **Values**:
  * **roleName** for set a role name
  * **u:UserName** for set a user name
  * **a:AccountID** for set an Account ID
  * **o:111122223333:o-abcdefghijkl** for set an Organization
  * **ou:111122223333:o-abcdefghijkl/ou-ab00-cdefghij** for set an Organization ID
 
* **Action**
  * A Grant or Revoke action
  * **Values:** "GRANT" or "REVOKE"
  
* **ResourceElements**
  * A target Resource element to set permission, to specify more than one use comma separation

  * **Values**:
  * **Leave empty** to specify only a Database permission
  * **"*"** to specify ALL TABLES within the database
  * **TableName** to specify a Table with all columns
  * **TableName(column1,column2,column3)** to include a Table with **included** list of columns, example: customer(col1,col2,col3)
  * **TableName(-column1,column2,column3)** to include a Table with **excluded** list of columns, the diference is the "-" symbol, example: customer(-email,address)
  * **TagKey:TagValue** to set a Tag with Key:Value, example: Domain:Customer

* **ResourcePermissions**

  * A Supported Lake Formation permission, to specify more than one use comma separation
  * 
  * **Values**:
  * **S** SELECT
  * **I** INSERT
  * **U** UPDATE
  * **DR** DROP
  * **DL** DELETE
  * **DS** DESCRIBE
  * **CT** CREATE TABLE
  * **CD:** CREATE_DATABASE
  * **DLA:** DATA_LOCATION_ACCESS
  * **AT:** ASSOCIATE_TAG

* **ResourceGrantPermissions**

  * A Supported Lake Formation Grantable permission, to specify more than one use comma separation.
  * 
  * **Values**:
  * **S** SELECT
  * **I** INSERT
  * **U** UPDATE
  * **DR** DROP
  * **DL** DELETE
  * **DS** DESCRIBE
  * **CT** CREATE TABLE
  * **CD:** CREATE_DATABASE
  * **DLA:** DATA_LOCATION_ACCESS
  * **AT:** ASSOCIATE_TAG

### Installation:

1. Clone the repo
2. Create an AWS Lambda function with Python 3.8 and paste the code in *src/Lambda_Source*
3. Create a Lambda Layer with the included Layer in *src/Lambda_Layer*
4. Add the Layer to the previusly created Lambda function
5. Attach to the Lambda role the policy: *AWSLakeFormationDataAdmin* 
6. Attach a the Lambda role a s3:GetObject permission for the S3 Bucket where you want to upload the Excel files.
7. Add the Lambda role as an Administrator in *Administrative roles and tasks* in AWS Lake Formation.
8. Modify the Excel and upload it to the selectd S3 path.















