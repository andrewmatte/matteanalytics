from datetime import datetime
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse
from starlette.routing import Route
from starlette.responses import Response
from starlette.templating import Jinja2Templates


from transforms import events
from transforms import signups
from helpers import sessions
from db import models
from db import queries


script = open('location.js').read()
CORS_headers = {'Access-Control-Allow-Origin': '*'}
templates = Jinja2Templates(directory='views')


async def hello_analytics(request):
    return JSONResponse({'hello': 'analytics'})


async def save_event(request):
    try:
        data = await request.json()
    except Exception as e:
        print(e)
        return JSONResponse({'error': 'missing json'})
    
    try:
        event = events.accept(data, request.headers)
    except Exception as e:
        print(e)
        return JSONResponse({}, 400, CORS_headers)

    # save
    try:
        models.execute(queries.save_event, (
            event['hashed_ip'],
            event['event'],
            event['referrer'],
        ))
    except Exception as e:
        print(e)
    
    f = open('analytics_dump.csv', 'a')
    f.write(event['hashed_ip'] + ',' + str(event['event']) + ',' + str(datetime.utcnow()) + ',' + event['referrer'] + '\n')
    f.close()

    return JSONResponse({}, 200, CORS_headers)


async def get_script(request):
    return Response(script, 200, CORS_headers, 'application/javascript')


async def data_dump(request):
    f = open('analytics_dump.csv', 'r').read()
    return Response(f)


async def splash(request):
    return templates.TemplateResponse('index.html', {'request': request})


async def create_signup(request):
    try:
        data = await request.form()
    except Exception as e:
        print(e)
        return JSONResponse({'error': 'missing form'})

    signup = signups.accept(data)

    try:
        new_user = models.execute(queries.create_signup, (
            signup['email'],
            signup['salt'],
            signup['passwd'],
        ))
    except:
        new_user = []
    
    if len(new_user) == 0:
        return RedirectResponse('/')
    
    new_session = sessions.create_session(new_user[0])

    return templates.TemplateResponse('dashboard', {'request': request})


app = Starlette(debug=True, routes=[
    Route('/', hello_analytics),
    Route('/save_event', save_event, methods=["POST"]),
    Route('/script', get_script),
    Route('/data_dump', data_dump),
    Route('/splash', splash),
    Route('/signup', create_signup, methods=["POST"])
])