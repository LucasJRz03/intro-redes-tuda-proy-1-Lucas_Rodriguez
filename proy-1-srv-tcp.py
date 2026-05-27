import socket 
import threading
import os
import datetime

HOST = '0.0.0.0'
PORT = 5500

#BD
USUARIO_VALIDO = {
   "admin": "root1",
   "usuario": "123456"
}

def size_readable(bytes_size):
   """Convierte bytes a un formato legible (KB, MB, etc.)"""
   for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
      if bytes_size < 1024.0:
         return f"{bytes_size:.1f}{unit}B" if unit else f"{bytes_size}{unit}B"
      bytes_size /= 1024.0
   return f"{bytes_size:.1f}YB"

def manejar_cliente(conn, addr):
    print(f"\n[INFO] Cliente conectado desde {addr}")

    try:

      # --- Fase de Login ---
        conn.send("USER_PROMPT".encode('utf-8'))
        usuario = conn.recv(1024).decode('utf-8').strip()

        conn.send("PASS_PROMPT".encode('utf-8'))
        password = conn.recv(1024).decode('utf-8').strip()
      
        if USUARIO_VALIDO.get(usuario) != password:
            conn.send("AUTH_FAIL|Credenciales incorrectas. Acceso denegado.".encode('utf-8'))
            print(f"[AUTH] Fallo de autenticación para {addr} (Usuario: {usuario})")
            return # Termina la conexión

        conn.send("AUTH_OK".encode('utf-8'))
        print(f"[AUTH] {addr} autenticado exitosamente como '{usuario}'.")
      #---------------------- 
      # --- Fase del Shell ---
        while True:
            comando = conn.recv(1024).decode('utf-8').strip()

            if not comando:
               break
            
            print(f"[{addr}] - [{usuario}] comando recibido:{comando}")
            partes_sh = comando.split()
            shell_r = partes_sh[0].lower()

            if shell_r == 'exit':
               conn.send("[INFO] Cerrando conexión...".encode('utf-8'))
               break
            
            elif shell_r == 'help':
               respuesta = """ 
               Comandos disponibles:
               help               : Muestra este mensaje de ayuda.
               pwd                : Muestra el directorio de trabajo actual.
               ls [-l] [-lh] [dir]: Lista el contenido del directorio actual o el especificado.
                       -l  : Muestra formato detallado.
                       -lh : Formato detallado con tamaños legibles.
               mkdir <nombre>     : Crea un nuevo directorio en la ruta actual.
               cat <archivo>      : Muestra el contenido de un archivo de texto.
               exit               : Cierra la sesión y desconecta el cliente.
               """

            

            if shell_r == 'exit':
               conn.send("[INFO] Cerrando conexión...".encode('utf-8'))
               break
         
            elif shell_r == 'pwd':
               respuesta = os.getcwd()

            elif shell_r == 'mkdir':
               if len(partes_sh) > 1:
                  nombre_directorio = partes_sh[1]
                  try:
                     os.makedirs(nombre_directorio, exist_ok=False)
                     respuesta = f"[INFO] Directorio '{nombre_directorio}' creado exitosamente."
                  except FileExistsError:
                     respuesta = f"[ERROR] El directorio '{nombre_directorio}' ya existe."
                  except Exception as e:
                     respuesta = f"[ERROR] No se pudo crear el directorio: {e}"
               else:
                  respuesta = "[ERROR] Uso incorrecto. Sintaxis: mkdir <nombre_directorio>"
                  
            elif shell_r() == 'ls':
               # Procesar argumentos de ls
               flags = [p for p in partes_sh[1:] if p.startswith('-')]
               rutas = [p for p in partes_sh[1:] if not p.startswith('-')]
               ruta_objetivo = rutas[0] if rutas else '.'
               formato_l = '-l' in flags or '-lh' in flags or '-hl' in flags
               formato_h = '-lh' in flags or '-hl' in flags
               
               try:
                  entradas = list(os.scandir(ruta_objetivo))
                  if not formato_l:
                     # comportamiento estándar
                     respuesta = '\n'.join(e.name for e in entradas) if entradas else 'Directorio vacío'
                  else:
                     # comportamiento con (-l / -lh)
                     lineas = []
                     for e in entradas:
                        stat = e.stat()
                        tipo = 'd' if e.is_dir() else '-'
                        size = stat.st_size
                        size_str = size_readable(size) if formato_h else str(size)

                        # Obtener fecha de modificación
                        fecha_mod = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')

                        # Formato tabular: [tipo] [tamaño] [fecha] [nombre]
                        lineas.append(f"{tipo} {size_str:>10} {fecha_mod} {e.name}")
                     respuesta = '\n'.join(lineas) if lineas else 'Directorio vacío'
               except FileNotFoundError:
                  respuesta= f"[ERROR] La ruta '{ruta_objetivo}' no existe."
               except NotADirectoryError:
                  respuesta = f"[ERROR] '{ruta_objetivo}' no es un directorio válido."
               except Exception as e:
                  respuesta = f"[ERROR] Ocurrió un error con ls: {e}"
        
            elif shell_r == 'cat':
               if len(partes_sh) > 1:
                  nombre_archivo = " ".join(partes_sh[1:])
                  if os.path.isfile(nombre_archivo):
                     with open(nombre_archivo, 'r') as archivo: 
                        respuesta = archivo.read()
                  else:
                     respuesta = f"[ERROR] Archivo '{nombre_archivo}' no encontrado."
               else: 
                  respuesta = "[ERROR] Uso incorrecto. Sintaxis: cat <nombre_archivo>"
            else:
               respuesta = "[ERROR] comando inválido. Escriba 'help' para ver la lista de comandos."

            conn.send(respuesta.encode('utf-8'))

    except ConnectionResetError:
        print(f"[ERROR] El cliente {addr} forzó la desconexión.")
    except Exception as e:
        print(f"[ERROR] con el cliente {addr}: {e}")

    finally:
        conn.close()
        print(f"[DESCONECTADO] {addr} - finalizado.")

def iniciar_servidor():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind((HOST,PORT))
   server.listen(5)
   print(f"[SERVER] Escuchando en el puerto: {PORT}")
   print(f"[SERVER] Usuarios registrados para pruebas: {list(USUARIO_VALIDO.keys())}")

   while True:
      conn, addr = server.accept()
      thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
      thread.start()

if __name__ == "__main__":
   iniciar_servidor()
