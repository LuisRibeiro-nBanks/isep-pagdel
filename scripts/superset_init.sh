#!/bin/bash

# Install required database driver
pip install psycopg2-binary

# Inicializa o banco de dados do Superset (migrations)
superset db upgrade

# Cria o usuário admin (altera user/password/email se quiseres)
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password admin

# Carrega configurações iniciais (roles, permissões)
superset init

# (Opcional) Carrega exemplos de dashboards e dados
# superset load-examples

echo "Superset inicializado com sucesso!"
