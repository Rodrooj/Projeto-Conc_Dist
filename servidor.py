import socket
import threading

HOST = '0.0.0.0'
PORT = 8080

# Lista com 100 assentos, livres (False)
seats = [False] * 100

# Bloqueio para evitar que duas pessoas reservem o mesmo assento ao mesmo tempo
seats_lock = threading.Lock()

# Essa função lida com cada cliente que se conecta ao servidor
def handle_client(conn, addr):
    print(f"[+] Cliente conectado: {addr}")
    try:
        # Recebe a mensagem do cliente
        data = conn.recv(1024).decode('utf-8').strip()
        if not data:
            return
        
        # O cliente pode pedir vários assentos separados por vírgulas
        pedidos = data.split(',')
        respostas = []

        for pedido in pedidos:
            try:
                # Converte o número do assento para inteiro
                seat_number = int(pedido)
            except ValueError:
                respostas.append(f"ERROR {pedido}")
                continue

            if seat_number < 1 or seat_number > 100:
                respostas.append(f"INVALID {seat_number}")
                continue

            # Bloqueia o acesso aos assentos para evitar conflitos com outros clientes
            with seats_lock:
                if not seats[seat_number - 1]:
                    seats[seat_number - 1] = True
                    respostas.append(f"OK {seat_number}")
                else:
                    respostas.append(f"FAIL {seat_number}")

        # Envia a resposta final ao cliente
        resposta_final = '\n'.join(respostas) + '\n'
        conn.sendall(resposta_final.encode('utf-8'))

    finally:
        conn.close()
        print(f"[-] Cliente desconectado: {addr}")

def main():
    print(f"[*] Servidor iniciado em {HOST}:{PORT}")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    try:
        while True:
            # Espera por uma nova conexão
            conn, addr = servidor.accept()
            # Cria uma nova thread para lidar com esse cliente
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Encerrando servidor...")
    finally:
        servidor.close()

# Inicia o servidor se o script for executado diretamente
if __name__ == '__main__':
    main()
