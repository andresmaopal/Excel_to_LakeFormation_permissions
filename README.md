![alt text](https://i.ibb.co/bF3Ts2F/excel-to-lf-logo.png)

 Lambda to Grant and Revoke bulk permissions to Lake Formation using an user-friendly Excel template

![alt text](https://i.ibb.co/xXgGv2Q/excel-to-lf-process.png")

Excel template example



| ResourceLocationDatabase | TargetPrincipals | Action | ResourceElements | ResourcePermissions	| ResourceGrantPermissions |
| --- | --- | --- | --- | --- | --- |
|tpcds	|spectrumroletest	|GRANT|		|CT,A,DR| |	
|tpcds	|spectrumroletest, u:lf-developer	|GRANT|	*	|S,I,U,DR|S,I,U,DR|
|tpcds	|AtScaleSpectrumRole|	GRANT	|date_dim,time_dim,ship_mode|	*	| |
|tpcds	|AtScaleSpectrumRole|	GRANT	|customer(-c_first_name,c_last_name,c_email_address)|	S	| |
|s3://lf-data-lake-654106941574	|spectrumroletest, u:lf-developer	|GRANT	|	DLA	| |
|tpcds	|spectrumroletest, u:lf-developer	|REVOKE|	*	|S,I,U,DR	|S,I,U,DR |












