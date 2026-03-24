import socket

# Configurações de conexão
MEU_IP = ''  # Ouve em todas as interfaces
MINHA_PORTA = 8000 

# Criação do socket: AF_INET (IPv4) e SOCK_STREAM (TCP)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reutilizar a porta rapidamente se o servidor for reiniciado
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp.bind((MEU_IP, MINHA_PORTA))
tcp.listen(1) # Aguarda até 1 conexão na fila
print(f"Servidor iniciado na porta {MINHA_PORTA}. Aguardando cliente...")

# Aceita a conexão (o programa trava aqui até alguém conectar)
conexao, docliente = tcp.accept()
print(f"O cliente {docliente} se conectou!")

try:
    while True:
        # Recebe os dados em formato de bytes (limite de 1024 bytes por vez)
        mensagem_bytes = conexao.recv(1024)
        
        # VALIDAÇÃO 1: Se não houver bytes, o cliente desconectou
        if not mensagem_bytes:
            print("O cliente encerrou a conexão.")
            break
            
        # Decodifica de bytes para string para podermos ler
        mensagem_texto = mensagem_bytes.decode('utf-8').strip()
        print(f"Recebi do cliente: {mensagem_texto}")

        # VALIDAÇÃO 2 e PROCESSAMENTO: Regras de negócio do nosso servidor
        if mensagem_texto.upper() == 'SAIR':
            resposta = "Encerrando conexão a seu pedido. Tchau!"
            conexao.sendall(resposta.encode('utf-8'))
            break
            
        elif mensagem_texto.isnumeric():
            # Se for número, multiplica por 2
            resultado = int(mensagem_texto) * 2
            resposta = f"Sua entrada foi validada como NÚMERO. O dobro é {resultado}."
            
        else:
            # Se for texto comum
            resposta = f"Sua entrada foi validada como TEXTO. Confirmação: {mensagem_texto}"

        # RETORNO EM TEMPO REAL: Envia a resposta processada de volta ao cliente
        conexao.sendall(resposta.encode('utf-8'))

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Garante que as portas sejam liberadas no final
    conexao.close()
    tcp.close()
    print("Fim do socket do servidor.")
