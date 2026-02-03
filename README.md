SoftJus - Sistema de Consulta Processual Brasileiro
https://via.placeholder.com/150x50/1976D2/FFFFFF?text=SoftJus

📋 Sobre o Projeto
SoftJus é um sistema desktop desenvolvido em Python com interface Kivy para consulta processual unificada em todos os tribunais brasileiros. O sistema permite pesquisar processos em mais de 85 tribunais diferentes através da API pública do DataJud do CNJ.

✨ Funcionalidades
🔍 Consulta Processual
Pesquisa por número de processo em qualquer tribunal brasileiro

Suporte a mais de 85 tribunais organizados por tipo:

Tribunais Superiores (TST, TSE, STJ, STM)

Justiça Federal (TRF1 a TRF6)

Justiça Estadual (Todos os 27 TJs)

Justiça do Trabalho (TRT1 a TRT24)

Justiça Eleitoral (TREs de todos os estados)

Justiça Militar (TJMMG, TJMRS, TJMSP)

⭐ Sistema de Favoritos
Adicione processos importantes à lista de favoritos

Visualização rápida dos processos favoritados

Informações salvas localmente em formato JSON

🎯 Filtros Inteligentes
Filtros por: Processo, Classe, Órgão Julgador, Data, Último Movimento

Sistema de busca em tempo real

Interface intuitiva com dropdowns

📱 Interface Moderna
Interface limpa e responsiva

Navegação por abas (Consulta, Favoritos, Atualizações)

Sistema de login com autenticação

Cards visuais para exibição de resultados

🏗️ Arquitetura do Projeto
text
softjus/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── app/                   # Módulo principal da aplicação
│   ├── __init__.py
│   ├── app.py            # Classe principal da aplicação
│   ├── screens/          # Telas da aplicação
│   │   ├── __init__.py
│   │   ├── login_screen.py      # Tela de login
│   │   ├── dashboard_screen.py  # Dashboard principal
│   │   ├── consulta_screen.py   # Tela de consulta
│   │   ├── favoritos_screen.py  # Tela de favoritos
│   │   └── atualizacoes_screen.py # Tela de atualizações
│   ├── widgets/          # Componentes de UI reutilizáveis
│   │   ├── __init__.py
│   │   ├── result_card.py      # Card de resultado
│   │   ├── favorite_card.py    # Card de favorito
│   │   └── update_card.py      # Card de atualização
│   ├── api/              # Integração com APIs
│   │   ├── __init__.py
│   │   ├── api_client.py      # Cliente HTTP para APIs
│   │   └── config.py          # Configurações e URLs
│   ├── storage/          # Armazenamento local
│   │   ├── __init__.py
│   │   ├── favorites_store.py # Gerenciamento de favoritos
│   │   └── data_formatter.py  # Formatação de dados
│   └── utils/            # Utilitários
│       ├── __init__.py
│       ├── helpers.py         # Funções auxiliares
│       └── validators.py      # Validações de dados
├── data/                 # Dados locais
│   ├── favorites.json   # Arquivo de favoritos
│   └── config.json      # Configurações da aplicação
└── assets/              # Recursos estáticos
    ├── fonts/          # Fontes personalizadas
    ├── icons/          # Ícones da aplicação
    └── images/         # Imagens e logos
🚀 Instalação e Execução
Pré-requisitos
Python 3.7 ou superior

pip (gerenciador de pacotes do Python)

Passos para Instalação
Clone ou baixe o projeto

Instale as dependências:

bash
pip install -r requirements.txt
Execute a aplicação:

bash
python main.py
Credenciais de Acesso
Usuário: admin

Senha: admin123

🛠️ Tecnologias Utilizadas
Python 3.9+ - Linguagem principal

Kivy 2.3.0 - Framework para interfaces gráficas

KivyMD 1.2.0 - Material Design para Kivy

Requests 2.31.0 - Cliente HTTP para APIs

JSON - Formato para armazenamento local

🔧 Configuração
URLs dos Tribunais
O sistema está pré-configurado com URLs para todos os tribunais brasileiros, incluindo:

Tribunais Superiores: 4 tribunais

Justiça Federal: 6 tribunais regionais

Justiça Estadual: 27 tribunais de justiça

Justiça do Trabalho: 24 tribunais regionais

Justiça Eleitoral: 27 tribunais regionais

Justiça Militar: 3 tribunais

Chave de API
O sistema utiliza a chave de API pública do DataJud/CNJ:

text
cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw
📊 Fluxo de Uso
Login: Acesse o sistema com as credenciais fornecidas

Seleção de Tribunal: Escolha o tipo de tribunal e depois o tribunal específico

Consulta: Digite o número do processo e clique em "Buscar"

Resultados: Visualize os dados processuais em cards organizados

Favoritos: Clique na estrela para adicionar/remover dos favoritos

Navegação: Use as abas para alternar entre consulta, favoritos e atualizações

🎨 Interface
Tela de Login
Design limpo com campos de usuário e senha

Validação em tempo real

Mensagens de erro claras

Dashboard Principal
Seletor de Tribunal: Dropdown em duas etapas (tipo → tribunal específico)

Área de Conteúdo: Abas para diferentes funcionalidades

Barra Superior: Logout e título da aplicação

Cards de Resultado
Número do processo em destaque

Informações da classe processual

Órgão julgador

Data de ajuizamento

Último movimento

Botão de favoritos

🔐 Segurança
Autenticação básica com credenciais pré-definidas

Armazenamento local seguro de favoritos

Comunicação HTTPS com APIs públicas

Dados sensíveis não são persistidos

📱 Compatibilidade
Sistemas Operacionais: Windows, Linux, macOS

Resolução Mínima: 1000x700 pixels

Conexão: Internet necessária para consultas à API

🔄 Atualizações
O sistema inclui uma aba de atualizações que mostra:

Histórico de mudanças

Novas funcionalidades

Correções de bugs

Melhorias de performance

🤝 Contribuição
Faça um fork do projeto

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

📞 Suporte
Para suporte, dúvidas ou sugestões:

Crie uma issue no repositório

Entre em contato com a equipe de desenvolvimento

🏢 Sobre a Equipe
SoftJus foi desenvolvido por uma equipe dedicada a simplificar o acesso à informação processual no Brasil. Nosso objetivo é tornar a consulta processual mais acessível e eficiente para todos os cidadãos.

Versão: 1.0.0
Última Atualização: Fevereiro 2024
Desenvolvido com ❤️ para a comunidade jurídica brasileira



📥 Como Instalar o SoftJus
Passo a Passo para Instalação
Pré-requisitos
Python 3.7 ou superior instalado

Pip (gerenciador de pacotes do Python)

Conexão com internet para baixar dependências

Windows
1. Verifique se tem Python instalado:
cmd
python --version
ou

cmd
py --version
2. Se não tiver Python, baixe e instale:
Acesse: python.org/downloads

Baixe a versão 3.9 ou superior

IMPORTANTE: Marque a opção "Add Python to PATH" durante a instalação

3. Crie uma pasta para o projeto:
cmd
mkdir SoftJus
cd SoftJus
4. Crie a estrutura de pastas:
cmd
mkdir app
mkdir app\screens app\widgets app\api app\storage app\utils
mkdir data assets
5. Copie os arquivos:
Copie todos os arquivos Python que eu forneci para suas respectivas pastas.

6. Crie o arquivo requirements.txt na pasta principal:
txt
kivy==2.3.0
kivymd==1.2.0
requests==2.31.0
python-dateutil==2.8.2
7. Instale as dependências:
cmd
pip install -r requirements.txt
8. Execute o programa:
cmd
python main.py
ou

cmd
py main.py
Mac/Linux
1. Verifique se tem Python instalado:
bash
python3 --version
2. Se não tiver Python, instale:
Ubuntu/Debian:

bash
sudo apt update
sudo apt install python3 python3-pip
Mac (com Homebrew):

bash
brew install python
3. Crie uma pasta para o projeto:
bash
mkdir SoftJus
cd SoftJus
4. Crie a estrutura de pastas:
bash
mkdir -p app/{screens,widgets,api,storage,utils}
mkdir -p data assets
5. Copie os arquivos para as pastas correspondentes
6. Crie e instale dependências:
bash
pip3 install kivy==2.3.0 kivymd==1.2.0 requests==2.31.0 python-dateutil==2.8.2
7. Execute:
bash
python3 main.py
🚨 Solução de Problemas Comuns
Erro: "ModuleNotFoundError: No module named 'kivy'"
cmd
pip install kivy==2.3.0
Erro: "ImportError: cannot import name '...'"
Verifique se todos os arquivos estão nas pastas corretas. A estrutura deve ser exatamente:

text
SoftJus/
├── main.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── login_screen.py
│   │   ├── dashboard_screen.py
│   │   ├── consulta_screen.py
│   │   ├── favoritos_screen.py
│   │   └── atualizacoes_screen.py
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── result_card.py
│   │   ├── favorite_card.py
│   │   └── update_card.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   └── config.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── favorites_store.py
│   │   └── data_formatter.py
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── validators.py
├── data/
└── assets/
Erro no Windows com instalação do Kivy
Tente instalar com:

cmd
pip install --pre --extra-index-url https://kivy.org/downloads/simple kivy[base]
Erro de permissão no Linux/Mac
bash
sudo pip3 install kivy==2.3.0
📦 Instalação Rápida (Script Automático)
Para Windows, crie um arquivo install.bat:
batch
@echo off
echo Instalando SoftJus...

REM Criar pastas
mkdir app 2>nul
mkdir app\screens 2>nul
mkdir app\widgets 2>nul
mkdir app\api 2>nul
mkdir app\storage 2>nul
mkdir app\utils 2>nul
mkdir data 2>nul
mkdir assets 2>nul

REM Criar requirements.txt
echo kivy==2.3.0 > requirements.txt
echo kivymd==1.2.0 >> requirements.txt
echo requests==2.31.0 >> requirements.txt
echo python-dateutil==2.8.2 >> requirements.txt

echo.
echo Instalando dependências...
pip install -r requirements.txt

echo.
echo Instalação concluída!
echo Execute: python main.py
pause
Para Linux/Mac, crie um arquivo install.sh:
bash
#!/bin/bash
echo "Instalando SoftJus..."

# Criar pastas
mkdir -p app/{screens,widgets,api,storage,utils}
mkdir -p data assets

# Criar requirements.txt
cat > requirements.txt << EOL
kivy==2.3.0
kivymd==1.2.0
requests==2.31.0
python-dateutil==2.8.2
EOL

echo
echo "Instalando dependências..."
pip3 install -r requirements.txt

echo
echo "Instalação concluída!"
echo "Execute: python3 main.py"
🎯 Verificação da Instalação
Teste se tudo está funcionando:
Execute o programa:

cmd
python main.py
A tela de login deve aparecer:

Use as credenciais:

Usuário: admin

Senha: admin123

Você deve ver o dashboard com o seletor de tribunais

🔧 Dicas para Desenvolvedores
Ambiente Virtual (Recomendado)
cmd
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
Atualizar dependências
cmd
pip install --upgrade kivy kivymd requests
Executar em modo debug
cmd
python -m main
📱 Executando em Diferentes Sistemas
Windows 10/11
Funciona nativamente

Requer Python 3.7+

Ubuntu 20.04+
bash
sudo apt-get install python3-pip
sudo apt-get install python3-dev python3-pip build-essential
MacOS
bash
brew install python
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer
🆘 Ainda com Problemas?
Verifique as versões:

cmd
python --version
pip --version
Atualize o pip:

cmd
pip install --upgrade pip
Instale manualmente cada pacote:

cmd
pip install kivy==2.3.0
pip install kivymd==1.2.0
pip install requests==2.31.0
Verifique os imports no código - todos devem estar corretos

Execute com mensagens de debug:

cmd
python -v main.py
✅ Sucesso na Instalação
Quando a instalação for bem-sucedida, você verá:

Uma janela com título "SoftJus - Consulta Processual"

Tela de login com campos de usuário e senha

Dashboard com seletor de tribunais após login

Funcionalidade completa de busca em todos os tribunais