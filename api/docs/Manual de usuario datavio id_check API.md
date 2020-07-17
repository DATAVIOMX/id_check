# Manual de usuario datavio id_check API


## Requerimientos de Software

Toda esta instalación se entregará al cliente dentro de una máquina virtual de VMWare 
Para descargar VMWare usar la siguiente liga:

https://my.vmware.com/en/web/vmware/downloads/details?downloadGroup=PLAYER-1556&productId=800&rPId=47861

### Requerimientos del cliente (Todo está preinstalado en la MV)

- python 3.6
- requests
- openCV

### Para conectar con la API de manera independiente

- wget o
- Postman

## Instalación en linux

Para una mejor experiencia lo ideal es tener las fotografías o textos en una base de datos y alimentar al cliente a partir de ella, por lo que se describe la instalación en un ambiente linux

Instalar el cliente en la carpeta `/home` del usuario que va a correr las peticiones.

```
$ cd /home/<usuario>/id_check-client
```

cambiar a modo de ejecución

```
$ sudo chmod +x id_check-client
```

## Ejecución del cliente en línea de comandos

Existen dos modos de ejecución de las peticiones vía texto o vía las imágenes de la credencial para votar INE.
El cliente recibirá argumentos en línea de comandos para cualquiera de las alternativas.

Las opciones que siempre deben estar presentes son:

- `-s` o `--salida` que es el nombre del archivo de salida de la página del INE.
- `-k` o `--key` que es la llave de la API que se debe adjuntar siempre.

### Validación vía texto:

```
$ id_check-client -s <salida> -k <API-key> text -t <tipo-credencial> -v <clave-elector>  -e <emision> -o <ocr>  -c <cic>
```

Explicación:

para la credencial tipo A,B o C se necesitan los valores de tipo credencial, clave-elector y emisión. Para las tipo D y E se necesitan los valores de cic y OCR. la opción de salida es el nombre base de los archivos, genera un archivo salida.html con la respuesta del ine y uno llamado salida_valid.txt que contiene una sóla línea diciendo si la credencial es válida o no.

### Validación vía imágenes

```
$ id_check-client -s <salida> -k <API-key> image -f <frente> -b <reverso>
```

Explicación

Para el modo de identificación vía análisis de imágenes, necesitamos definir el modo i para imagen y los archivos de las imágenes de frente y el reverso en formato JPG o PNG. la opción de salida es el nombre base de los archivos, genera un archivo salida.html con la respuesta del ine y uno llamado salida_valid.txt que contiene una seola línea diciendo si la credencial es válida o no.



