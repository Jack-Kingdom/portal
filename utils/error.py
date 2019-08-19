class CodeError(BaseException):

    def __init__(self, code):
        self.code = code
