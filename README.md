CORE (React + Flask )

Este proyecto "MVC" fue desarrollado de la siguiente manera:

FRONT END -> REACT (VIEW)
BACKEND -> FLASK (CONTROLLER )
BASE DE DATOS -> AZURE (MODEL)


En este mini core el frontend fue deployado en vercel con el siguiente URL: 
https://front-mvc.vercel.app/
el cual se conecta con el link de render "https://api-web-latest-nbk1.onrender.com" donde se encuentra despliegue de la API de FLASK para poder consumir los datos de la base de datos de azure.

Este minicore fue desarollado para poder ver el total de gastos por departamento según su fecha.
 

Para su funcionamiento tendrás que: 

 En PYTHON-FLASK:
 	- verificar la conexión con la base de datos de Azure 
 	- verificar que tengas todas las instalaciones necesarias para Flask, etc
 EN AZURE:
	 CREAR UNA BD CON EL NOMBRE: "MVCore"
	CREAR TABLAS DE ("Empleado", "Departamento", "Gasto")
 
 EN REACT:
	- verificar el link de de render para la conexión con el Backend
	y la despliegas en vercel nuevamente 


con estas indicaciones el proyecto esta listo para usarse

contacto:
hayland.montalvo@udla.edu.ec
0999567465


