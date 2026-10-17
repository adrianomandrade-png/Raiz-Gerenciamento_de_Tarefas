# Changelog

Todas as mudanças relevantes do **Raiz — Gerenciamento de Tarefas** são
registradas neste arquivo.

## [2.0.0] - Planejado

### Persistência e infraestrutura

- Implementar persistência real com PostgreSQL.
- Conectar os repositórios ao SQLAlchemy com suporte assíncrono via `asyncpg`.
- Criar modelos persistentes e migrações de banco de dados com Alembic.
- Adicionar `Dockerfile` para a API.
- Adicionar Docker Compose com os serviços da API e do PostgreSQL.
- Configurar healthcheck e conexão segura entre a API e o banco de dados.
- Adicionar testes de integração utilizando um banco PostgreSQL.

### Autenticação e autorização

- Substituir a API key simples por autenticação de usuários com JWT ou OAuth2.
- Implementar cadastro e autenticação de usuários.
- Adicionar autorização por usuário, papéis e permissões.
- Restringir o acesso às tarefas de acordo com o proprietário autenticado.
- Adicionar mecanismos de rotação e gerenciamento seguro de credenciais.

### Consultas e gerenciamento de tarefas

- Adicionar filtros avançados por título, descrição, status e período de
  criação.
- Implementar ordenação dos resultados.
- Implementar paginação para listagens.
- Ampliar os recursos de gerenciamento de usuários e tarefas persistentes.

### Qualidade e operação

- Ampliar a cobertura de testes unitários e de integração.
- Adicionar validações de qualidade e segurança de dependências ao CI.
- Evoluir o monitoramento com métricas e verificações mais completas de saúde
  da aplicação.

## [v1.0.0] - 2026-10-17

### Funcionalidades implementadas

- Adicionada API RESTful com FastAPI para gerenciamento de tarefas.
- Adicionado endpoint `GET /health` para verificar a disponibilidade da API.
- Adicionado endpoint `POST /tasks` para criação de tarefas.
- Adicionado endpoint `GET /tasks` para listagem de tarefas.
- Adicionado filtro opcional por status em `GET /tasks?status=true|false`.
- Adicionado endpoint `GET /tasks/{task_id}` para consulta por UUID.
- Adicionado endpoint `PUT /tasks/{task_id}` para atualização de tarefas.
- Adicionado endpoint `DELETE /tasks/{task_id}` para exclusão de tarefas.
- Adicionada autenticação por API key usando o cabeçalho `X-API-Key`.
- Adicionada comparação segura da API key com `secrets.compare_digest`.
- Adicionada configuração por variáveis de ambiente:
  `API_KEY`, `APP_TITLE` e `LOG_LEVEL`.
- Adicionado `.env.example` com valores de exemplo sem credenciais reais.
- Adicionada validação de entrada e saída com Pydantic.
- Adicionados limites de tamanho para títulos e descrições de tarefas.
- Adicionado identificador UUID e timestamp UTC para tarefas.
- Adicionado tratamento de erros para UUID inválido, tarefa inexistente e
  falhas de autenticação.
- Adicionado logging para eventos de autenticação e tarefas não encontradas.
- Adicionada arquitetura em camadas com Controller, Service e Repository
  Pattern.
- Adicionada injeção de dependências para repositórios e serviços.
- Adicionadas interfaces de repositório para desacoplar as regras de negócio
  da persistência.
- Adicionados repositórios assíncronos em memória para tarefas e usuários.

### Qualidade e testes

- Adicionados testes automatizados com Pytest para os endpoints da API.
- Adicionados testes de validação dos modelos Pydantic.
- Cobertos cenários de sucesso, autenticação, filtros, UUIDs inválidos,
  recursos inexistentes e limites de campos.
- Configurado Black para padronização da formatação do código.
- Configurado GitHub Actions para executar os testes e verificar o Black em
  Python 3.9 e 3.11.
- Adicionada validação de mensagens no padrão Conventional Commits.
- Adicionado hook local para rejeitar mensagens de commit fora do padrão.

### Documentação e desenvolvimento

- Adicionado README com descrição, tecnologias, pré-requisitos, instalação,
  configuração, exemplos `curl`, testes, estrutura e limitações.
- Adicionado diagrama Mermaid da arquitetura planejada.
- Adicionado Makefile com comandos para instalação, execução, testes,
  formatação e instalação do hook de commits.
- Adicionado `requirements.txt` com versões fixadas das dependências.
- Declarada a versão do projeto como `1.0.0` no `pyproject.toml`.
- Publicada a tag Git `v1.0.0`.

### Limitações conhecidas da versão

- A persistência atual é em memória e os dados são perdidos ao reiniciar a
  aplicação.
- PostgreSQL, SQLAlchemy e Docker ainda não estão conectados ao fluxo de
  execução da API.
- A autenticação disponível é somente por API key; não há JWT, OAuth2 ou
  autorização por usuário.
- Não há filtros avançados, ordenação ou paginação.
