-- Script de creación de la base de datos y la tabla
-- Ejecutar en SQL Server Management Studio (SSMS): botón "Nueva consulta" y luego "Ejecutar"

IF DB_ID('DatosAbiertosDB') IS NULL
    CREATE DATABASE DatosAbiertosDB;
GO

USE DatosAbiertosDB;
GO

IF OBJECT_ID('dbo.RegistrosAPI', 'U') IS NULL
CREATE TABLE RegistrosAPI (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    id_api         NVARCHAR(100) NOT NULL UNIQUE,   -- código DIVIPOLA del municipio (evita duplicados)
    municipio      NVARCHAR(150) NULL,
    departamento   NVARCHAR(150) NULL,
    tipo_municipio NVARCHAR(100) NULL,
    latitud        NVARCHAR(50)  NULL,
    longitud       NVARCHAR(50)  NULL,
    json_original  NVARCHAR(MAX) NULL,              -- copia completa del JSON recibido
    fecha_captura  DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO
