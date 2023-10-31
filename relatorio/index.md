---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Um Serviço de Stream de Dados"
subtitle: "Trabalho Prático de Redes de Computadores II - Turma 2023/2"
summary: "Relatório do Trabalho Prático de Redes de Computadores II" 
authors: []
# tags: [networks, python]
categories: []
date: 2023-10-22T16:20:35-03:00
featured: false
draft: false


# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []

url_code: https://github.com/PedroKochinski/stream-server

---
<a href="https://br.freepik.com/vetores-gratis/conceito-de-processamento-de-dados-grandes-sala-de-servidores-acesso-ao-token-de-tecnologia-blockchain_3629651.htm#&position=3&from_view=author">Imagem de fullvector</a> no Freepik


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

ou alternativamente:

```bash
pip install pydub==0.25.1
```

## Funcionamento


### Cliente
O cliente se comunica com um servidor para receber e reproduzir áudio. Ele inicia estabelecendo uma conexão com o servidor e envia uma mensagem de **solicitação de conexão**. O servidor pode aceitar ou rejeitar a conexão com base na capacidade atual. Após a conexão ser estabelecida, o cliente começa a **receber dados de áudio** do servidor em segmentos e os reproduz. 

O cliente mantém uma fila de segmentos de áudio (*buffer*) para garantir uma reprodução contínua. Ele lida com mensagens de controle do servidor, como o encerramento da transmissão, a detecção de perda de pacotes e mensagens de erro, registrando essas informações em um arquivo de log. O cliente possui duas *threads*: uma para **receber mensagens** e outra para **reproduzir o áudio**. Ele pode ser encerrado manualmente ou após o término da transmissão, assim exibe estatísticas sobre as mensagens recebidas e perdidas.


### Servidor
O servidor escuta em uma porta específica e **gerencia a comunicação com vários clientes**. Quando um cliente solicita uma conexão, o servidor decide aceitar ou rejeitar com base na capacidade de atendimento. Se aceita, o servidor mantém uma lista de endereços dos clientes conectados. O servidor tem duas *threads* principais: uma para **receber mensagens dos clientes** e outra para **enviar dados de áudio para todos os clientes conectados**. 

O servidor envia dados de áudio em segmentos para todos os clientes em intervalos regulares. Ele também **lida com mensagens de controle**, como o encerramento da transmissão. O servidor **registra todas as atividades em um arquivo de log**. Quando a transmissão é concluída ou o servidor é encerrado manualmente, ele envia uma mensagem de encerramento para todos os clientes e encerra suas operações.

### Mensagens

As mensagens são compostas por campos específicos, e são utilizadas para a comunicação entre o cliente e o servidor. A classe `Message` implementa os métodos para enviar e receber mensagens, e também para converter uma mensagem em bytes e vice-versa. Todas as mensagens possuem os seguintes campos:

* `sequencia`: identificador utilizado para verificar a ordem das mensagens
* `tipo`: utilizado para identificar o tipo da mensagem e adaptar o tratamento
* `dados`: conjunto de bytes pode ser texto ou trechos de áudio

## Código
* [server.py](server.py.txt): implementação do **Servidor** 
* [client.py](client.py.txt): implementação do **Cliente**
* [message.py](message.py.txt): implementação da classe **Mensagem**
* [requirements.txt](requirements.txt): pacotes necessários


## Logs
* [server.log](server.log.txt): log do **servidor**
* [client.log](client.log.txt): log do **cliente**

## Projeto
A implementação completa do projeto está disponível no GitHub:

{{< icon name="fab fa-github" pack="fab" >}} [Respositório](https://github.com/PedroKochinski/stream-server)

<br>

