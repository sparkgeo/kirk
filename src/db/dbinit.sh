#!/bin/bash

# This option causes the script to exit immediatly if
# an error is encountered.
set -o errexit

readonly REQUIRED_ENV_VARS=(
  "DB_USER"
  "DB_PASSWORD"
  "DB_NAME")


# Verify the environment vars are set.
verify_env_vars() {
  for evar in ${REQUIRED_ENV_VARS[@]}; do
    if [[ -z "${!evar}" ]]; then
      echo "Err: The env var '$evar' must be set."
      exit 1
    fi
  done
}


# Initalize
init_rdbms() {
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
     CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
     CREATE DATABASE $DB_NAME;
EOSQL
}

main() {
  verify_env_vars
  init_rdbms
}

main "$@"
