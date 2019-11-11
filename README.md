# Socket Server similar to memcached
## Installation
clone the repo
git clone https://github.com/joebach71/socket_server.git

cd socket_server

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cd frontend

npm install

You can run client.py to populate data

python client.py