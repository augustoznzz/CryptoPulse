#!/bin/bash

echo "🚀 Iniciando build para Netlify..."

# Verificar se os arquivos necessários existem
if [ ! -f "index.html" ]; then
    echo "❌ Erro: index.html não encontrado na raiz"
    exit 1
fi

if [ ! -d "static" ]; then
    echo "❌ Erro: pasta static não encontrada"
    exit 1
fi

if [ ! -f "static/css/style.css" ]; then
    echo "❌ Erro: style.css não encontrado"
    exit 1
fi

if [ ! -f "static/js/script.js" ]; then
    echo "❌ Erro: script.js não encontrado"
    exit 1
fi

echo "✅ Todos os arquivos estáticos encontrados"
echo "✅ Build concluído com sucesso!"
echo "🌐 Site estático pronto para deploy na Netlify"
