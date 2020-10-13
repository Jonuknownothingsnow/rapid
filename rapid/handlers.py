from sanic import response
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler
from traceback import format_exc
from sanic.log import logger

INTERNAL_SERVER_ERROR_HTML = """
    <h1>Internal Server Error</h1>
    <p>
        The server encountered an internal error and cannot complete
        your request.
    </p>
"""


class JosnErrorHandler(ErrorHandler):
    def default(self, request, exception):
        """
        Provide a default behavior for the objects of :class:`ErrorHandler`.
        If a developer chooses to extent the :class:`ErrorHandler` they can
        provide a custom implementation for this method to behave in a way
        they see fit.

        :param request: Incoming request
        :param exception: Exception object

        :type request: :class:`sanic.request.Request`
        :type exception: :class:`sanic.exceptions.SanicException` or
            :class:`Exception`
        :return:
        """
        self.log(format_exc())
        try:
            url = repr(request.url)
        except AttributeError:
            url = "unknown"

        response_message = "Exception occurred while handling uri: %s"
        logger.exception(response_message, url)

        if issubclass(type(exception), SanicException):
            d = {"err": "Error: {}".format(exception), "msg": "", "success": False}
            return response.json(
                d,
                status=getattr(exception, "status_code", 500),
                headers=getattr(exception, "headers", dict()),
            )
        elif self.debug:
            html_output = self._render_traceback_html(exception, request)

            return response.html(html_output, status=500)
        else:
            return response.html(INTERNAL_SERVER_ERROR_HTML, status=500)
