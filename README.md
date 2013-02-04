method_decorator
================

This Python decorator knows the class the decorated method is bound to.

It is unusual for Python, because, when the decorator is applied to just-defined method, the class does not exist yet.  
And once this class is not known in advance, it is almost impossible to get this knowledge, while desired.  
I needed this when I was implementing RPC of class-methods (and other types of functions) over AMQP.  
It is also needed for some other people, according to [this Stack Overflow question](http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class/).  
From [my answer there](http://stackoverflow.com/questions/306130/python-decorator-makes-function-forget-that-it-belongs-to-a-class/3412743#3412743):

Ideas proposed here are excellent, but have some disadvantages:
* `inspect.getouterframes` and `args[0].__class__.__name__` are not suitable for plain functions and static-methods.
* `__get__` must be in a class, that is rejected by `@wraps`.
* `@wraps` itself should be hiding traces better.

So, I've combined some ideas from that page, links, docs and my own head,  
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

method_decorator version 0.1.3  
Copyright (C) 2013 by Denis Ryzhkov <denisr@denisr.com>  
MIT License, see http://opensource.org/licenses/MIT
