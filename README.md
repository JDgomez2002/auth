# Flask API con Autenticación Keycloak
Este ejercicio es una API construida con Flask que utiliza Keycloak para autenticación mediante tokens JWT.

## Miembros 
- Abner Garcia - 21285
- Esteban Donis - 21610
- Daniel Gomez - 21429
- Adrian Rodriguez - 21691
- Samuel Chamalé - 21881
- Diego Alonzo - 20172

## Requisitos Previos
Antes de ejecutar este ejercicio, asegúrate de tener instalado:
- Python 3.x
- Flask
- Docker (para ejecutar Keycloak)
- Postman (para probar la API)
- Las siguientes librerías de Python:
pip install flask flask-cors flask-restful python-dotenv pyjwt

## Evidencia de configuración de Keycloak
![alt text](/imagenes/image.png)
![alt text](/imagenes/image-1.png)
![alt text](/imagenes/image-2.png)
![alt text](/imagenes/image-3.png)
![alt text](/imagenes/image-4.png)
![alt text](/imagenes/image-5.png)
![alt text](/imagenes/image-6.png)
![alt text](/imagenes/image-7.png)
![alt text](/imagenes/image-8.png)
![alt text](/imagenes/image-9.png)
![alt text](/imagenes/image-10.png)
![alt text](/imagenes/image-11.png)

## Ejecutar la Api en Flask
1. Clona el repositorio y entra en la carpeta del proyecto.
``` 
git clone <REPO_URL>
cd <PROJECT_FOLDER>
```
2. Instala las dependencias:
```
pip install -r requirements.txt
```

ejecuta el siguiente comando para poder correr la api
``` 
python3 app.py
```

## Pruebas con Postman
``` 
curl -X POST "http://localhost:8080/realms/CybersecurityRealm/protocol/openid-connect/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=api-client" \
     -d "client_secret=TU_SECRET_AQUI" \
     -d "grant_type=password" \
     -d "username=testuser" \
     -d "password=password123"
```

## Endpoints
- GET /public: Ruta pública sin autenticación.
- GET /private: Ruta protegida, requiere token válido.
- POST /data: Ruta protegida para enviar datos JSON.



