#!/bin/bash

# TODO: parameters
# Run time folder
# Repo folders

# check and delete content in the runtime folder
[ -d /opt/lost-n-found ] && find /opt/lost-n-found -mindepth 1 ! -name 'uwsgi.ini' -exec rm -rf {} +
find /opt/lost-n-found -mindepth 1 ! -name 'uwsgi.ini' -exec rm -rf {} +

cp ~/se-lost-and-found/src/Lost_n_Found/manage.py /opt/lost-n-found/
cp ~/se-lost-and-found/src/Lost_n_Found/requirements.txt /opt/lost-n-found/

cp -r ~/se-lost-and-found/src/Lost_n_Found/app /opt/lost-n-found/
cp -r ~/se-lost-and-found/src/Lost_n_Found/Lost_n_Found /opt/lost-n-found/

cp ~/se-lost-and-found/src/Lost_n_Found/db.sqlite3 /opt/lost-n-found/

