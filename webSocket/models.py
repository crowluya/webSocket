import json

from utils import log


def save(data, path):
    '''
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    :param data:
    :param path:
    :return:
    '''
    s = json.dump(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    '''
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    :param path:
    :return:
    '''
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load ', s)
        return json.loads(s)


# Model 是存放存储数据的基类
class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        '''
        得到一个类的所有存储的实例
        :param cls:
        :return:
        '''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        '''
        save 方法保存一个Model 的实例
        :param self:
        :return:
        '''
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict 包含所有对象与属性与值的字段
        l = [m.__dict__ for m in models]
        path = self.dp_path()
        save(l, path)

    def __repr__(self):
        '''
        魔法方法
        :param self:
        :return:
        '''
        classname = self.__class__.__name__
        properties = ['{}:({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<{}\n{}>'.format(classname, s)


# 实际数据处理类
class User(Model):
    def new(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'xiao' and self.password =='123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


# class 保存 message
class Message(Model):
    def new(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')