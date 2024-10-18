# Streaming de Áudio UDP/IP

## Autores
* [Pedro Henrique Kochinski Silva](https://github.com/PedroKochinski/stream-server)
* [Vinícius Mioto](https://github.com/viniciusmioto)

## Introdução
Este relatório apresenta a implementação de um servidor de *streaming* capaz de transmitir áudio (mp3). Cada stream é composto por mensagens com campos específicos, e é possível ajustar o intervalo entre essas mensagens. Vários clientes podem se conectar ao servidor via **UDP/IP** para receber o stream, e ao encerrar, o cliente gera estatísticas sobre a qualidade da transmissão. A operação sobre os dados recebidos pelo cliente se dá pela reprodução do áudio.

## Implementação

O trabalho foi implementado utilizando a linguagem **Python3** e testado no laboratório 12 do Departamento de Informática da UFPR.

Para o funcionamento correto do Cliente, é necessário ter instalado o pacote `pydub==0.25.1`.

A instalação pode ser feita com o comando:

```bash
pip install -r requirements.txt
```

## Funcionamento


### Cliente
O cliente se comunica com um servidor para receber e reproduzir áudio. Ele inicia estabelecendo uma conexão com o servidor e envia uma mensagem de **solicitação de conexão**. O servidor pode aceitar ou rejeitar a conexão com base na capacidade atual. Após a conexão ser estabelecida, o cliente começa a **receber dados de áudio** do servidor em segmentos e os reproduz. 

O cliente mantém uma fila de segmentos de áudio (*buffer*) para garantir uma reprodução contínua. Ele lida com mensagens de controle do servidor, como o encerramento da transmissão, a detecção de perda de pacotes e mensagens de erro, registrando essas informações em um arquivo de log. O cliente possui duas *threads*: uma para **receber mensagens** e outra para **reproduzir o áudio**. Ele pode ser encerrado manualmente ou após o término da transmissão, assim exibe estatísticas sobre as mensagens recebidas e perdidas.

Para executar o cliente, basta executar o comando:

```bash
python3 client.py <porta> <ip>
```

Vale ressaltar que o servidor deve estar em execução para que o cliente funcione corretamente. Após isso, o áudio será reproduzido na máquina do cliente.

### Servidor
O servidor escuta em uma porta específica e **gerencia a comunicação com vários clientes**. Quando um cliente solicita uma conexão, o servidor decide aceitar ou rejeitar com base na capacidade de atendimento. Se aceita, o servidor mantém uma lista de endereços dos clientes conectados. O servidor tem duas *threads* principais: uma para **receber mensagens dos clientes** e outra para **enviar dados de áudio para todos os clientes conectados**. 

O servidor envia dados de áudio em segmentos para todos os clientes em intervalos regulares. Ele também **lida com mensagens de controle**, como o encerramento da transmissão. O servidor **registra todas as atividades em um arquivo de log**. Quando a transmissão é concluída ou o servidor é encerrado manualmente, ele envia uma mensagem de encerramento para todos os clientes e encerra suas operações.

Para executar o servidor, basta executar o comando:

```bash
python3 server.py <porta>
```

Após isso, o programa irá solicitar qual arquivo de áudio deve ser transmitido e qual taxa de envio das mensagens em segundos.

### Mensagens

As mensagens são compostas por campos específicos, e são utilizadas para a comunicação entre o cliente e o servidor. A classe `Message` implementa os métodos para enviar e receber mensagens, e também para converter uma mensagem em bytes e vice-versa. Todas as mensagens possuem os seguintes campos:

* `sequencia`: identificador utilizado para verificar a ordem das mensagens
* `tipo`: utilizado para identificar o tipo da mensagem e adaptar o tratamento
* `dados`: conjunto de bytes pode ser texto ou trechos de áudio

## Código Fonte
* [server.py](server.py.txt): implementação do **Servidor** 
* [client.py](client.py.txt): implementação do **Cliente**
* [message.py](message.py.txt): implementação da classe **Mensagem**
* [requirements.txt](requirements.txt): pacotes necessários

## Arquivos de Logs
* [server.log](server.log.txt): log do **servidor**
* [client.log](client.log.txt): log do **cliente**

<br>

