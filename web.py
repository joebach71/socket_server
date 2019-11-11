
# import aiohttp
# class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
#   async def handle_request(self, message, payload):
#       response = aiohttp.Response(
#           self.writer, 200, http_version=message.version
#       )
#       response.add_header('Content-Type', 'application/json')
#       response.add_header('Content-Length', '18')
#       response.send_headers()
#       response.write(b'<h1>It Works!</h1>')
#       await response.write_eof()
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     f = loop.create_server(
#         lambda: HttpRequestHandler(debug=True, keep_alive=75),
#         '0.0.0.0', '8000')
#     srv = loop.run_until_complete(f)
#     print('serving on', srv.sockets[0].getsockname())
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass

import sqlite3
import sys, os, json
from flask import g, Flask

app = Flask(__name__)

def get_db(db_name=None):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    cur = get_db().cursor()
    rows = cur.fetchall()
    print (rows)
    return json.dumps(rows, ensure_ascii=True)
    # return 'Hello, World!'

if __name__ == '__main__':
    DATABASE = sys.argv[1]
    # app = create_app(DATABASE)
    with app.app_context():
        get_db(DATABASE)
    app.run(port=sys.argv[2])