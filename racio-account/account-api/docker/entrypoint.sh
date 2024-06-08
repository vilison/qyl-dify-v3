
#!/bin/bash

set -e

if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Running migrations"
  flask db upgrade
fi

pip install --prefix=/pkg -r requirements.txt

if [[ "${DEBUG}" == "true" ]]; then
  flask run --host=${ACCOUNT_BIND_ADDRESS:-0.0.0.0} --port=${ACCOUNT_PORT:-5003} --debug
else
  gunicorn \
    --bind "${ACCOUNT_BIND_ADDRESS:-0.0.0.0}:${ACCOUNT_PORT:-5003}" \
    --workers ${SERVER_WORKER_AMOUNT:-1} \
    --worker-class ${SERVER_WORKER_CLASS:-gevent} \
    --timeout ${GUNICORN_TIMEOUT:-200} \
    --preload \
    app:app
fi