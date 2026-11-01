# Kivun Tech

Site institucional da Kivun Tech, desenvolvido com Django.

## Desenvolvimento local

No PowerShell, na pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = 'True'
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. O arquivo `.env.example` é apenas uma referência: o projeto não carrega arquivos `.env` automaticamente. Em desenvolvimento, o envio de e-mail usa o backend de console, a menos que SMTP seja configurado explicitamente no ambiente.

## Publicação na Vercel

Conecte o repositório GitHub à Vercel. O endereço HTTPS `*.vercel.app` fornecido pelo projeto pode ser usado inicialmente, sem domínio próprio. Cadastre as configurações de produção em **Project Settings → Environment Variables**, nunca no código ou em arquivos versionados.

Configure `DJANGO_DEBUG=False`, uma `DJANGO_SECRET_KEY` forte e aleatória, `DJANGO_ALLOWED_HOSTS` com o host atribuído ao projeto e `DJANGO_CSRF_TRUSTED_ORIGINS` com a origem HTTPS correspondente. Para habilitar o formulário, cadastre também as variáveis SMTP indicadas em `.env.example`, incluindo a senha de app do provedor como segredo. Gere um novo deploy após alterar variáveis.

A Vercel detecta projetos Django pelo `manage.py` e coleta os arquivos configurados em `STATIC_ROOT`. Confirme no deploy que o formulário, HTTPS, páginas e arquivos estáticos estão funcionando.

## Conteúdo do repositório

O repositório contém apenas os arquivos necessários para executar e servir o site, além deste guia e do exemplo de configuração. O `.gitignore` exclui o banco de dados local, ambientes virtuais, segredos, capturas de tela, currículo, documentação interna e materiais de referência.

Os dados profissionais e canais de contato que aparecem nas páginas são conteúdo intencionalmente público do próprio site. Antes de publicar, confirme que esses dados e os logos exibidos têm aprovação para divulgação. Nunca inclua senhas, chaves, dados de clientes ou cópias privadas de documentos no repositório.
