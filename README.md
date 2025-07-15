# 🔥 Discord Flame Messenger Pro

Uma solução moderna e intuitiva para automação de mensagens no Discord com interface gráfica elegante e controles avançados.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Configuração](#configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O Discord Flame Messenger Pro foi desenvolvido para resolver um problema específico: **automatizar o envio de mensagens no Discord sem a necessidade de manter o computador principal ligado constantemente**.

### 💡 Origem do Projeto

Este script foi criado para ajudar um amigo que precisava:
- Divulgar links específicos no Discord para várias pessoas
- Enviar mensagens automáticas em intervalos regulares
- Fazer isso sem precisar ficar com o PC pessoal ligado 24/7

### 🚀 Solução Implementada

Para resolver esse problema, foi criada uma **VPS (Virtual Private Server) usando o Paperspace**, onde foi configurado um ambiente Linux com interface gráfica. O script foi desenvolvido com uma interface amigável que permite configurar facilmente todas as automações necessárias.

## ✨ Características

### 🎨 Interface Moderna
- Design inspirado no Discord com tema dark
- Interface responsiva e intuitiva
- Animações e efeitos visuais modernos
- Suporte completo a scroll para listas extensas

### 🎯 Funcionalidades Principais
- **Automação de Cliques**: Configure coordenadas específicas para automação
- **Envio de Mensagens**: Envie mensagens personalizadas automaticamente
- **Controle de Tempo**: Configure intervalos personalizados entre ciclos
- **Múltiplas Coordenadas**: Gerencie várias abas e conversas simultaneamente
- **Persistência de Dados**: Salva automaticamente todas as configurações

### 🛠️ Recursos Avançados
- **Monitor de Posição do Mouse**: Visualização em tempo real da posição do cursor
- **Sistema de Status**: Acompanhe o progresso da automação em tempo real
- **Backup Automático**: Configurações salvas automaticamente em JSON
- **Controles Intuitivos**: Botões modernos com feedback visual
- **Validação de Dados**: Verificação automática de entrada de dados

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

```bash
# Python 3.7 ou superior
python --version

# Pip (gerenciador de pacotes do Python)
pip --version
```

### 📦 Dependências Necessárias

```bash
pip install pyautogui
pip install tkinter  # Geralmente já vem com Python
```

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/discord-flame-messenger.git
cd discord-flame-messenger
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o programa**
```bash
python discord2.py
```

## 📖 Como Usar

### 1. 🎯 Configuração Inicial

1. **Abra o programa** - Execute o script e a interface gráfica será exibida
2. **Configure a mensagem** - Digite a mensagem que deseja enviar automaticamente
3. **Defina o tempo de pausa** - Configure o intervalo entre os ciclos (em minutos)

### 2. 📍 Adicionando Coordenadas

Para cada conversa/canal que você quer automatizar:

1. **Clique em "➕ Adicionar"**
2. **Preencha os campos**:
   - **Coordenada X/Y da Aba**: Posição do clique para selecionar a aba
   - **Coordenada X/Y da Conversa**: Posição do clique para selecionar a conversa

3. **Use o monitor de posição** para encontrar as coordenadas exatas

### 3. ▶️ Executando a Automação

1. **Verifique suas configurações**
2. **Clique em "▶️ Iniciar Automação"**
3. **Aguarde 5 segundos** - O sistema iniciará automaticamente
4. **Monitore o status** - Acompanhe o progresso na seção de status

### 4. ⏹️ Parando a Automação

- Clique em "⏹️ Parar Automação" a qualquer momento
- O sistema para de forma segura após o ciclo atual

## ⚙️ Configuração

### 📁 Arquivo de Configuração

O programa salva automaticamente as configurações em `discord_config.json`:

```json
{
  "coordenadas": [
    [x1, y1, x2, y2],
    [x1, y1, x2, y2]
  ],
  "mensagem": "Sua mensagem aqui",
  "pause_minutes": 10,
  "saved_at": "2024-01-01T12:00:00"
}
```

### 🎛️ Parâmetros Configuráveis

- **Mensagem**: Texto que será enviado automaticamente
- **Tempo de Pausa**: Intervalo entre ciclos (mínimo 1 minuto)
- **Coordenadas**: Lista de posições para cliques automáticos
- **Fail-safe**: Proteção automática do PyAutoGUI ativada

## 🏗️ Estrutura do Projeto

```
discord-flame-messenger/
├── discord2.py              # Arquivo principal
├── discord_config.json      # Configurações salvas
├── requirements.txt         # Dependências
├── README.md               # Este arquivo
└── assets/                 # Recursos adicionais
    └── screenshots/        # Capturas de tela
```

### 🔧 Componentes Principais

- **`DiscordBotApp`**: Classe principal da aplicação
- **`ModernDialog`**: Diálogos customizados para entrada de dados
- **`ModernButton`**: Botões estilizados com efeitos hover
- **Sistema de Scroll**: Suporte completo para listas extensas
- **Monitor de Mouse**: Tracking em tempo real da posição do cursor

## 💻 Tecnologias Utilizadas

- **Python 3.7+** - Linguagem principal
- **Tkinter** - Interface gráfica nativa
- **PyAutoGUI** - Automação de mouse e teclado
- **JSON** - Persistência de configurações
- **Threading** - Execução assíncrona da automação

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Siga estes passos:

1. **Fork o projeto**
2. **Crie uma branch** (`git checkout -b feature/nova-funcionalidade`)
3. **Commit suas mudanças** (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push para a branch** (`git push origin feature/nova-funcionalidade`)
5. **Abra um Pull Request**

## ⚠️ Aviso Legal

Este software é fornecido apenas para fins educacionais e de automação pessoal. Certifique-se de:

- Respeitar os Termos de Serviço do Discord
- Usar apenas em servidores onde você tem permissão
- Não usar para spam ou atividades maliciosas
- Seguir as diretrizes da comunidade

## 📞 Contato

Se você tiver dúvidas ou sugestões, sinta-se à vontade para:

- Abrir uma issue no GitHub
- Enviar um pull request
- Entrar em contato diretamente

---

**Desenvolvido com ❤️ para a comunidade**

*"Automatizando o mundo, uma mensagem por vez"* 🚀
