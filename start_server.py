#!/usr/bin/env python3
"""
Script de Inicialização do CryptoRocket - Versão Simplificada
Aplicação funciona via Netlify Functions
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Imprime o banner do CryptoRocket"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 CryptoRocket                           ║
    ║                   Análise de Criptomoedas                    ║
    ║                                                              ║
    ║     Analisando as 16 Criptomoedas Selecionadas               ║
    ║     Indicadores: price_change_24h, volume_24h, market_cap    ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def show_menu():
    """Mostra o menu de opções simplificado"""
    print("\n📊 Escolha uma opção:")
    print("1. 🌐 Abrir interface web (index.html)")
    print("2. 🔧 Abrir interface alternativa (crypto-analyzer.html)")
    print("3. 📁 Abrir pasta do projeto")
    print("4. ❌ Sair")
    
    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("❌ Opção inválida. Digite 1, 2, 3 ou 4.")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            sys.exit(0)

def execute_choice(choice):
    """Executa a opção escolhida"""
    if choice == '1':
        print("\n🌐 Abrindo interface principal...")
        print("📊 Aplicação funciona via Netlify Functions")
        print("🚀 Abrindo index.html no navegador...")
        
        # Tentar abrir no navegador padrão
        try:
            if sys.platform.startswith('win'):
                os.startfile('index.html')
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', 'index.html'])
            else:
                subprocess.run(['xdg-open', 'index.html'])
        except Exception as e:
            print(f"⚠️  Erro ao abrir navegador: {e}")
            print("📁 Abra manualmente o arquivo index.html")
            
    elif choice == '2':
        print("\n🔧 Abrindo interface alternativa...")
        print("📊 Interface crypto-analyzer.html")
        
        try:
            if sys.platform.startswith('win'):
                os.startfile('crypto-analyzer.html')
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', 'crypto-analyzer.html'])
            else:
                subprocess.run(['xdg-open', 'crypto-analyzer.html'])
        except Exception as e:
            print(f"⚠️  Erro ao abrir navegador: {e}")
            print("📁 Abra manualmente o arquivo crypto-analyzer.html")
            
    elif choice == '3':
        print("\n📁 Abrindo pasta do projeto...")
        try:
            if sys.platform.startswith('win'):
                os.startfile('.')
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', '.'])
            else:
                subprocess.run(['xdg-open', '.'])
        except Exception as e:
            print(f"⚠️  Erro ao abrir pasta: {e}")

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == '4':
            print("\n👋 Até logo!")
            break
        else:
            try:
                execute_choice(choice)
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")
            
            print("\n" + "="*60)
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main() 