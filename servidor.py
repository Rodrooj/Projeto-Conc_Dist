#!/usr/bin/env python3
import socket
import threading

HOST = '0.0.0.0'
PORT = 8080

# Estado compartilhado dos assentos: False = livre, True = reservado
seats = [False] * 100
seats_lock = threading.Lock()

def handle_client(conn, addr):
    """
    Trata uma conexão de cliente.
    Protocolo simples: cliente envia números de assentos separados por vírgula,
    ex: "10,20,30\n". Servidor responde linha por linha: "OK 10", "FAIL 20", etc.
    """
    print(f"[+] Conexão de {addr}")
    try:
        data = conn.recv(1024).decode('utf-8').strip()
        if not data:
            return
        pedidos = data.split(',')
        respostas = []
        # Tentar reservar cada assento pedido
        for p in pedidos:
            try:
                seat_no = int(p)
            except ValueError:
                respostas.append(f"ERROR {p}")
                continue
            if not (1 <= seat_no <= 100):
                respostas.append(f"INVALID {seat_no}")
                continue
            # seção crítica
            with seats_lock:
                if not seats[seat_no - 1]:
                    seats[seat_no - 1] = True
                    respostas.append(f"OK {seat_no}")
                else:
                    respostas.append(f"FAIL {seat_no}")
        # envia resposta
        conn.sendall(('\n'.join(respostas) + '\n').encode('utf-8'))
    finally:
        conn.close()
        print(f"[-] Desconectado {addr}")

def main():
    print(f"[*] Iniciando servidor em {HOST}:{PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    try:
        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[!] Servidor finalizando...")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
