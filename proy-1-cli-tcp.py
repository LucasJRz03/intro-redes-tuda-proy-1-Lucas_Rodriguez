import socket

HOST = '192.168.10.1'
PORT = 5500

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
        print(f"\nConectado al servidor {HOST}:{PORT}")
        print("Comandos disponibles: ls,pwd, cat<archivo>, exit")

        while True:
            comando = input("\nEscribir_Comando> ")

            if not comando.strip():
                continue 

            cliente.send(comando.encode('utf-8'))

            respuesta = cliente.recv(4096).decode('utf-8')
            print(respuesta)

            if comando.strip() == 'exit':
                break

    except Exception as e: 
        print(f"[ERROR] Ocurrio un problema: {e}")

    finally:
        cliente.close() 

if __name__ == "__main__":
    iniciar_cliente()
    