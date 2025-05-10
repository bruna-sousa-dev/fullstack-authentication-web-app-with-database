FROM python:3.11-slim

# Evita interações durante instalação de pacotes
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

# Instala dependências Python de uma vez
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copia todo o restante do app
COPY . .

# Torna o script de inicialização executável
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Documenta as portas necessárias
EXPOSE 5000 80 443

# Comando de inicialização
CMD ["/start.sh"]
