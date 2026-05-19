import socket 
import threading
import os
HOST = '0.0.0.0'
PORT = 5500

def manejar_cliente(conn, addr):
    print(f"Cliente conectado desde {addr}")

    while True:
        try:
         comando = conn.recv(1024).decode('utf-8').strip()

         if not comando:
            break
            
         print(f"[{addr}] comando recibido:{comando}")

         if comando.lower() == 'exit':
            print(f"Cliente {addr} desconectado.")
            break
         
         elif comando.lower() == 'pwd':
            respuesta = os.getcwd()

         elif comando.lower() == 'ls':
            archivos = os.listdir('.')
            respuesta = '\n'.join(archivos) if archivos else 'Directorio vacío'
        
         elif comando.lower().startswith('cat'):
            nombre_archivo = comando[4:].strip()
            if os.path.isfile(nombre_archivo):
                with open(nombre_archivo, 'r') as f: 
                    respuesta = f.read()
            else:
               respuesta = f"Archivo '{nombre_archivo}' no encontrado."
         else:
            respuesta = "Error: comando inválido. Use ls, pwd,cat<archivo> o exit."
         conn.send(respuesta.encode('utf-8'))

        except Exception as e:
            print(f"[ERROR] con el cliente {addr}: {e}")
            break
        finally:
            conn.close()
            print(f"[DESCONECTADO] {addr} - finalizado.")

def iniciar_servidor():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(HOST,PORT)
   server.listen(5)
   print(f"[SERVER] Escuchando en el puerto: {PORT}")
   
   while True:
      conn, addr = server.accept()
      thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
      thread.start()

if __name__ == "__main__":
   iniciar_servidor()


    