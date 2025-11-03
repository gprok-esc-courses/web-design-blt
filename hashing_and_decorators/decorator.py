from functools import wraps

# assume this was in session
role = 'admin'

def roles_permitted(roles):
     global role
     def decorator(f):
         @wraps(f) 
         def wrapper(*args, **kwargs):
             if role not in args[0]:
                 print("NO ACCESS")
                 return
             else:
                 return f(*args, **kwargs)
         return wrapper
     return decorator


@roles_permitted(['admin'])
def function1(roles):
    print("Function 1")

@roles_permitted(['member'])
def function2(roles):
    print("Function 2")


function1(['admin'])
function1(['member'])

function2(['admin'])
function2(['member'])