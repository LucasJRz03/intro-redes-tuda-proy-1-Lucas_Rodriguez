# Proyecto: Shell Remoto Multihilo 

**Materia:** Introducción a las Redes.

**Institución:** Universidad Nacional de Tierra del Fuego (UNTDF)

**Alumno:** Lucas Rodríguez

## 1. Introducción
*El propósito de esta actividad es utilizar los sockets como recurso de comunicación ofrecido por el sistema operativo, a través de las librerías estándar de (`Python`), para desarrollar una aplicación Cliente/Servidor
*El servidor implementado actúa como un intérprete de comandos remoto limitado, permitiendo a los clientes conectados ejecutar operaciones básicas de gestión de archivos

## 2. Implementación Técnica

### ¿Cómo se implementó la comunicación con socket? 
La comunicación se hace gracias a la librería nativa `socket` de Python.
* Se implementó un servidor TCP utilizando la familia de direcciones IPv4(`AF_INET`) y el tipo de socket (`SOCK_STREAM`).
* El servidor escucha conexiones en todas las interfaces de red disponibles (`0.0.0.0`) y está configurada para escuchar en el puerto (`5500`).
* Se utiliza el método `listen(5)` para que el servidor pueda atender hasta 5 clientes de forma simultánea.
* El cliente, por su parte, instancia un socket idéntico y utiliza el método `connect()` apuntando a la IP y puerto del servidor. 

### ¿Cómo se gestionan los hilos en el servidor?
Para evitar que un cliente bloquee a los demás, el servidor maneja la concurrencia utilizando la librería `threading`.
* El servidor está en un ciclo infinito usando `while True` donde espera conexiones entrantes a través del método `accept()`.
* Una vez que un cliente se conecta, el servidor crea un hilo por cliente para manejar la comunicación de forma independiente. 
* Se instancia un objeto `threading.Thread`, pasando como objetivo (`target`) la función `manejar_cliente` y como argumentos el socket de conexión (`conn`) y la dirección del cliente (`addr`). Luego se invoca `start()` para iniciar la ejecución en paralelo. 

---

### Ejemplos de cómo ejecutar el servidor y el cliente. 

Debes tener minimo 2 VMs, una va a ser el 'servidor' y la otra el 'cliente'
**Paso 1: Iniciar el servidor**
El servidor debe ejecutarse primero para que el puerto quede a la escucha. En la terminal (en VM1) vas a ejecutar: 
`bash
python3 proy-1-srv-tcp.py`

**Paso 2: Iniciar el cliente**
En la otra terminal (desde VM2),ejecutar: 
`bash
python3 proy-1-cli-tcp.py`

**Paso 3: Uso de la terminal**
Una vez conectado, el cliente interactúa enviando comandos al servidor y mostrando la respuesta recibida



