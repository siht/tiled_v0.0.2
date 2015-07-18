# -*- coding: cp1252 -*-
# fechad de inicio ?? Enero 2014
# fecha de lanzamiento 23 enero 2014
## author: José Carlos Tzompantzi de Jesús
## license: LGPL v3
## si no recibiste copia de la licencia ir a http://www.gnu.org/licenses/lgpl.html
## queda a disposición de quien quiera ocuparla y modificarla
## no hay garantía de que funcione, ni me hago responsable del uso potencial
## de este código
MATHS = '__add__', '__and__', '__div__', '__floordiv__', '__invert__', '__lshift__', '__mod__', '__mul__', '__neg__', '__or__', '__radd__', '__rand__', '__rdiv__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__sub__', '__truediv__', '__xor__'

DEF = ('''
def {0}(self, *args, **kwargs):
    return self.__class__(self.{1}.{0}(*args, **kwargs))
wrap_method = {0}
del({0})''', '''
def {0}(self, *args, **kwargs):
    return self.{1}.{0}(*args, **kwargs)
wrap_method = {0}
del({0})''')

PROP = '''
def setter(self, value):
    self.{1}.{0} = value
def getter(self):
    return self.{1}.{0}'''

def metodo(name, wrap='wrap'):
    # esta función es externa, ya que no se me permite incluirla en la definición de una metaclase
    # además de que el truco con funciones lambda no me funcionó
    # this function is external for the metaclass and the
    if name in MATHS:
        a = DEF[0].format(name, wrap)
    else:
        a = DEF[1].format(name, wrap)
    exec(a)
    method = wrap_method
    del(wrap_method)
    return method

def propiedad(name, wrap='wrap'):
    # igual esta que la anterior
    exec(PROP.format(name, wrap))
    ret = property(getter, setter)
    del(setter, getter)
    return ret

class MetaWrap(type):
    '''
    a class that wields this metaclass made that class a wrapper.
    When instanciate that class with an argumment automagically
    adopt all methods and atributes of that argument
    '''
    # métodos que no quiero sobreescribir
    invalid = ('__init__', '__new__', '__subclasshook__', '__class__', '__str__',
               '__delattr__', '__getattribute__', '__setattr__', '__repr__', '__doc__', 'wrap')
    _clss = {}
    def __init__(cls, name, bases, dct):
        super(MetaWrap, cls).__init__(name, bases, dct)
        if cls not in cls._clss:
            over = [method for method in dct if not method.startswith('__')]
            over_dct = {}
            for m in over:
                over_dct[m] = dct[m]
            cls._clss[cls] = over_dct

    def __call__(cls, *params, **kwparams):
        # obtener un parámetro o None si no hay
        wrap = None
        if params:
            wrap = params[0]
        if not params and kwparams:
            wrap = kwparams.popitem()[1]
        # obtener todos los atributos del objeto
        obj_attrs = dir(wrap)
        for attr in obj_attrs:
            # verificar que no esté sobre escrito
            if attr not in cls._clss[cls]:
                if callable(wrap.__getattribute__(attr)):
                    # asignar métodos a la clase y hacer que los método tengan un valor por default
                    if attr not in cls.invalid:
                        setattr(cls, attr, metodo(attr))
                else:
                    if attr not in cls.invalid and not attr.startswith('__'):
                        setattr(cls, attr, propiedad(attr))
        # crear el objeto
        obj = super(MetaWrap, cls).__call__()
        # y añadirle al vuelo el objeto a envolver
        obj.wrap = wrap
        return obj

def typewrapper(type_, name):
    '''
    a class that uses this decorator turns to a wrapper of type type_
    and wraps the attribute especified in name
    '''
    def body(cls):
        if type(name) != str:
            raise Exception('name must be string')
        atr = dir(type_)
        for a in atr:
            if not a.startswith('__'):
                if callable(getattr(type_, a)):
                    setattr(cls, a, metodo(a, name))
                else:
                    setattr(cls, a, propiedad(a, name))
        return cls
    return body
################################################################################################    
if __name__ == '__main__':
    ## algunos nombres no los he cambiado y es por una confusión de términos de mi parte entre
    ## Wrapper y Patrón Decorador, los he dejado así de momento
    
    # class Decorador(object): __metaclass__ = MetaWrap

    # class DecoSimple(Decorador):
        # def inerte(self): pass # se comporta como mixin
        
        # def mthod(self): # y ya puede 'sobre escribir' un método
            # return self.wrap.mthod() - 66

    # class DecoInt(Decorador): pass

    # class ObjetoSimple(object):
        # hola = 'je'
        # def mthod(self):
            # return 99

        # def atributize(self, value):
            # self.a = value

        # def get_a(self):
            # return self.a
    
    # obj = ObjetoSimple()
    # entero_decorado = DecoInt(5)
    # entero_decorado *= 10
    # print entero_decorado.wrap
    # obj_decorado = DecoSimple(obj)
    # print obj_decorado.mthod()
    # obj_decorado.atributize('hola')
    # print obj_decorado.get_a()
    # print obj_decorado.inerte()
    # print obj_decorado.hola
    pass
