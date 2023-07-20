USE MedCorpDB
GO

IF NOT EXISTS (
	SELECT name
	FROM sys.databases
	WHERE name = N'MedCorpDB'
)

CREATE DATABASE [MedCorpDB]
GO

IF OBJECT_ID(N'dbo.MakeAppointment', N'U') IS NULL
	CREATE TABLE MakeAppointment (
		specialization_ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
		specialization VARCHAR(250) NOT NULL,
	);
GO

INSERT INTO MakeAppointment (specialization)
VALUES ('Allergy and immunology'),
('Anesthesiology'),
('Dermatology'),
('Diagnostic radiology'),
('Emergency medicine'),
('Family medicine'),
('Internal medicine'),
('Medical genetics'),
('Neurology'),
('Obstetrics and gynecology'),
('Ophthalmology'),
('Pathology'),
('Pediatrics'),
('Physical medicine and rehabilitation'),
('Preventive medicine'),
('Psychiatry'),
('Radiation oncology'),
('Surgery'),
('Urology');

IF OBJECT_ID(N'dbo.DoctorsTable', N'U') IS NULL
	CREATE TABLE DoctorsTable (
		doctor_ID INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
		doc_name CHAR(250) NOT NULL,
		doc_surname CHAR(250) NOT NULL,
		specialization_ID INT FOREIGN KEY REFERENCES MakeAppointment(specialization_ID),
	);
GO

INSERT INTO DoctorsTable (doc_name, doc_surname, specialization_ID)
VALUES ('Zoya', 'Price', 6),
('Mattie', 'Farley', 8),
('Elias', 'Bentley', 3),
('Deanna', 'Rocha', 4),
('Kirsten', 'Middleton', 3),
('Drew', 'Case', 5),
('Elouise', 'Goodman', 8),
('Jeremiah', 'Clements', 6),
('Miah', 'Sykes', 6),
('Kathleen', 'Valdez', 2),
('Leo', 'Mckenzie', 4),
('Syeda', 'Ferguson', 6),
('Gethin', 'Sloan', 10),
('Virginia', 'Andrews', 7),
('Siena', 'Petersen', 1),
('Kira', 'Blankenship', 7),
('Ruairi', 'Best', 6),
('Brodie', 'Finley', 4),
('Jeffrey', 'Reeves', 2),
('Fay', 'Kline', 7);