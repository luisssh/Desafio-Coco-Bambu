# Desafio Coco Bambu – CRUD de Usuários

## Descrição do Projeto
Esta aplicação é um **CRUD de usuários** com autenticação OAuth2 (via JWT), permitindo cadastro de usuários (somente superusuários), listagem de usuários (somente superusuários), login de usuários e visualização de dados do próprio usuário. A aplicação foi desenvolvida com **Python + Flask + SQLite** no backend e **HTML, CSS e JavaScript puro** no frontend. O objetivo é demonstrar a capacidade de criar uma **API REST** segura e consumi-la em um client web funcional.

---

## Funcionalidades
O sistema permite cadastrar usuários (somente superusuário), realizar login com autenticação JWT, listar usuários (somente superusuário), visualizar o perfil do usuário logado, editar e excluir usuários (restrito a superusuários) e realizar logout.

---

## Pré-requisitos
Para rodar o projeto é necessário ter Python 3.x instalado, junto com pip, e um navegador moderno como Chrome, Edge ou Firefox. O projeto utiliza SQLite, que já vem configurado e não precisa de instalação adicional.

---

## Instalação e Execução
Para começar, clone o repositório usando o comando `git clone https://github.com/luisssh/Desafio-Coco-Bambu.git` e entre na pasta do projeto com `cd Desafio-Coco-Bambu`. Em seguida, crie e ative um ambiente virtual com `python -m venv venv`. No Windows CMD use `venv\Scripts\activate` e no PowerShell `.\venv\Scripts\Activate.ps1`. Com o ambiente virtual ativo, instale as dependências usando `pip install -r requirements.txt`. As principais dependências são: flask, flask-cors, werkzeug e pyjwt.

O banco de dados SQLite será criado automaticamente ao rodar o backend, mas você pode inicializá-lo manualmente executando `python -c "from app.models import init_db; init_db()"`. Para iniciar o backend, execute `python -m app`; a API estará disponível em `http://127.0.0.1:5000`. Para acessar o frontend, abra o arquivo `index.html` no navegador, que fará as requisições para o backend automaticamente.

---

## Testes
Os endpoints da API podem ser testados manualmente. Para login utilize `POST /login`, para visualizar o perfil do usuário `GET /profile`, para listar usuários `GET /users` (somente superusuário), para criar usuários `POST /users` (somente superusuário), para editar `PUT /users/<id>` (somente superusuário) e para excluir `DELETE /users/<id>` (somente superusuário). É possível testar via frontend.

---

## Observações / Diferenciais
O projeto implementa autenticação via JWT/OAuth2, controle de acesso baseado no tipo de usuário, frontend funcional e responsivo, e código organizado em MVC simples (models, routes, auth). O banco SQLite já vem com tabela de blacklist de tokens e há possibilidade de extensões futuras, como Docker, login social e testes unitários.

---

## Autor
**Nome:** Luís Henrique  
**E-mail:** lhlds78@gmail.com  
**Projeto:** Desafio Coco Bambu  
**Repositório GitHub:** [https://github.com/luisssh/Desafio-Coco-Bambu]
