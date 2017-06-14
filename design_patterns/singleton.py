"""
Opis wzorca można znaleźć tutaj:
https://4programmers.net/In%C5%BCynieria_oprogramowania/Wzorce_projektowe/Singleton
"""

class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super().__new__(cls, *args, **kwargs)
        return cls._inst

class Foo(Singleton):
    pass

class Bar(Foo):
    pass

f = Foo()
b = Bar()

print(f is b)
