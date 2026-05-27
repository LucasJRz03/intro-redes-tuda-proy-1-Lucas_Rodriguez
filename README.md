# Proyecto: Shell Remoto Multihilo 

**Materia:** Introducción a las Redes.

**Institución:** Universidad Nacional de Tierra del Fuego (UNTDF)

**Alumno:** Lucas Rodríguez

## 1. Introducción
*El propósito de esta actividad es utilizar los sockets como recurso de comunicación ofrecido por el sistema operativo, a través de las librerías estándar de (`Python`), para desarrollar una aplicación Cliente/Servidor.
*El servidor implementado actúa como un intérprete de comandos remoto limitado, permitiendo a los clientes conectados ejecutar operaciones básicas de gestión de archivos.
*Cuenta con un sistema de autenticación de usuarios previo al acceso del shell para garantizar que solo usuarios autorizados puedan ejecutar comandos.

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

### Autenticación y Seguridad
* Antes de habilitar el shell interactivo, el servidor envía señales (`USER_PROMPT` y `PASS_PROMPT`) solicitando credenciales.
* En el cliente, se implementó la librería nativa `getpass` para enmascarar la contraseña introducida por el usuario en la terminal, evitando que se muestre en texto plano por pantalla.

### 3. Comandos Disponibles 
El shell remoto soporta los siguientes comandos tras una autenticación exitosa: 

* `help`: Muestra un listado de los comandos disponibles y su forma de uso.

* `pwd`: Imprime el directorio de trabajo actual.

* `mkdir <nombre>`: Crea un nuevo directorio en la ruta actual.

* `ls [ruta] [-l] [-lh]`: Lista el contenido de un directorio. Soporta el pasaje de parámetros para alterar su comportamiento:

* `ls`: Imprime únicamente los nombres de directorios y archivos. Se le puede especificar una ruta (ej. `ls /home`).

* `ls -l`: Imprime la salida en un formato tabular y detallado (tipo, tamaño en bytes, fecha de modificación y nombre).

* `ls -lh`: Combinado con `-l`, altera la representación numérica del tamaño del archivo a un formato comprensible por humanos (KB, MB, GB, etc.) para facilitar su lectura.

* `cat <archivo>`: Muestra el contenido de un archivo de texto específico.

* `exit`: Cierra la sesión actual, informando al servidor y finalizando la conexión del cliente.

---

### 4. Ejemplos de cómo ejecutar el servidor y el cliente. 

Debes tener minimo 2 VMs, una va a ser el 'servidor' y la otra el 'cliente'

**Paso 1: Iniciar el servidor**

El servidor debe ejecutarse primero para que el puerto quede a la escucha. En la terminal (en VM1) vas a ejecutar: <br>
(```python3 proy-1-srv-tcp.py```)

**Paso 2: Iniciar el cliente**

En la otra terminal (desde VM2), ejecutar:<br>
(```python3 proy-1-cli-tcp.py```)

**Paso 3: Autenticación y uso de la terminal**

Una vez ejecutado, se debería conectar y mostrarte el flujo de autenticación: 
(```Conectado al servidor {HOST}/{PORT}```)
(```Usuario: admin```)
(```Contraseña:```) 
<br>

(```Autenticación exitosa.```)
(```Escribe 'help' para ver los comandos disponibles.```)

(```escribir_comando> help ```)
<br>

_(Nota: Al escribir la contraseña, esta no se mostrará en pantalla por `getpass`)_

**Paso 3: Uso de la terminal**

Una vez conectado, el cliente interactúa enviando comandos al servidor y mostrando la respuesta recibida. Por ejemplo: 
__bash__<br>
(```Escribir_Comando> pwd```)<br>
deberías ver algo cómo <br>
(```/home/usuario```)

## 4. Diagrama de Flujo de Datos

```text
[ CLIENTE ]                                           [ SERVIDOR ]
     |                                                     |
     | --- (TCP Connect) --------------------------------> |  socket() -> bind() -> listen()
     |                                                     |  accept() [Bloqueado]
     | <--- (Conexión Aceptada) -------------------------- |  ¡Conexión establecida!
     |                                                     |  --> Crea un HILO nuevo
     |                                                     |
  [FASE DE LOGIN]                                          |
     | <--- "USER_PROMPT" -------------------------------- |  Verifica credenciales
     | --- Envia Usuario --------------------------------> |
     | <--- "PASS_PROMPT" -------------------------------- |
     | --- Envia Password (oculta por getpass) ----------> |
     | <--- "AUTH_OK" (o rechazo) ------------------------ |
     |                                                     |
  [FASE DE SHELL]                                          |
while True:                                           while True:
     | -- 1. Envía comando string (bytes) ---------------> |    |
     |                                                     |    |-- 2. recv() -> decode() -> split()
     |                                                     |    |-- 3. Procesa argumentos (ls -l, mkdir, etc)
     |                                                     |    |-- 4. Genera respuesta
     |                                                     |    |
     | <- 5. Recibe respuesta (bytes) -------------------- | <--| conn.send()
     |
(Muestra texto en pantalla)
```