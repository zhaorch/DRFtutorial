__author__ = 'zrc'
__date__ = '2019/7/1 14:43'

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "HelloWorld"