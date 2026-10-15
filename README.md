# Raiz — Gerenciamento de Tarefas

Uma base em construção para uma API de gerenciamento de tarefas. O repositório ainda não contém a API CRUD descrita no diagrama de arquitetura: no momento, inclui uma função simples para adicionar itens a um carrinho, as dependências Python listadas e um diagrama da arquitetura planejada.

## Índice

1. [Tecnologias utilizadas](#tecnologias-utilizadas)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação e configuração](#instalação-e-configuração)
4. [Uso e exemplos](#uso-e-exemplos)
5. [Estrutura do projeto](#estrutura-do-projeto)
6. [Testes](#testes)
7. [Limitações e próximos passos](#limitações-e-próximos-passos)
8. [Contribuição](#contribuição)
9. [Licença](#licença)

## Tecnologias utilizadas

- **Linguagem:** Python (a função atual usa anotações de tipo da sintaxe Python 3.9+).
- **Dependências fixadas** em `requirements.txt` e espelhadas em `pyproject.toml`:
  - SQLAlchemy 3.3.6
  - Pydantic 2.14.1
  - Psycopg 2.1.4, com binários
- Esses pins vêm dos arquivos do projeto; não foram confirmados por um ambiente Pipenv instalado. FastAPI e Psycopg2 não estão declarados nas dependências atuais.
- **Arquitetura planejada**, conforme `arquitetura.md`: frontend React, API FastAPI, validação Pydantic, persistência SQLAlchemy e PostgreSQL.
- **Infraestrutura:** PostgreSQL está no desenho arquitetural, mas ainda não há configuração de banco ou containers no repositório.
- **Assistentes de IA:** não há ferramentas ou versões documentadas no projeto.

## Pré-requisitos

- Python 3.11 recomendado (Python 3.9 ou superior para executar o código atual).
- Git.
- `venv` e `pip`, incluídos na instalação padrão do Python.

PostgreSQL, Docker e Node.js não são necessários para executar o código atualmente presente. Poderão ser necessários quando a API e a arquitetura planejada forem implementadas.

## Instalação e configuração

Clone o repositório e crie um ambiente virtual:

```bash
git clone https://github.com/adrianomandrade-png/Raiz-Gerenciamento_de_Tarefas.git
cd Raiz-Gerenciamento_de_Tarefas
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências declaradas:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Como alternativa, usando Poetry:

```bash
poetry install
```

O código atual não lê variáveis de ambiente, não exige arquivo `.env` e não conecta a um banco de dados. Não há configuração de containers no repositório.

## Uso e exemplos

Ainda não há servidor FastAPI nem endpoints HTTP implementados. A função disponível pode ser usada diretamente em Python:

```python
from shopping_cart import add_item_to_cart

cart: dict[str, int] = {}
add_item_to_cart(cart, "caderno", 3)

print(cart)
# {'caderno': 3}
```

Para executar o exemplo sem criar um arquivo:

```bash
python -c 'from shopping_cart import add_item_to_cart; cart = {}; add_item_to_cart(cart, "caderno", 3); print(cart)'
```

## Estrutura do projeto

```text
.
├── LICENSE             # Licença MIT
├── README.md           # Visão geral e instruções do projeto
├── arquitetura.md      # Diagrama da arquitetura planejada
├── pyproject.toml      # Configuração básica de dependências para Poetry
├── requirements.txt    # Dependências Python fixadas
├── shopping_cart.py    # Função atual para adicionar item ao carrinho
└── .gitignore          # Arquivos e diretórios ignorados pelo Git
```

## Testes

O repositório ainda não contém testes automatizados nem configura Pytest ou cobertura. Para preparar essas ferramentas:

```bash
python -m pip install pytest pytest-cov
```

Quando os testes forem adicionados, execute-os e gere um relatório de cobertura com:

```bash
python -m pytest
python -m pytest --cov=shopping_cart --cov-report=term-missing
```

## Limitações e próximos passos

- A função atual trata de um carrinho, não de tarefas, e não há operações CRUD.
- FastAPI, modelos Pydantic, serviços, repositórios e integração com PostgreSQL estão apenas representados no diagrama arquitetural.
- Não há testes, cobertura, configuração de ambiente, migrações ou containers.
- Não há documentação sobre autenticação, autorização ou filtros de busca.
- As ferramentas de IA utilizadas ainda não estão especificadas.

Próximos passos sugeridos:

1. Implementar a API de tarefas de acordo com o diagrama.
2. Definir configuração e execução local do PostgreSQL, incluindo migrações.
3. Adicionar testes unitários e de integração e configurar cobertura.
4. Documentar endpoints, variáveis de ambiente e decisões de segurança.
5. Evoluir a API e documentar os contratos dos endpoints.

## Contribuição

1. Faça um fork do repositório no GitHub.
2. Crie uma branch para sua alteração:

   ```bash
   git checkout -b feat/descricao-da-alteracao
   ```

3. Faça alterações pequenas e focadas, seguindo o estilo existente e mantendo as anotações de tipo.
4. Execute os testes disponíveis. Se adicionar testes, documente como executá-los.
5. Envie sua branch e abra um Pull Request descrevendo a motivação e as mudanças:

   ```bash
   git push origin feat/descricao-da-alteracao
   ```

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para
conhecer os termos completos.
