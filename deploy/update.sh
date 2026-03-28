#!/bin/bash

set -e

RUNTIME_DIR="/opt/lost-n-found"
CURRENT_USER="${SUDO_USER:-$(whoami)}"
USER_HOME="$(eval echo "~$CURRENT_USER")"
REPO_DIR="$USER_HOME/se-lost-and-found/src/Lost_n_Found"
APP_BUILD=$(git rev-parse --short HEAD)
SECRETS_FILE="$RUNTIME_DIR/Lost_n_Found/secrets.py"

if [ ! -f "$SECRETS_FILE" ]; then
    echo "ERROR: Missing secrets file: $SECRETS_FILE"
    exit 1
fi

systemctl stop lost-n-found

find "$RUNTIME_DIR" -mindepth 1 -maxdepth 1 ! -name 'uwsgi.ini' ! -name 'Lost_n_Found' -exec rm -rf {} +

cp "$REPO_DIR/manage.py" "$RUNTIME_DIR/"
cp "$REPO_DIR/unix_requirements.txt" "$RUNTIME_DIR/"
cp -r "$REPO_DIR/app" "$RUNTIME_DIR/"
cp "$REPO_DIR/Lost_n_Found/settings.py" "$RUNTIME_DIR/Lost_n_Found/"
cp "$REPO_DIR/Lost_n_Found/urls.py" "$RUNTIME_DIR/Lost_n_Found/"
cp "$REPO_DIR/Lost_n_Found/wsgi.py" "$RUNTIME_DIR/Lost_n_Found/"

cp "$REPO_DIR/db.sqlite3" "$RUNTIME_DIR/"

cp "$USER_HOME/secrets/secrets.py" "$RUNTIME_DIR/Lost_n_Found/secrets.py"


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

sudo sed -i "s/^Environment=\"APP_BUILD=.*\"$/Environment=\"APP_BUILD=${APP_BUILD}\"/" /etc/systemd/system/lost-n-found.service
sudo systemctl daemon-reload

systemctl start lost-n-found

echo "Deployment update completed successfully."
