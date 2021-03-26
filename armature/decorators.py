def dont_use(func):
    def inner():
        raise Exception("Don't use this method")

    return inner
