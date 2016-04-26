from httmock import response, urlmatch

GET = 'get'
HEADERS = {'content-type': 'application/json'}
NETLOC = r'(.*\.)?api\.cloudpassage\.com$'

class Resource:
    def __init__(self, path):
        self.path = path

    def get(self):
        with open(self.path, 'r') as f:
            content = f.read()
        return content

@urlmatch(netloc=NETLOC, method=GET)
def resource_get(url, request):
    file_path = url.netloc + url.path + '/result'
    try:
        content = Resource(file_path).get()
    except EnvironmentError:
        return response(404, {}, HEADERS, None, 5, request)
    return response(200, content, HEADERS, None, 5, request)
