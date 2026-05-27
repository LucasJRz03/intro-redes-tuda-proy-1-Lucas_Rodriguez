import socket
import getpass

HOST = '192.168.10.1'
PORT = 5500

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        print(f"\nConectado al servidor {HOST}:{PORT}")
        # --- fase de login ---
        autenticado = False
        while not autenticado:
            peticion = cliente.recv(1024).decode('utf-8')

            if peticion == "USER_PROMPT":
                usuario = input("Usuario: ")
                cliente.send(usuario.encode('utf-8'))
            
            elif peticion == "PASS_PROMPT":
                # getpass enmascara la entrada para que no se vea la contraseña
                password = getpass.getpass("Contraseña: ")
                cliente.send(password.encode('utf-8'))
            
            elif peticion.startswith("AUTH_FAIL"):
                mensaje_error = peticion.split('|')[1]
                print(f"\n[X] {mensaje_error}")
                return # Cierra el cliente si falla
            
            elif peticion == "AUTH_OK":
                print("\n[✔] Autenticación exitosa.")
                print("Escribe 'help' para ver los comandos disponibles.")
                autenticado = True

        # --- fase del shell ---

        while True:
            comando = input("\nescribir_comando> ")

            if not comando.strip():
                continue 

            cliente.send(comando.encode('utf-8'))

            # aumentamos el buffer para recibir respuestas más largas
            respuesta = cliente.recv(8192).decode('utf-8')
            print(respuesta)

            if comando.strip().lower() == 'exit':
                break

    except ConnectionRefusedError:
        print("[ERROR] El servidor rechazó la conexión (¿Está encendido?)")
    except Exception as e: 
        print(f"[ERROR] Ocurrio un problema: {e}")

    finally:
        cliente.close() 

if __name__ == "__main__":
    iniciar_cliente()
    