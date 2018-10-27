def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # import os
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # os.path.join(BASE_DIR, "log.txt")
        # with open("log.txt", "a") as wf:
        #     wf.write(str(request.__dict__))

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware