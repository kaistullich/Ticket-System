from threading import Thread

# Async decorator for Asynchronous email sending
def async_(f):
    def wrapper(*args, **kwargs):
        # Create new thread for given target `f`
        thr = Thread(target=f, args=args, kwargs=kwargs)
        # Start new thread
        thr.start()
    return wrapper
