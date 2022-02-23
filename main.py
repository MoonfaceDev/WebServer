import json
from pathlib import Path

from http_utils.headers import Headers
from http_utils.requests.request import Request
from http_utils.responses.response import Response
from server import Server

server = Server()


@server.post('/create_penguin.php')
def post_login(request: Request):
    login_data = request.body.decode()
    print(login_data)
    return Response(
        body=json.dumps({
            'error_id': 49,
            'message': "Invalid validation of validity.",
            'success': False,
        }).encode(),
        headers=Headers({
            "content-type": "application/json",
        })
    )


server.serve_directory(Path(r'C:\My Web Sites'), Path(r'C:\My Web Sites\index.html'))


def main():
    server.run(port=8080)


if __name__ == '__main__':
    main()
