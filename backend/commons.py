

class StatusCodeEnum:

    Failed = 1000
    AuthFailed = 1001
    ArgsError = 1002

    Success = 2000
    # 发帖

    # 评论

    # 点赞
    FavorPlus = 2301
    FavorMinus = 2302


class BaseResponse():
    def __init__(self):
        self.status = False
        self.code = '200'
        self.data = None
        self.summary = None
        self.message = {}
