

class BaseResponse():
    def __init__(self):
        self.status = False
        self.code = '200'
        self.data = None
        self.summary = None
        self.message = {}
