# 🚀 Deploy na Netlify - Crypto Trading Analyzer

## 📋 Pré-requisitos
- Conta na [Netlify](https://netlify.com)
- Projeto conectado ao GitHub/GitLab/Bitbucket

## 🔧 Configuração

### 1. Estrutura do Projeto
O projeto foi configurado para funcionar como um site estático na Netlify:

```
CryptoPulse/
├── index.html          # Página principal (na raiz)
├── static/             # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── netlify.toml        # Configuração da Netlify
└── NETLIFY_DEPLOY.md   # Este arquivo
```

### 2. Configuração da Netlify
O arquivo `netlify.toml` está configurado para:
- Publicar a pasta raiz (`.`)
- Configurar redirecionamentos para SPA
- Definir versão do Node.js

## 🚀 Deploy

### Opção 1: Deploy via Git (Recomendado)
1. Conecte seu repositório na Netlify
2. Configure as opções de build:
   - **Build command**: `echo 'Build completed'`
   - **Publish directory**: `.` (ponto - pasta raiz)
3. Clique em "Deploy site"

### Opção 2: Deploy Manual
1. Faça upload da pasta raiz do projeto
2. A Netlify detectará automaticamente a configuração

## ⚠️ Importante

**Este é um site estático de demonstração!**

- ✅ Funciona perfeitamente na Netlify
- ✅ Interface completa com CSS e JavaScript
- ✅ Dados simulados para demonstração
- ❌ Não possui backend Python/Flask
- ❌ Não faz análises reais de criptomoedas

## 🔄 Para Versão Completa com Backend

Se quiser a versão completa com análise real:
1. Use plataformas que suportam Python (Heroku, Railway, Render)
2. Mantenha os arquivos `app.py`, `requirements.txt`, etc.
3. Configure variáveis de ambiente para APIs

## 🎯 Funcionalidades da Versão Estática

- ✅ Interface responsiva e moderna
- ✅ Animações e efeitos visuais
- ✅ Dados simulados realistas
- ✅ Demonstração completa da funcionalidade
- ✅ Compatível com todos os navegadores

## 📱 Teste

Após o deploy:
1. Acesse o site da Netlify
2. Clique em "Search for Trade"
3. Veja os resultados simulados
4. Teste a responsividade em diferentes dispositivos

## 🆘 Suporte

Se houver problemas:
1. Verifique se todos os arquivos estão na pasta raiz
2. Confirme se o `netlify.toml` está correto
3. Verifique os logs de build na Netlify
4. Teste localmente abrindo o `index.html` no navegador
