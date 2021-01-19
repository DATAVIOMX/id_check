# MANUAL del Administrador

## Creacion de usuarios:

Vamos a insertar un registro en la base de datos, para esto corremos el 
siguiente query:
NOTA: La cadena 'oBE3PSTPOswJDRIfGCbhRnxE00rgG' es la sal del hash no se debe
cambiar
Esto le da una validez de un mes al password
```
INSERT INTO users(userid, creation_date, update_date, status, api_key, api_key_exp_date, calls_remaining) VALUES (uuid_generate_v4(), NOW()::timestamp,NOW()::timestamp, 0, crypt('mypass','oBE3PSTPOswJDRIfGCbhRnxE00rgG'),(NOW()::timestamp+interval) '30 days',1000);
```

Para alterar un usuario y generarle una nueva llave de su API
```
UPDATE users set 
api_key = crypt('mynewpass','oBE3PSTPOswJDRIfGCbhRnxE00rgG'),
update_date = NOW()::timestamp,
api_key_exp_date = (NOW()::timestamp+interval '1 month')
where userid = '<userid>'::uuid;
```
