![alt text](https://i.ibb.co/bF3Ts2F/excel-to-lf-logo.png)

 AWS Lambda to Grant and Revoke permissions in bulk to Lake Formation using an user-friendly Excel template

![alt text](https://i.ibb.co/xXgGv2Q/excel-to-lf-process.png")

### Excel template example

| ResourceLocationDatabase | TargetPrincipals | Action | ResourceElements | ResourcePermissions	| ResourceGrantPermissions |
| --- | --- | --- | --- | --- | --- |
|tpcds	|spectrumroletest	|GRANT|		|CT,A,DR| |	
|tpcds	|spectrumroletest, u:lf-developer	|GRANT|	*	|S,I,U,DR|S,I,U,DR|
|tpcds	|SpectrumRole|	GRANT	|date_dim,time_dim,ship_mode|	*	| |
|tpcds	|SpectrumRole|	GRANT	|customer(-c_first_name,c_last_name,c_email_address)|	S	| |
|s3://lf-data-lake-bucket|spectrumroletest, u:lf-developer	|GRANT	|	DLA	| |
|tpcds	|spectrumroletest, u:lf-developer	|REVOKE|	*	|S,I,U,DR	|S,I,U,DR |

### Supported syntax

* **ResourceLocationDatabase** 
  * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"

* **TargetPrincipals**
  * Any IAM Principal: User, Role, Organization or Organization Unit to set permissions, to specify more than one use comma separation:
  Values:
  * **roleName** for set a role name
  * **u:UserName** for set a user name
  * **a:AccountID** for set an Account ID
  * **o:111122223333:o-abcdefghijkl** for set an Organization
  * **ou:111122223333:o-abcdefghijkl/ou-ab00-cdefghij** for set an Organization ID
 
* **Action**
  * A Grant or Revoke action
  * **Example:** "GRANT" or "REVOKE"
  
* **ResourceElements**
  * A target Resource element to set permission, to specify more than one use comma separation:
  Values:  
  * **Leave empty** to specify only a Database permission
  * **"*"** to specify ALL TABLES within the database
  * **TableName** to specify a Table with all columns
  * **TableName(column1,column2,column3)** to include a Table with **included** list of columns, example: customer(col1,col2,col3)
  * **TableName(-column1,column2,column3)** to include a Table with **excluded** list of columns, the diference is the "-" symbol, example: customer(-email,address)
  * **TagKey:TagValue** to set a Tag with Key:Value

* **ResourcePermissions**

  * A Supported Lake Formation permission, to specify more than one use comma separation:
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















