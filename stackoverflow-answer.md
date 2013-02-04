Ideas proposed here are excellent, but have some disadvantages:

 1. `inspect.getouterframes` and `args[0].__class__.__name__` are not suitable for plain functions and static-methods.
 2. `__get__` must be in a class, that is rejected by `@wraps`.
 3. `@wraps` itself should be hiding traces better.

So, I've combined some ideas from this page, links, docs and my own head,  
and finally found a solution, that lacks all three disadvantages above.

As a result, `method_decorator`:

 * Knows the class the decorated method is bound to.
 * Hides decorator traces by answering to system attributes more correctly than `functools.wraps()` does.
 * Is covered with unit-tests for bound an unbound instance-methods, class-methods, static-methods, and plain functions.

Usage:

    pip install method_decorator
    from method_decorator import method_decorator

    class my_decorator(method_decorator):
        # ...

See [full unit-tests for usage details](https://github.com/denis-ryzhkov/method_decorator/blob/master/method_decorator.py#L48).

And here is just the code of the `method_decorator` class:

    class method_decorator(object):
    
        def __init__(self, func, obj=None, cls=None, method_type='function'):
            # These defaults are OK for plain functions
            # and will be changed by __get__() for methods once a method is dot-referenced.
            self.func, self.obj, self.cls, self.method_type = func, obj, cls, method_type
    
        def __get__(self, obj=None, cls=None):
            # It is executed when decorated func is referenced as a method: cls.func or obj.func.
    
            if self.obj == obj and self.cls == cls:
                return self # Use the same instance that is already processed by previous call to this __get__().
    
            method_type = (
                'staticmethod' if isinstance(self.func, staticmethod) else
                'classmethod' if isinstance(self.func, classmethod) else
                'instancemethod'
                # No branch for plain function - correct method_type for it is already set in __init__() defaults.
            )
    
            return object.__getattribute__(self, '__class__')( # Use specialized method_decorator (or descendant) instance, don't change current instance attributes - it leads to conflicts.
                self.func.__get__(obj, cls), obj, cls, method_type) # Use bound or unbound method with this underlying func.
    
        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)
    
        def __getattribute__(self, attr_name): # Hiding traces of decoration.
            if attr_name in ('__init__', '__get__', '__call__', '__getattribute__', 'func', 'obj', 'cls', 'method_type'): # Our known names. '__class__' is not included because is used only with explicit object.__getattribute__().
                return object.__getattribute__(self, attr_name) # Stopping recursion.
            # All other attr_names, including auto-defined by system in self, are searched in decorated self.func, e.g.: __module__, __class__, __name__, __doc__, im_*, func_*, etc.
            return getattr(self.func, attr_name) # Raises correct AttributeError if name is not found in decorated self.func.
    
        def __repr__(self): # Special case: __repr__ ignores __getattribute__.
            return self.func.__repr__()
