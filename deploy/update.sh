#!/bin/bash

set -e

RUNTIME_DIR="/opt/lost-n-found"
CURRENT_USER="${SUDO_USER:-$(whoami)}"
USER_HOME="$(eval echo "~$CURRENT_USER")"
REPO_DIR="$USER_HOME/se-lost-and-found/src/Lost_n_Found"

systemctl stop lost-n-found

find "$RUNTIME_DIR" -mindepth 1 -maxdepth 1 ! -name 'uwsgi.ini' -exec rm -rf {} +

cp "$REPO_DIR/manage.py" "$RUNTIME_DIR/"
cp "$REPO_DIR/unix_requirements.txt" "$RUNTIME_DIR/"
cp -r "$REPO_DIR/app" "$RUNTIME_DIR/"
cp -r "$REPO_DIR/Lost_n_Found" "$RUNTIME_DIR/"
cp "$REPO_DIR/db.sqlite3" "$RUNTIME_DIR/"

chown -R "$CURRENT_USER:$CURRENT_USER" "$RUNTIME_DIR"

cd "$RUNTIME_DIR"

python3 -m venv env
source env/bin/activate

python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools wheel

python -m pip install -r unix_requirements.txt
python -m pip install uwsgi

python manage.py migrate
python manage.py collectstatic --noinput

deactivate

chown -R "$CURRENT_USER:$CURRENT_USER" "$RUNTIME_DIR"

systemctl start lost-n-found

echo "Deployment update completed successfully."

