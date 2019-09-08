import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


# 定义一个class 保存请求
class Request(object):
    def __init__(self):
        self.method = "GET"
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        log('args', args)
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def error(request, code=404):
    '''
    根据 code 返回 不同的错误响应
    :param request:
    :param code:
    :return:
    '''
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    # r.update 是什么意思
    r.update(route_dict)
    # 这里返回的error值 哪里来的值
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    '''
    启动服务器
    :param host:
    :param port:
    :return:
    '''
    log('start at ', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无线循环处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, request))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置request的method
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            # body 放入request里面
            response = response_for_path(path)
            # 把响应发送给客户段
            connection.sendall(response)
            connection.close()


if __name__ == "__main__":
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
