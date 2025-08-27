# 🚫 Sistema de Rate Limiting - Crypto Trading Analyzer

## 📋 Visão Geral

O sistema implementa um **rate limiting baseado em IP** que permite apenas **1 solicitação por IP a cada 1 hora**, garantindo uso justo e prevenindo abuso da aplicação.

## 🔒 Características de Segurança

### ✅ **Resistente à Manipulação**
- **Timestamp do servidor**: Usa `Date.now()` do servidor, não do cliente
- **Impossível burlar**: Usuários não podem alterar data/hora do computador para contornar o limite
- **IP real**: Detecta IP real através de múltiplos headers (Cloudflare, Netlify, etc.)

### 🕐 **Controle de Tempo**
- **Período**: 1 hora (3.600.000 milissegundos)
- **Contagem**: 1 solicitação por IP por período
- **Reset automático**: Após 1 hora, o IP pode fazer nova solicitação

## 🏗️ **Arquitetura Técnica**

### **Armazenamento em Memória**
```javascript
const rateLimitStore = new Map(); // IP -> { lastRequest: timestamp, count: number }
```

### **Detecção de IP**
```javascript
function getClientIP(event) {
  const headers = event.headers || {};
  
  // Múltiplos headers para diferentes provedores
  const ip = headers['x-forwarded-for'] || 
             headers['x-real-ip'] || 
             headers['cf-connecting-ip'] || 
             headers['x-client-ip'] ||
             'unknown';
  
  return ip.split(',')[0].trim();
}
```

### **Verificação de Rate Limit**
```javascript
function checkRateLimit(ip) {
  const now = Date.now(); // Timestamp do servidor
  const oneHour = 60 * 60 * 1000; // 1 hora em ms
  
  if (!rateLimitStore.has(ip)) {
    // Primeira solicitação
    rateLimitStore.set(ip, { lastRequest: now, count: 1 });
    return { allowed: true, remainingTime: 0 };
  }
  
  const record = rateLimitStore.get(ip);
  const timeSinceLastRequest = now - record.lastRequest;
  
  if (timeSinceLastRequest < oneHour) {
    // Ainda dentro do período
    const remainingTime = Math.ceil((oneHour - timeSinceLastRequest) / 1000 / 60);
    return { 
      allowed: false, 
      remainingTime,
      message: `Rate limit exceeded. Try again in ${remainingTime} minutes.`
    };
  } else {
    // Passou 1 hora, resetar
    rateLimitStore.set(ip, { lastRequest: now, count: 1 });
    return { allowed: true, remainingTime: 0 };
  }
}
```

## 🧹 **Manutenção Automática**

### **Limpeza de IPs Antigos**
```javascript
function cleanupOldIPs() {
  const now = Date.now();
  const oneDay = 24 * 60 * 60 * 1000; // 1 dia
  
  for (const [ip, record] of rateLimitStore.entries()) {
    if (now - record.lastRequest > oneDay) {
      rateLimitStore.delete(ip);
    }
  }
}
```

### **Execução Automática**
- **Frequência**: A cada 100 solicitações
- **Objetivo**: Evitar acúmulo infinito de IPs na memória
- **Critério**: Remove IPs que não fizeram solicitação há mais de 1 dia

## 📱 **Interface do Usuário**

### **Mensagem de Rate Limit**
```
⏰ Rate Limit Exceeded
Rate limit exceeded. Try again in 45 minutes.

💡 This limit prevents abuse and ensures fair usage for all users.
```

### **Informações de Rate Limit (Sucesso)**
```
⏰ Rate Limit Info
Next request allowed: 12/23/2025, 3:45:30 PM
Limit: 1 request per hour per IP address
```

## 🚨 **Respostas HTTP**

### **Rate Limit Exceeded (429)**
```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "message": "Rate limit exceeded. Try again in 45 minutes.",
  "remainingTime": 45,
  "timestamp": "2025-12-23T14:45:30.123Z"
}
```

### **Sucesso (200)**
```json
{
  "success": true,
  "results": [...],
  "rate_limit_info": {
    "ip": "192.168.1.100",
    "next_request_allowed": "2025-12-23T15:45:30.123Z"
  }
}
```

## 🛡️ **Benefícios de Segurança**

1. **Prevenção de Abuso**: Evita spam de solicitações
2. **Uso Justo**: Garante que todos os usuários tenham acesso igual
3. **Proteção de Recursos**: Preserva performance da aplicação
4. **Auditoria**: Rastreia IPs e horários de solicitações
5. **Resistência**: Impossível contornar através de manipulação de data/hora

## 🔧 **Configuração**

### **Período de Rate Limit**
```javascript
const oneHour = 60 * 60 * 1000; // 1 hora (modificável)
```

### **Frequência de Limpeza**
```javascript
if (requestCount % 100 === 0) { // A cada 100 solicitações
  cleanupOldIPs();
}
```

### **Período de Limpeza**
```javascript
const oneDay = 24 * 60 * 60 * 1000; // 1 dia (modificável)
```

## 📊 **Monitoramento**

### **Logs de Sistema**
```
🔍 Request from IP: 192.168.1.100
✅ Rate limit check passed, starting cryptocurrency analysis...
🚫 Rate limit exceeded for IP 192.168.1.100: Rate limit exceeded. Try again in 45 minutes.
🧹 Cleaned up old IPs. Current store size: 15
```

### **Métricas Disponíveis**
- **IPs ativos**: Número de IPs únicos no período
- **Tentativas bloqueadas**: Solicitações rejeitadas por rate limit
- **Tempo médio**: Tempo entre solicitações do mesmo IP

## 🚀 **Deploy e Manutenção**

### **Netlify Functions**
- **Memória**: Rate limit store é mantido em memória da função
- **Cold Start**: Store é resetado em cold starts (normalmente a cada 10 minutos de inatividade)
- **Escalabilidade**: Cada instância da função mantém seu próprio store

### **Considerações de Produção**
- **Persistência**: Para produção em larga escala, considerar Redis ou banco de dados
- **Distribuição**: Rate limiting distribuído para múltiplas instâncias
- **Monitoramento**: Alertas para IPs com muitas tentativas bloqueadas

---

**🎯 Objetivo**: Sistema robusto e justo que previne abuso enquanto mantém boa experiência do usuário.
