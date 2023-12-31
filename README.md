#  SHOTEXT (ALPHA)
Ideia (resumo)
-
Tive a ideia de criar o Shotext quando estava assistindo as aulas da faculdade à distância e vi que eu estava pausando muito os videos para fazer algumas anotações, e isso estava me deixando frustrado, então fui a procura de um programa que facilitasse essa tarefa apenas tirando print da tela, mas infelizmente eu não achei, então por incrivel que pareça me veio a ideia de eu mesmo criar meu proprio app que faça isso por mim, não demorou muito até a primeira versão ficar pronta, apenas pensei que juntar uma biblioteca que tire print e uma que transforma imagens em texto já resolveria, e não é que funcionou? tive alguns problemas no começo pois não sou muito familiarizado com o python, porém no final deu tudo certo.

o SHOTEXT ainda não é 100% funcional, podendo não funcionar em Mac e Linux, porém pretendo atualizar futuramente para que seja 100% disponivel ao publico que se encontram no mesmo problema que eu.
# Instruções para Usuários
Seja bem-vindo ao Aplicativo de Captura e Conversão de Texto (SHOTEXT) usando Tesseract!

Antes de começar a utilizar a ferramenta, é importante seguir os passos abaixo para garantir que tudo funcione corretamente.

## Baixar o TESSERACT (Para Usuários)

Baixar o Tesseract é obrigatório para o uso do programa e para o desenvolvimento,
O Tesseract OCR é uma biblioteca essencial para a conversão de texto a partir das imagens capturadas. Siga as instruções abaixo para instalar o Tesseract no seu sistema:

1. Acesse o repositório oficial do Tesseract OCR no GitHub: https://github.com/tesseract-ocr/tesseract
2. Siga as instruções de instalação fornecidas no repositório para o seu sistema operacional específico.
3. Certifique-se de instalar também os pacotes de linguagem necessários durante a instalação do Tesseract. Essas linguagens são essenciais para a correta conversão do texto.
O Aplicativo de Captura e Conversão de Texto é uma ferramenta desenvolvida em Python que possibilita aos usuários capturar uma imagem da tela, converter qualquer texto presente na imagem usando a biblioteca Tesseract e, em seguida, enviar automaticamente o texto convertido para a área de transferência. O aplicativo funciona em segundo plano, permitindo um acesso rápido e conveniente a essa funcionalidade.

## Funcionalidades

- **Captura de Tela:** O aplicativo permite que os usuários capturem uma imagem da tela pressionando o atalho "Ctrl + [" ou clicando na opção "Screenshot" no menu do ícone do aplicativo.
- **Conversão de Texto:** O texto presente na imagem capturada é extraído e convertido utilizando a biblioteca Tesseract, um reconhecedor óptico de caracteres (OCR).
- **Envio para a Área de Transferência:** Após a conversão do texto, o aplicativo automaticamente envia o texto convertido para a área de transferência do sistema, permitindo que o usuário cole-o imediatamente em qualquer aplicativo.

## Requisitos do Sistema

- Python 3.x instalado
- Bibliotecas Python: `pyautogui`, `Pillow`, `pyperclip`, `keyboard`, `pytesseract`
- Tesseract OCR instalado e configurado no sistema

## Instalação e Uso

1. Verifique se o Python 3.x está instalado no seu sistema.
2. Instale as bibliotecas necessárias executando o seguinte comando:
`pip install pyautogui Pillow pyperclip keyboard pytesseract`
3. Instale o Tesseract OCR em seu sistema. Instruções de instalação estão disponíveis aqui: https://github.com/tesseract-ocr/tesseract
4. Clone este repositório em sua máquina ou baixe-o como um arquivo ZIP e descompacte-o.
5. Abra um terminal na pasta onde o aplicativo está localizado.
6. Execute o aplicativo usando o seguinte comando: `python app.py`
7. O aplicativo agora está em execução em segundo plano.
8. Para capturar uma imagem da tela e converter o texto, pressione "Ctrl + [" ou clique na opção "Screenshot" no menu do ícone do aplicativo.
9. O texto convertido estará na área de transferência e poderá ser colado em qualquer aplicativo.

## Personalização do Atalho

Se você deseja alterar o atalho padrão "Ctrl + [" para capturar a imagem da tela, é possível editar o arquivo `app.py` e procurar pela seção onde o atalho é definido. Você precisará importar a biblioteca `keyboard` e modificar o atalho de acordo com sua preferência. Certifique-se de escolher um atalho que não entre em conflito com outros atalhos do sistema.

```python
# Defina o atalho personalizado para capturar a imagem da tela
keyboard.add_hotkey("ctrl+[", on_press_key)
