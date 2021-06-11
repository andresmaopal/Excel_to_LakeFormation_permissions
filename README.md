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
  * Any IAM Principal, User, Role, Organization or Organization Unit to set permissions, to specify more than use commas.

  * **RoleName** for set a role name
  * **u:UserName** for set a user name
  * **a:AccountID** for set an Account ID
  * **o:111122223333:o-abcdefghijkl** for set an Organization
  * **ou:111122223333:o-abcdefghijkl/ou-ab00-cdefghij** for set an Organization ID
 
* **Action**
*   * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"
* **ResourceElements**
*   * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"
* **ResourcePermissions**
*   * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"
* **ResourceGrantPermissions**
*   * Any Glue Catalog Database name or S3 Data Location path to set permissions
  * **Example:** "database_name" or "s3://bucket/table"














