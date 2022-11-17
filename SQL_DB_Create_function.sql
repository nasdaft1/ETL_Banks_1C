USE FirmMS;



SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE

--K	Debit	632200118697	6324030091	Индивидуальный предприниматель Тимохин Виталий Федорович	ООО "Интерком"	2015.04.30	127	14500	Оплата за оказание услуг по ремонту системы охранной 


--поиск в таблице данных до первого совпадения
--если не найдено добавить новое значение






GO
CREATE OR ALTER PROCEDURE  [usp_Add_Money] (
	@business_entities NVARCHAR(50),
	@type_operation NVARCHAR(10),
	@ITN_in NVARCHAR(12),
	@ITN_out NVARCHAR(12),
	@name_organizations NVARCHAR(250),
	@date_operation DATE,
	@payment_amount DECIMAL(8,2),
	@name_payment NVARCHAR(200)
) AS
DECLARE @X INT;




GO
INSERT  money_movement.business_entities (name_business_entities) VALUES	(N'K'),(N'B');
GO
SELECT * FROM money_movement.business_entities

SELECT * FROM money_movement.business_entities 
DECLARE @N NVARCHAR(3);
SET @N =N'h'
--поиск до первого совпадения и если не найдено добавить в таблице новое значение
IF NOT EXISTS (SELECT 1 
	        FROM money_movement.business_entities WHERE name_business_entities=@N)
				INSERT INTO money_movement.business_entities (name_business_entities) VALUES (@N);

DECLARE
@ITN_in NVARCHAR(12),
@name_organizations NVARCHAR(250)
SET @ITN_in = N'K'
SET @name_organizations = N'Индивидуальный предприниматель Тимохин Виталий Федорович'
IF NOT EXISTS (SELECT 1   
	        FROM money_movement.organizations WHERE ITN =@N)
				INSERT INTO money_movement.organizations (name_organizations , ITN) VALUES (@name_organizations, @ITN_in);



--присвоение 
--CREATE OR ALTER PROCEDURE  [usp_Genre_Add] (
--@Genre NVARCHAR(50),
--@IdGenre INT OUTPUT
--) AS
--DECLARE @TranName NVARCHAR(50) = object_name(@@procid);  -- получаем название процедуры для создания именованной транзакции
--SET NOCOUNT ON;
--BEGIN TRY
--	BEGIN TRAN @TranName
--		SELECT TOP(1) @IdGenre =  TbGenre.IdGenre -- получение id жанра книги
--		FROM Book.Genre AS TbGenre
--			WHERE TbGenre.NameGenre =  @Genre
--			IF @IdGenre = -1  -- если данных нет производится встака данных
--				BEGIN
--					INSERT INTO Book.Genre (NameGenre,DataCreate)
--						VALUES (@Genre, SYSUTCDATETIME())
--					SET @IdGenre = SCOPE_IDENTITY()
--				END
--			--PRINT concat('@IdGenre=',@IdGenre)
--	COMMIT TRAN @TranName -- сохранение транзации
--END TRY 
--	BEGIN CATCH -- блок обработки исключений
--		IF @@TRANCOUNT>0 
--			BEGIN
--				PRINT CONCAT(N'Error and abort transaction -',@TranName)
--				ROLLBACK TRAN @TranName-- отмена транзакции
--			END
--			ELSE PRINT CONCAT(N'Error cisntaxis -',@TranName)
--	END CATCH 
--GO