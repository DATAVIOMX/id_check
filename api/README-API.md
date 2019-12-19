# ID-CHECK-API

API RESTful para comprobación de INE, hecha con python, Flask y PostgreSQL.

## Autor

Motoko Research

## Fecha de creación 

2019-12-16

## Dependencias

- Ubuntu Linux 18.04 LTS
- Python 3
- venv
- PostgreSQL 10
- SQLite 3 (testing)
- Flask
- Flask-restful
- SQLAlchemy
- psycopg2
- gunicorn
- NGinx

## Instalación

1. Crear una carpeta para el repositorio
2. Crear un ambiente virtual `python3.6 -m venv venv`
3. Activarlo `source venv/bin/activate`
4. Crear base de datos en SQLite `sqlite3 id-check-db.sqlite < id-check-db.sql`
5. Instalar dependencias `pip install -r requirements.txt`

```pip install Flask Flask-restful SQLAlchemy psycopg2``` 
 
## Endpoints

- users: Lista los usuarios 
- check-ids: Analiza las imágenes  
- images: Permite subir las imágenes regresa una id de la imagen

## Estructura de archivos

```
id_check_api/
    README.md
    venv/
    app.py
    wsgi.py
    requirements.txt
```

## Formato de las llamadas

### users

GET a users/userid lista la fecha de creacion del usuario, y la fecha de
terminación del servicio, fecha de ultimo pago y llamadas restantes  

PUT a users/userid, actualiza un usuario

POST a users crea un usuario y devuelve el userid y el API key

DELETE a users/userid borra un usuario 

### images

POST a images sube una imagen y devuelve su id

DELETE a images/imageid borra una imagen

### check-ids

GET a check-ids analiza la imagen (terminado el análisis borra las imágenes) 

## Modo de uso 

### Creación de un nuevo usuario

TBD

### Borrar usuario

TBD

### Nueva llave de la API

TBD

### Subir imágenes

TBD

### Analizar INE

TBD

