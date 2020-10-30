from datetime import datetime
import hashlib
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.responses import Response


script = open('location.js').read()
CORS_headers = {'Access-Control-Allow-Origin': '*'}


async def homepage(request):
    return JSONResponse({'hello': 'analytics'})


async def save_event(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return JSONResponse({'error': 'missing json'})
    event = data.get('event')
    if not event:
        return JSONResponse({'error': 'missing event key'})
    host = request['client'][0]
    h = hashlib.new('md5')
    h.update(bytes(host, 'utf8'))
    hashed_ip = h.hexdigest()
    f = open('analytics_dump.csv', 'a')
    f.write(hashed_ip + ',' + str(event) + ',' + str(datetime.utcnow()) + '\n')
    f.close()
    return JSONResponse({'thanks': 'a lot'}, 200, CORS_headers)


async def get_script(request):
    return Response(script, 200, CORS_headers, 'application/javascript')


async def data_dump(request):
    f = open('analytics_dump.csv', 'r').read()
    return Response(f)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/save_event', save_event, methods=["POST"]),
    Route('/script', get_script),
    Route('/data_dump', data_dump),
])
