from threading import Thread


# Async decorator for Asynchronous email sending
def asynchronous(func):
    def wrapper(*args, **kwargs):
        # Create new thread for given target `func`
        thr = Thread(target=func, args=args, kwargs=kwargs)
        # Start new thread
        thr.start()

    # Return the wrapper function
    return wrapper
