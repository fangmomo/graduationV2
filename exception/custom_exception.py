from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

from app.exception import ResponseCodeStatus


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    """
    # 添加 Http status code to the response
    if response is not None:
        print(response.data)
        response.data.clear()
        response.data['code'] = response.status_code
        response
        response.data['data'] = []

        
        if response.status_code == ResponseCodeStatus.VALIDATE_ERROR:
            response.data['message'] = 'Input error'
        """
    return response


def exception_handler(exc, content):
    data = {
        'result': False,
        'data': None
    }
    if isinstance(exc, ValidationError):
        # 更改返回的状态为为自定义错误类型的状态码
        data.update({
            'code': ResponseCodeStatus.VALIDATE_ERROR,
            'message': exc.message,
        })
    else:
        data.update({
            'code': ResponseCodeStatus.SERVER_500_ERROR,
            'message': exc.message,
        })
    set_rollback()
    return Response(data, status=status.HTTP_200_OK)