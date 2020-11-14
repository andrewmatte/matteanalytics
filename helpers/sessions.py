from db import models
from db import queries
from uuid import uuid4


def create_session(user):
    user_id = user.get('id')
    session_token = str(uuid4())
    session = models.execute(queries.create_session, (user_id, session_token,))
    return session[0]