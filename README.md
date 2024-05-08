# Documentación del Microservicio de Scraping

## 1. Introducción

Este documento proporciona una guía para ejecutar y administrar el microservicio de scraping Django, incluyendo la estructura de la base de datos y la documentación del modelo Invoice.

## 2. Requisitos Previos
- Clonar el repositorio: [text](https://github.com/waperdomob/scrapper-api.git)
- Docker instalado en su sistema local
- Imagen de Docker construida para el microservicio

## 3. Ejecución Local

Abra una terminal en el directorio raíz de su proyecto.

Ejecute el siguiente comando para ejecutar el microservicio y la base de datos localmente:

```bash
docker-compose up -d
```

Verificamos que los contenedores estén corriendo:
```bash
docker ps
```

Ahora debemos correr las migraciones ingresando al contenedor scraper-api:
```bash
docker exec -it scrapper-scraper_api-1 /bin/bash
```

y luego ejecutando el comando:
```bash
python manage.py migrate
```


Esto iniciará los contenedores de Docker para su microservicio y la base de datos especificados en el archivo `docker-compose.yml`.

Una vez que los contenedores estén en ejecución, puede acceder a su aplicación Django en el siguiente puerto: [http://localhost:8000](http://localhost:8000).


La base de datos es MySQL, puede acceder a ella utilizando las siguientes credenciales:
- Usuario: root
- Contraseña: password
- Nombre de la base de datos: scrapper


Para detener los contenedores en ejecución y finalizar la ejecución del microservicio, ejecute el siguiente comando:

```bash
docker-compose down
```

## 4. Estructura de la Base de Datos

La estructura de la base de datos se compone de una tabla principal:

### Tabla: facturas

| Campo           | Tipo de Dato   | Descripción                                                                                               |
|-----------------|----------------|-----------------------------------------------------------------------------------------------------------|
| cufe            | CharField(100) | Almacena el CUFE (Código Único de Facturación Electrónica) de la factura. Es un identificador único de la factura (máximo 100 caracteres). |
| events          | JSONField      | Almacena información de los eventos de la factura en formato JSON.  |
| issuer_name     | CharField(50)  | Almacena el nombre del emisor de la factura (máximo 50 caracteres).                                         |
| issuer_nit      | CharField(50)  | Almacena el NIT (Número de Identificación Tributaria) del emisor de la factura (máximo 50 caracteres).    |
| receiver_name   | CharField(50)  | Almacena el nombre del receptor de la factura (máximo 50 caracteres).                                       |
| receiver_nit    | CharField(50)  | Almacena el NIT del receptor de la factura (máximo 50 caracteres).                                          |
| representation  | CharField(255) | Almacena el enlace a la representación gráfica de la factura (máximo 255 caracteres).                        |

