# FitConnect - Plataforma de Rede Social Fitness

FitConnect é uma plataforma web que conecta alunos e educadores físicos, permitindo o compartilhamento e acompanhamento de treinos personalizados.

## Funcionalidades Principais

- Cadastro de usuários (alunos e educadores físicos)
- Anamnese completa para alunos
- Criação e compartilhamento de treinos
- Feed de atividades
- Sistema de conquistas
- Interações sociais (seguir, curtir, comentar)

## Tecnologias Utilizadas

- Backend: Django
- Frontend: HTML, TailwindCSS, DaisyUI
- Banco de Dados: PostgreSQL
- Autenticação: django-allauth

## Requisitos

- Python 3.8+
- PostgreSQL
- Node.js e npm (para TailwindCSS)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/fitconnect.git
cd fitconnect
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados PostgreSQL:
- Crie um banco de dados chamado `fitness_db`
- Configure as credenciais no arquivo `website/settings.py`

5. Execute as migrações:
```bash
cd website
python manage.py migrate
```

6. Instale e configure o TailwindCSS:
```bash
python manage.py tailwind install
python manage.py tailwind start
```

7. Popule o banco de dados com dados de exemplo:
```bash
python manage.py populate_db
```

8. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## Usuários de Teste

Após executar o comando `populate_db`, os seguintes usuários estarão disponíveis:

- Administrador:
  - Email: admin@example.com
  - Senha: admin123

- Educador Físico:
  - Email: educador@example.com
  - Senha: educador123

- Alunos:
  - Email: aluno0@example.com até aluno4@example.com
  - Senha: aluno123

## Estrutura do Projeto

```
website/
├── fitness/            # Aplicativo principal
│   ├── models.py      # Modelos de dados
│   ├── views.py       # Views e lógica
│   ├── forms.py       # Formulários
│   └── urls.py        # URLs do app
├── users/             # Aplicativo de usuários
│   ├── models.py      # Modelo de usuário
│   ├── views.py       # Views de autenticação
│   └── forms.py       # Formulários de usuário
├── templates/         # Templates HTML
│   ├── base.html     # Template base
│   ├── fitness/      # Templates do app fitness
│   └── users/        # Templates de usuário
└── static/           # Arquivos estáticos
    ├── css/          # Estilos
    └── img/          # Imagens
```

## Desenvolvimento

1. Para criar novas migrações:
```bash
python manage.py makemigrations
```

2. Para aplicar migrações:
```bash
python manage.py migrate
```

3. Para criar um superusuário:
```bash
python manage.py createsuperuser
```

4. Para compilar o TailwindCSS:
```bash
python manage.py tailwind build
```

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
