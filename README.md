# Raiz — Gerenciamento de Tarefas

Micro-API RESTful do **Raiz — Gerenciamento de Tarefas**, desenvolvida em Python
com FastAPI para criar, listar, atualizar e excluir tarefas. A aplicação utiliza
modelos Pydantic para validação, serviços para as regras de negócio e o Repository
Pattern para desacoplar a persistência da camada de aplicação.

> **Estado atual:** o CRUD funciona com repositórios em memória. PostgreSQL,
> SQLAlchemy e Docker fazem parte da arquitetura planejada, mas a persistência
> PostgreSQL ainda não foi conectada ao código.

## Índice

1. [Tecnologias](#tecnologias)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação e configuração](#instalação-e-configuração)
4. [Execução da API](#execução-da-api)
5. [Endpoints e exemplos](#endpoints-e-exemplos)
6. [Execução de testes](#execução-de-testes)
7. [Estrutura do projeto](#estrutura-do-projeto)
8. [Commits](#commits)
9. [Como a IA Acelerou Este Projeto](#como-a-ia-acelerou-este-projeto)
10. [Limitações e Próximos Passos](#limitações-e-próximos-passos)
11. [Licença](#licença)

## Tecnologias

- **Python 3.11** — linguagem-alvo do projeto. O código atual também mantém
  compatibilidade declarada com Python 3.9 ou superior.
- **FastAPI 0.115.0** — framework para a API RESTful.
- **Pydantic 2.10.0** — validação e serialização dos dados.
- **SQLAlchemy 2.0.36** — ORM previsto para a persistência relacional.
- **PostgreSQL** — banco de dados previsto para a versão persistente da API.
- **Docker** — tecnologia prevista para executar serviços, incluindo PostgreSQL.
- **Pytest 8.4.2** — testes automatizados.
- **Black 25.11.0** — formatação do código Python.
- **Uvicorn 0.32.0** — servidor ASGI.
- **GitHub Copilot** — auxílio à escrita e autocompletar código.
- **Cursor** — apoio a refatorações que envolvem múltiplos arquivos.
- **Claude 4.6 Sonnet** — apoio à geração e revisão dos testes unitários.

O driver PostgreSQL atualmente instalado no ambiente é `asyncpg 0.30.0`.
Embora Psycopg2 seja mencionado no escopo original, ele não está instalado no
ambiente atual e não é usado pela implementação presente.
A implementação atual usa armazenamento em memória; por isso, as dependências
SQLAlchemy, PostgreSQL e Docker ainda não participam do fluxo de execução do
CRUD.

## Pré-requisitos

Para executar a versão atual da API:

- Python 3.9 ou superior instalado;
- `pip` disponível;
- Git;
- acesso a um terminal;
- ambiente virtual recomendado.

Para a futura execução com PostgreSQL e Docker:

- Docker Engine e Docker Compose instalados;
- PostgreSQL 14 ou superior, caso o banco seja executado localmente sem Docker;
- uma porta disponível para a API, por padrão `8000`;
- uma porta disponível para o PostgreSQL, por padrão `5432`.

## Instalação e configuração

### Clonar o projeto

```bash
git clone https://github.com/adrianomandrade-png/Raiz-Gerenciamento_de_Tarefas.git
cd Raiz-Gerenciamento_de_Tarefas
```

### Configurar o ambiente virtual

O fluxo oficial desta versão usa `venv` e o `requirements.txt`, que contém as
versões exatas das dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
make install
make install-hooks
```

Depois de ativar o ambiente virtual, os comandos `make run`, `make test` e
`make format` usam o Python e os pacotes desse ambiente.

O `pyproject.toml` contém metadados e uma configuração opcional para Poetry,
mas o fluxo oficial desta release não depende de Poetry ou Pipenv.

### Configurar as variáveis de ambiente

A API exige uma chave no ambiente para proteger as rotas:

```bash
export API_KEY="substitua-por-uma-chave-secreta"
export APP_TITLE="Raiz — Gerenciamento de Tarefas"
export LOG_LEVEL="INFO"
```

Para carregar essas variáveis a partir de um arquivo local `.env`, crie o arquivo
na raiz do projeto:

```dotenv
API_KEY=substitua-por-uma-chave-secreta
APP_TITLE=Raiz — Gerenciamento de Tarefas
LOG_LEVEL=INFO
```

O código lê as variáveis com `os.getenv`. Portanto, carregue o arquivo no shell
antes de iniciar a API:

```bash
set -a
source .env
set +a
```

O arquivo `.env` não deve ser versionado. O `.gitignore` do projeto já o ignora.

### Configurar PostgreSQL com Docker

Ainda não existe um `docker-compose.yml` neste repositório. Quando a integração
com PostgreSQL for implementada, a configuração deverá incluir, no mínimo:

```dotenv
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/tarefas
```

Neste momento, `DATABASE_URL` é apenas uma configuração planejada e não é
consumida pela aplicação atual.

## Execução da API

Com as variáveis de ambiente carregadas, execute:

```bash
python -m uvicorn app.main:app --reload
```

Ou use o comando equivalente do Makefile:

```bash
make run
```

A API ficará disponível em `http://127.0.0.1:8000`.

Documentação interativa:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Todas as rotas de tarefas exigem o cabeçalho:

```http
X-API-Key: substitua-por-uma-chave-secreta
```

## Endpoints e exemplos

Defina a chave usada nos exemplos:

```bash
export API_KEY="substitua-por-uma-chave-secreta"
```

### Criar uma tarefa

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY}" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Revisar os endpoints da API",
    "status": false
  }'
```

Resposta esperada: `201 Created`, com o `id` UUID e o campo `created_at`
preenchidos pela API.

### Listar tarefas

```bash
curl -X GET "http://127.0.0.1:8000/tasks" \
  -H "X-API-Key: ${API_KEY}"
```

Para filtrar pelo status:

```bash
curl -X GET "http://127.0.0.1:8000/tasks?status=true" \
  -H "X-API-Key: ${API_KEY}"
```

### Buscar uma tarefa por UUID

Substitua `<TASK_ID>` pelo UUID retornado na criação:

```bash
curl -X GET "http://127.0.0.1:8000/tasks/<TASK_ID>" \
  -H "X-API-Key: ${API_KEY}"
```

### Atualizar uma tarefa

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/<TASK_ID>" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${API_KEY}" \
  -d '{
    "title": "Estudar FastAPI e Pydantic",
    "description": "Concluir a revisão da API",
    "status": true
  }'
```

### Excluir uma tarefa

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/<TASK_ID>" \
  -H "X-API-Key: ${API_KEY}"
```

A exclusão bem-sucedida retorna `204 No Content`. Um UUID inexistente retorna
`404 Not Found`.

## Execução de testes

Instale as dependências e execute a suíte com:

```bash
python -m pytest
```

Ou use:

```bash
make test
```

Os testes cobrem:

- criação de tarefas;
- listagem e filtro por status;
- atualização do status para `true`;
- exclusão;
- UUID inexistente ou inválido;
- autenticação por API key;
- limites de validação dos campos Pydantic.

Para formatar os arquivos Python com Black:

```bash
make format
```

## Commits

O projeto segue o padrão [Conventional Commits](https://www.conventionalcommits.org/).
Ative o hook local uma vez por clone:

```bash
make install-hooks
```

Depois disso, mensagens fora do padrão serão rejeitadas antes da criação do
commit. Exemplos válidos:

```text
feat: adicionar endpoint de tarefas
fix(api): corrigir validação de UUID
test: cobrir busca de tarefa inexistente
```

As mensagens também são verificadas automaticamente no GitHub Actions em pushes
e pull requests.

## Estrutura do projeto

```text
.
├── app/
│   ├── main.py           # Aplicação FastAPI, autenticação e endpoints
│   ├── repositories.py   # IRepository e repositórios concretos
│   ├── schemas.py        # Modelos Pydantic de entrada e saída
│   └── services.py       # Regras de negócio e injeção de repositórios
├── tests/
│   ├── conftest.py       # Fixtures e isolamento do repositório
│   ├── test_api.py       # Testes dos endpoints HTTP
│   └── test_schemas.py   # Testes de validação Pydantic
├── arquitetura.md        # Diagrama da arquitetura planejada
├── Makefile              # Comandos de instalação, execução, testes e formato
├── pyproject.toml        # Configuração básica para Poetry
├── requirements.txt      # Dependências com versões fixadas
├── shopping_cart.py      # Exemplo independente de função tipada
└── .gitignore
```

## Como a IA Acelerou Este Projeto

Ferramentas de inteligência artificial generativa foram utilizadas como apoio
ao desenvolvimento, sempre com revisão humana:

- **GitHub Copilot:** auxiliou o autocompletar, a criação de trechos repetitivos
  e a exploração inicial de soluções;
- **Cursor:** apoiou refatorações que envolviam vários arquivos, como a
  separação entre rotas, serviços e repositórios;
- **Claude 4.6 Sonnet:** auxiliou na geração e revisão dos testes unitários,
  incluindo cenários de caminho feliz e casos de borda.

Esse uso acelerou a implementação, a documentação, a criação de testes e a
identificação de inconsistências entre os arquivos do projeto. A revisão humana
foi essencial para validar requisitos, conferir compatibilidade das versões,
revisar segurança, corrigir sugestões inadequadas e confirmar os resultados
com execução de testes.

## Limitações e Próximos Passos

### Limitações atuais

- O armazenamento atual é em memória; os dados são perdidos quando a aplicação
  é reiniciada.
- Ainda não há integração efetiva com PostgreSQL, SQLAlchemy ou Docker.
- Há proteção simples por API key, mas não existe autenticação de usuários
  robusta com JWT/OAuth2.
- Não há autorização por usuário, papéis ou permissões: a API key não identifica
  um usuário nem restringe tarefas por proprietário.
- Os filtros disponíveis estão limitados ao campo booleano `status`.
- Não há filtros avançados por título, descrição, período de criação, ordenação
  ou paginação.
- Não há migrações de banco de dados nem `docker-compose.yml`.

### Próximos passos

1. Implementar repositórios PostgreSQL com SQLAlchemy e `asyncpg`.
2. Criar modelos persistentes, migrações e configuração segura de conexão.
3. Adicionar Dockerfile e Docker Compose para API e PostgreSQL.
4. Substituir a API key simples por autenticação de usuários com JWT ou OAuth2.
5. Implementar autorização por usuário, papéis e permissões.
6. Adicionar filtros avançados, ordenação e paginação.
7. Ampliar os testes com integração real ao PostgreSQL.
8. Configurar CI para executar testes, Black e verificações de qualidade.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE)
para conhecer os termos completos.
