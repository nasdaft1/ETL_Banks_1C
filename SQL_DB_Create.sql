USE FirmMS;

-- �������� PRIMARY KEY �� ���� ��������
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
DECLARE 
@Table  nvarchar (128)='', -- �������� ����� +.+ �������
@CONSTRAINT_NAME nvarchar (128)='', -- �������� CONTRAINT ��� �����
@Command nvarchar (420)='' -- ���������� ������������ �������� ������ � ��� �������� ���������� � ��������������� ������ ������������ �������� 128+128+128+30 = 414 (����� ������������ �������� ����������) 
WHILE 1=1 -- ������� ����������� ����
	BEGIN
	SELECT TOP (1) @Table =  CONCAT_WS(N'.',TABLE_SCHEMA, TABLE_NAME), @CONSTRAINT_NAME = CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE -- �������� ������ ������ � ������ � ����������� �� ����������
		IF @@ROWCOUNT = 0 BREAK  -- ��������� �������� ��� �� ��������� �����
		ELSE  --���� �������� ��������� �������� ��������
			BEGIN
				SET @Command = 	CONCAT(N'ALTER TABLE ', @Table, N' DROP CONSTRAINT ', @CONSTRAINT_NAME)  -- ��������� ������� ��� ����������
				--SELECT @Command AS [COMMAND] , @@ROWCOUNT
				EXEC (@Command) --ALTER TABLE @Table DROP CONSTRAINT @CONSTRAINT_NAME 
			END;
	END;
GO

-- �������� ���� ������ � ���� ������
SELECT * FROM INFORMATION_SCHEMA.TABLES
DECLARE 
@Table  nvarchar (128)='', -- �������� ����� +.+ �������
@Command nvarchar (280)='' -- ���������� ������������ �������� ������ � ��� �������� ���������� � ��������������� ������ ������������ �������� 128+128+20 = 276 (����� ������������ �������� ����������) 
BEGIN	
	WHILE 1=1 -- ������� ����������� ����
	BEGIN
	SELECT TOP (1) @Table =  CONCAT_WS(N'.',TABLE_SCHEMA, TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES -- �������� ������ ���� +.+ ������ 
		IF @@ROWCOUNT = 0 BREAK  -- ��������� �������� ��� �� ��������� �����
		ELSE  --���� �������� ��������� �������� ��������
			BEGIN
				SET @Command = 	CONCAT(N'DROP TABLE ', @Table)  -- ��������� ������� ��� ����������
				SELECT @Command AS [COMMAND] , @@ROWCOUNT
				EXEC (@Command)  --DROP TABLE @Table 
			END;
	END;
END;
GO

-- �������� ���� ��������� ������������� ����� 
SELECT Tb1.SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA AS Tb1 WHERE Tb1.SCHEMA_NAME<>N'dbo' AND Tb1.SCHEMA_OWNER = N'dbo' -- ��������� ��� ����� � ���� ������ ��������� 
DECLARE 
@SCHEMA_NAME  nvarchar (128)='', -- �������� ����� 
@Command nvarchar (280)='' -- ���������� ������������ �������� ������ � ��� �������� ���������� � ��������������� ������ ������������ �������� 128+128+20 = 276 (����� ������������ �������� ����������) 
WHILE 1=1 -- ������� ����������� ����
	BEGIN
	SELECT TOP (1) @SCHEMA_NAME =  Tb1.SCHEMA_NAME 
		FROM INFORMATION_SCHEMA.SCHEMATA AS Tb1 
		WHERE Tb1.SCHEMA_NAME<>N'dbo' AND Tb1.SCHEMA_OWNER = N'dbo' -- �������� �������� ����� ��������� ������������� 
		IF @@ROWCOUNT = 0 BREAK  -- ��������� �������� ��� �� ��������� �����
		ELSE  --���� �������� ��������� �������� ��������
			BEGIN
				SET @Command = 	CONCAT(N'DROP SCHEMA ', @SCHEMA_NAME)  -- ��������� ������� ��� ����������
				EXEC (@Command)  --DROP SCHEMA @SCHEMA_NAME 
			END;
	END;

GO -- �������� ����
	CREATE SCHEMA money_movement AUTHORIZATION dbo;
GO
	CREATE SCHEMA product_movement AUTHORIZATION dbo;
GO
SELECT * FROM INFORMATION_SCHEMA.TABLES
GO

-- ������� ������
CREATE TABLE money_movement.operation_external( --�������� �������
	id_operation_external INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_1] PRIMARY KEY, --id ������� ��������
	id_organizations INT, --id �����������
	number_operation INT, --����� ��������
	payment_amount DECIMAL(8,2), --�����
	type_operation BINARY, --��� �������� (�����/������)
	date_operation DATE, --���� ��������
	id_business_entities INT, --id �������������� ��������
	name_payment NVARCHAR(200), --��� �������
	id_payment_intermediary INT --id ��������� ���������
	);

CREATE TABLE money_movement.payment_intermediary(--��������� ���������
	id_payment_intermediary INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_2] PRIMARY KEY, --id_���������_���������
	name_payment_intermediary NVARCHAR(20), --name_��������� ���������
	date_start_intermediary DATE, --����_������_������_����������
	id_business_entities  INT, --id_������������� �������
	date_end_intermediary DATE --����_���������_������_����������
	);

CREATE TABLE money_movement.operation_internal(--��������
	id_operation_internal INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_3] PRIMARY KEY, --ID_�������� ����������
	id_operation_external INT, --ID_�������� �������
	id_business_entities_credit INT, --id_������������� �������_������
	id_business_entities_debit INT, --id_������������� �������_�����
	payment_amount DECIMAL(8,2), --�����
	type_operation INT, --��� ��������
	date_operation DATE, --���� ��������
	name_payment NVARCHAR(50) --���_�������
	);

CREATE TABLE money_movement.organizations(--�����������
	id_organizations INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_4] PRIMARY KEY, --id_�����������
	name_organizations NVARCHAR(250) CONSTRAINT [UK_1] UNIQUE, --�������� �����������
	ITN NVARCHAR(12) CONSTRAINT [UK_2] UNIQUE, --���
	id_business_entities INT --id_������������� �������
	);

CREATE TABLE money_movement.business_entities(--������������� �������
	id_business_entities  INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_5] PRIMARY KEY, --id_������������� �������
	name_business_entities NVARCHAR(50) CONSTRAINT [UK_3] UNIQUE --���_�������������� ��������
	);

CREATE TABLE product_movement.storehouse(--�����
	id_storehouse INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_6] PRIMARY KEY, --id_������
	name_storehouse NVARCHAR(20) CONSTRAINT [UK_4] UNIQUE, --���_������
	id_business_entities INT --id_������������� �������
	);

CREATE TABLE product_movement.product_list(--������ �������
	id_product INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_7] PRIMARY KEY, --id_������ �������
	id_waybill INT, --id_���������
	id_name_product INT, --id_���_������
	quantity_product INT, --����������_������
	id_storehouse INT --id_������
	);

CREATE TABLE product_movement.waybill(--���������
	id_waybill INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_8] PRIMARY KEY, --id_���������
	id_invoice INT, --id ����� �������
	date_waybill DATE --date_���������
	);

CREATE TABLE product_movement.product(--�����
	id_name_product INT NOT NULL IDENTITY(1,1)	CONSTRAINT [PK_9] PRIMARY KEY, --id_���_������
	name_product NVARCHAR(30) CONSTRAINT [UK_5] UNIQUE --���_������
	);

CREATE TABLE product_movement.invoices(--����� �������
	id_invoice INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_10] PRIMARY KEY, --id ����� �������
	number_invoice NVARCHAR(30), --�����_�����_�������
	payment_amount DECIMAL(8,2), --�����
	date_invoice DATE --���� ����� �������
	);

CREATE TABLE product_movement.payments(--�������
	id_operation INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_11] PRIMARY KEY, --ID_�����������
	id_invoice INT --id ����� �������
	);

GO
-- ���������� � ������� ������
ALTER TABLE [money_movement].[operation_external] WITH CHECK 
	ADD CONSTRAINT [FK_1] FOREIGN KEY(id_payment_intermediary)
	REFERENCES [money_movement].[payment_intermediary] (id_payment_intermediary);


ALTER TABLE [money_movement].[operation_external] WITH CHECK
	ADD CONSTRAINT [FK_2] FOREIGN KEY(id_organizations)
	REFERENCES [money_movement].[organizations] (id_organizations);


ALTER TABLE [money_movement].[payment_intermediary] WITH CHECK
	ADD CONSTRAINT [FK_3] FOREIGN KEY(id_business_entities)
	REFERENCES [money_movement].[business_entities] (id_business_entities);


ALTER TABLE [money_movement].[operation_internal] WITH CHECK
	ADD CONSTRAINT [FK_4] FOREIGN KEY(id_operation_external)
	REFERENCES [money_movement].[operation_external] (id_operation_external);

ALTER TABLE [money_movement].[operation_internal] WITH CHECK
	ADD CONSTRAINT [FK_5] FOREIGN KEY(id_business_entities_credit)
	REFERENCES [money_movement].[business_entities] (id_business_entities);

ALTER TABLE [money_movement].[operation_internal] WITH CHECK
	ADD CONSTRAINT [FK_6] FOREIGN KEY(id_business_entities_debit)
	REFERENCES [money_movement].[business_entities] (id_business_entities);


ALTER TABLE [money_movement].[organizations] WITH CHECK
	ADD CONSTRAINT [FK_7] FOREIGN KEY(id_business_entities )
	REFERENCES [money_movement].[business_entities] (id_business_entities);

-------------------------------------------------------------------------------------------------------
ALTER TABLE [product_movement].[storehouse] WITH CHECK
	ADD CONSTRAINT [FK_8] FOREIGN KEY(id_business_entities)
	REFERENCES [money_movement].[business_entities] (id_business_entities);


ALTER TABLE [product_movement].[product_list] WITH CHECK
	ADD CONSTRAINT [FK_9] FOREIGN KEY(id_storehouse)
	REFERENCES [product_movement].[storehouse] (id_storehouse);

ALTER TABLE [product_movement].[product_list] WITH CHECK
	ADD CONSTRAINT [FK_10] FOREIGN KEY(id_waybill)
	REFERENCES [product_movement].[waybill] (id_waybill);

ALTER TABLE [product_movement].[product_list] WITH CHECK
	ADD CONSTRAINT [FK_11] FOREIGN KEY(id_name_product)
	REFERENCES [product_movement].[product] (id_name_product);


ALTER TABLE [product_movement].[waybill] WITH CHECK
	ADD CONSTRAINT [FK_12] FOREIGN KEY(id_invoice)
	REFERENCES [product_movement].[invoices] (id_invoice);

GO


SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE




