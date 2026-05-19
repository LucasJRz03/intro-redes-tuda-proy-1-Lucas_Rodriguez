# Proyecto: Shell Remoto Multihilo 

**Materia:** Introducción a las Redes.
**Institución:** Universidad Nacional de Tierra del Fuego (UNTDF)
**Alumno:** Lucas Rodríguez

## 1. Introducción
*El propósito de esta actividad es utilizar los sockets como recurso de comunicación ofrecido por el sistema operativo, a través de las librerías estándar de (```PYTHON```), para desarrollar una aplicación Cliente/Servidor
*El servidor implementado actúa como un intérprete de comandos remoto limitado, permitiendo a los clientes conectados ejecutar operaciones básicas de gestión de archivos

## 2. Implementación Técnica
###¿Cómo se implementó la comunicación con socket? 
La comunicación se hace gracias a la librería nativa `socket` de Python.
* Se implementó un servidor TCP utilizando la familia de direcciones IPv4(`AF_INET`) y el tipo de socket (`SOCK_STREAM`).
* El servidor escucha conexiones en todas las interfaces de red disponibles (`0.0.0.0`) y está configurada para escuchar en el puerto (`5500`).
* Se utiliza el método `listen(5)` para que el servidor pueda atender hasta 5 clientes de forma simultánea.
* El cliente, por su parte, instancia un socket idéntico y utiliza el método `connect()` apuntando a la IP y puerto del servidor. 
