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

* *ResourceLocationDatabase*
* asadasd

* TargetPrincipals
* Action
* ResourceElements
* ResourcePermissions
* ResourceGrantPermissions














