import hashlib


def accept(data, headers):
    # event
    event = data.get('event')
    if not event:
        raise Exception('No event in data')

    # host
    host = headers.get('x-real-ip')
    h = hashlib.new('md5')
    h.update(bytes(host, 'utf8'))
    hashed_ip = h.hexdigest()

    # referrer
    referrer = str(data.get('referrer'))
    return {
        'event': event,
        'hashed_ip': hashed_ip,
        'referrer': referrer,
    }
