#!/usr/bin/env python3
"""
Script de Inicialização do CryptoPulse
Permite escolher qual versão da aplicação usar
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Imprime o banner do CryptoPulse"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 CryptoRocket                            ║
    ║              Análise de Criptomoedas                         ║
    ║                                                              ║
    ║  Analisando as Top 30 Criptomoedas por Market Cap           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def show_menu():
    """Mostra o menu de opções"""
    print("\n📊 Escolha a versão da aplicação:")
    print("1. 🚀 Versão Rápida (Recomendada) - Cache + Resposta Rápida")
    print("2. ⚡ Versão Completa - Análise em Tempo Real")
    print("3. 🧪 Versão de Teste - Dados Simulados")
    print("4. 📋 Comando Direto - Top 30 Criptomoedas")
    print("5. ❌ Sair")
    
    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Opção inválida. Digite 1, 2, 3, 4 ou 5.")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            sys.exit(0)

def start_server(version):
    """Inicia o servidor baseado na versão escolhida"""
    if version == '1':
        print("\n🚀 Iniciando versão rápida...")
        print("📊 Cache ativo para resposta rápida")
        print("🌐 Acesse: http://localhost:5000")
        subprocess.run([sys.executable, "app_fast.py"])
        
    elif version == '2':
        print("\n⚡ Iniciando versão completa...")
        print("📊 Análise em tempo real das top 30 criptomoedas")
        print("⏱️  A primeira análise pode demorar alguns minutos...")
        print("🌐 Acesse: http://localhost:5000")
        subprocess.run([sys.executable, "app.py"])
        
    elif version == '3':
        print("\n🧪 Iniciando versão de teste...")
        print("📊 Dados simulados para teste rápido")
        print("🌐 Acesse: http://localhost:5000")
        subprocess.run([sys.executable, "app_simple.py"])
        
    elif version == '4':
        print("\n📋 Executando análise direta das top 30 criptomoedas...")
        subprocess.run([sys.executable, "main.py", "--top30", "--verbose"])

def main():
    """Função principal"""
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == '5':
            print("\n👋 Até logo!")
            break
        else:
            try:
                start_server(choice)
            except KeyboardInterrupt:
                print("\n\n⏹️  Servidor interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"\n❌ Erro ao iniciar servidor: {str(e)}")
                print("🔧 Verifique se todas as dependências estão instaladas:")
                print("   pip install -r requirements.txt")
            
            print("\n" + "="*60)
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main() 