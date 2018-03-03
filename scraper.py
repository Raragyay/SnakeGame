import requests


def establish_connection(url):
    useragent = {
        'name': 'raragbot',
        'email': 'mailto: raragbot@gmail.com'
    }
    website = requests.get(url + '/robots.txt', headers={
        'user-agent': 'python-requests/4.8.2(Compatible;{};{})'.format(useragent['name'], useragent['email'])
    })
    if website.status_code == 200:
        return requests.get(url)
    else:
        raise ConnectionError


url = 'http://www.reddit.com'
try:
    r = establish_connection(url)
    print(r.text)
except ConnectionError:
    print('Could not establish a connection to the server. ')
