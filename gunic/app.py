from urllib.parse import parse_qs

def application(environ, start_response):
    # Получение данных из GET-запроса
    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)

    # Получение данных из POST-запроса
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    post_body = environ['wsgi.input'].read(content_length)
    post_params = parse_qs(post_body)

    # Формирование ответа
    response_body = f"GET параметры: {get_params}\nPOST параметры: {post_params}"
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]
def application(environ, start_response):
    # Получение данных из GET-запроса
    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)

    # Получение данных из POST-запроса
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    post_body = environ['wsgi.input'].read(content_length)
    post_params = parse_qs(post_body)

    # Формирование ответа
    response_body = f"GET параметры: {get_params}\nPOST параметры: {post_params}"
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]
