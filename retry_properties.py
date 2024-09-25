
# Sample:
# # Same as the above, but with the per-status limit taking precedence, so
# # the total wait time is 62 seconds:
# session.max_http_attempts = 6
# response = session.get('/users/PNOEXST')

def set_session_retry_properties(session):
    '''
    This will take about 30 seconds plus API request time, carrying out four
    attempts with 2, 4, 8 and 16 second pauses between them, before finally
    returning the status 404 response object for the user that doesn't exist:
    '''

    session.max_http_attempts = 4 # lower value takes effect
    session.retry[404] = 5 # this won't take effect
    session.sleep_timer = 1
    session.sleep_timer_base = 2

    return session
