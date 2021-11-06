USE [accs00]
go

CREATE TABLE dbo.orgs (
	--id PRIMARY KEY,
	orgname  VARCHAR (150),
	inn      VARCHAR (15),
	kpp      VARCHAR (10)
	);
	
	
INSERT INTO dbo.orgs (orgname, inn, kpp) VALUES ('ООО Регион', '7106085078', '710601001');
	