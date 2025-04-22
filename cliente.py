#!/usr/bin/env python3
import socket
import sys

if len(sys.argv) < 3:
    print("Uso: python cliente.py <host> <assento1> [<assento2> ...]")
    sys.exit(1)

HOST = sys.argv[1]
# Converte argumentos seguintes em lista de inteiros
seats = sys.argv[2:]
request = ','.join(seats) + '\n'

PORT = 8080

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Não foi possível conectar a {HOST}:{PORT}")
            sys.exit(1)
        # envia pedido
        sock.sendall(request.encode('utf-8'))
        # recebe resposta
        resp = sock.recv(1024).decode('utf-8').strip()
        for line in resp.split('\n'):
            print(line)

if __name__ == '__main__':
    main()