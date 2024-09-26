# SUGL - Sistema Universal de Empréstimo de Livros

Este projeto é um sistema de gerenciamento de empréstimos de livros para bibliotecas comunitárias. O sistema permite registrar e controlar empréstimos de livros e devoluções, utilizando uma interface com **Flask** (backend), **PostgreSQL** (banco de dados) e **Telegram** (para notificações).

## Funcionalidades

- Registro de livros no sistema
- Registro de usuários (membros da biblioteca)
- Registro de empréstimos de livros
- Controle de devoluções e atualização do status do livro
- Notificação via Telegram sobre empréstimos e devoluções
- Relatório de livros disponíveis e emprestados

## Tecnologias Utilizadas

- **Flask** - Framework web em Python para o backend
- **PostgreSQL** - Banco de dados relacional para armazenar as informações dos livros, usuários, e transações
- **Telegram API** - Para enviar notificações automáticas aos usuários

## Requisitos

- **Python 3.x**
- **PostgreSQL** instalado e configurado
- **Conta no Telegram** para usar a API de Bots
- **Flask** e dependências listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/biblioteca-comunitaria.git
   
