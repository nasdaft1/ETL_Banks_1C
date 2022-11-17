USE FirmMS;

-- удаление PRIMARY KEY во всех таблицах
SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
DECLARE 
@Table  nvarchar (128)='', -- название схемы +.+ таблица
@CONSTRAINT_NAME nvarchar (128)='', -- названия CONTRAINT для ключа
@Command nvarchar (420)='' -- выставляем максимальное значение строки с при сложение переменных и дополнительного текста формирующего комманду 128+128+128+30 = 414 (сумма максимальных значений переменных) 
WHILE 1=1 -- создаем бесконечный цикл
	BEGIN
	SELECT TOP (1) @Table =  CONCAT_WS(N'.',TABLE_SCHEMA, TABLE_NAME), @CONSTRAINT_NAME = CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE -- получаем список ключей и таблиц и присваиваем их переменным
		IF @@ROWCOUNT = 0 BREAK  -- проверяем остались еще не удаленные ключи
		ELSE  --если осталось выполняем следущее действия
			BEGIN
				SET @Command = 	CONCAT(N'ALTER TABLE ', @Table, N' DROP CONSTRAINT ', @CONSTRAINT_NAME)  -- формируем команду для выполнения
				--SELECT @Command AS [COMMAND] , @@ROWCOUNT
				EXEC (@Command) --ALTER TABLE @Table DROP CONSTRAINT @CONSTRAINT_NAME 
			END;
	END;
GO

-- удаление всех таблиц в базе данных
SELECT * FROM INFORMATION_SCHEMA.TABLES
DECLARE 
@Table  nvarchar (128)='', -- название схемы +.+ таблица
@Command nvarchar (280)='' -- выставляем максимальное значение строки с при сложение переменных и дополнительного текста формирующего комманду 128+128+20 = 276 (сумма максимальных значений переменных) 
BEGIN	
	WHILE 1=1 -- создаем бесконечный цикл
	BEGIN
	SELECT TOP (1) @Table =  CONCAT_WS(N'.',TABLE_SCHEMA, TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES -- получаем список схем +.+ таблиц 
		IF @@ROWCOUNT = 0 BREAK  -- проверяем остались еще не удаленные ключи
		ELSE  --если осталось выполняем следущее действия
			BEGIN
				SET @Command = 	CONCAT(N'DROP TABLE ', @Table)  -- формируем команду для выполнения
				SELECT @Command AS [COMMAND] , @@ROWCOUNT
				EXEC (@Command)  --DROP TABLE @Table 
			END;
	END;
END;
GO

-- удаление схем созданных пользователем ранее 
SELECT Tb1.SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA AS Tb1 WHERE Tb1.SCHEMA_NAME<>N'dbo' AND Tb1.SCHEMA_OWNER = N'dbo' -- показывет все схемы в базе данных созданные 
DECLARE 
@SCHEMA_NAME  nvarchar (128)='', -- название схемы 
@Command nvarchar (280)='' -- выставляем максимальное значение строки с при сложение переменных и дополнительного текста формирующего комманду 128+128+20 = 276 (сумма максимальных значений переменных) 
WHILE 1=1 -- создаем бесконечный цикл
	BEGIN
	SELECT TOP (1) @SCHEMA_NAME =  Tb1.SCHEMA_NAME 
		FROM INFORMATION_SCHEMA.SCHEMATA AS Tb1 
		WHERE Tb1.SCHEMA_NAME<>N'dbo' AND Tb1.SCHEMA_OWNER = N'dbo' -- получаем название схемы созданной пользователем 
		IF @@ROWCOUNT = 0 BREAK  -- проверяем остались еще не удаленные ключи
		ELSE  --если осталось выполняем следущее действия
			BEGIN
				SET @Command = 	CONCAT(N'DROP SCHEMA ', @SCHEMA_NAME)  -- формируем команду для выполнения
				EXEC (@Command)  --DROP SCHEMA @SCHEMA_NAME 
			END;
	END;

GO -- Создание схем
	CREATE SCHEMA money_movement AUTHORIZATION dbo;
GO
	CREATE SCHEMA product_movement AUTHORIZATION dbo;
GO
SELECT * FROM INFORMATION_SCHEMA.TABLES
GO

-- Создане таблиц
CREATE TABLE money_movement.operation_external( --Операции внешнии
	id_operation_external INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_1] PRIMARY KEY, --id Внешний операции
	id_organizations INT, --id организации
	number_operation INT, --Номер операции
	payment_amount DECIMAL(8,2), --Сумма
	type_operation BINARY, --тип операции (дебит/кредит)
	date_operation DATE, --дата операции
	id_business_entities INT, --id хозяйствующего субъекта
	name_payment NVARCHAR(200), --имя платежа
	id_payment_intermediary INT --id платежный посредник
	);

CREATE TABLE money_movement.payment_intermediary(--платежный посредник
	id_payment_intermediary INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_2] PRIMARY KEY, --id_платежный_посредник
	name_payment_intermediary NVARCHAR(20), --name_платежный посредник
	date_start_intermediary DATE, --дата_начала_работы_посредника
	id_business_entities  INT, --id_Хозяйствующий субъект
	date_end_intermediary DATE --дата_окончания_работы_посредника
	);

CREATE TABLE money_movement.operation_internal(--Операции
	id_operation_internal INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_3] PRIMARY KEY, --ID_операции внутренняя
	id_operation_external INT, --ID_Операция внешняя
	id_business_entities_credit INT, --id_Хозяйствующий субъект_кредит
	id_business_entities_debit INT, --id_Хозяйствующий субъект_дебит
	payment_amount DECIMAL(8,2), --Сумма
	type_operation INT, --тип операции
	date_operation DATE, --дата операции
	name_payment NVARCHAR(50) --имя_платежа
	);

CREATE TABLE money_movement.organizations(--Организаций
	id_organizations INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_4] PRIMARY KEY, --id_Организаций
	name_organizations NVARCHAR(250) CONSTRAINT [UK_1] UNIQUE, --Название Организации
	ITN NVARCHAR(12) CONSTRAINT [UK_2] UNIQUE, --ИНН
	id_business_entities INT --id_Хозяйствующий субъект
	);

CREATE TABLE money_movement.business_entities(--Хозяйствующий субъект
	id_business_entities  INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_5] PRIMARY KEY, --id_Хозяйствующий субъект
	name_business_entities NVARCHAR(50) CONSTRAINT [UK_3] UNIQUE --имя_хозяйствующего субъекта
	);

CREATE TABLE product_movement.storehouse(--Склад
	id_storehouse INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_6] PRIMARY KEY, --id_склада
	name_storehouse NVARCHAR(20) CONSTRAINT [UK_4] UNIQUE, --имя_склада
	id_business_entities INT --id_Хозяйствующий субъект
	);

CREATE TABLE product_movement.product_list(--список товаров
	id_product INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_7] PRIMARY KEY, --id_список товаров
	id_waybill INT, --id_накладная
	id_name_product INT, --id_имя_товара
	quantity_product INT, --количество_товара
	id_storehouse INT --id_склада
	);

CREATE TABLE product_movement.waybill(--накладная
	id_waybill INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_8] PRIMARY KEY, --id_накладная
	id_invoice INT, --id счета фактуры
	date_waybill DATE --date_накладная
	);

CREATE TABLE product_movement.product(--товар
	id_name_product INT NOT NULL IDENTITY(1,1)	CONSTRAINT [PK_9] PRIMARY KEY, --id_имя_товара
	name_product NVARCHAR(30) CONSTRAINT [UK_5] UNIQUE --имя_товара
	);

CREATE TABLE product_movement.invoices(--счета фактуры
	id_invoice INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_10] PRIMARY KEY, --id счета фактуры
	number_invoice NVARCHAR(30), --номер_счета_фактуры
	payment_amount DECIMAL(8,2), --Сумма
	date_invoice DATE --дата счета фактуры
	);

CREATE TABLE product_movement.payments(--платежи
	id_operation INT NOT NULL IDENTITY(1,1) CONSTRAINT [PK_11] PRIMARY KEY, --ID_Организации
	id_invoice INT --id счета фактуры
	);

GO
-- Добавление в таблицу связей
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




