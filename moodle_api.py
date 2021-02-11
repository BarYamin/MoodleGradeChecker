from requests import get, post
import ssl

# Module variables to connect to moodle api
ENDPOINT = "/webservice/rest/server.php?moodlewsrestformat=json"
SERVICE = "moodle_mobile_app"

class MoodleClient:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    def get_class_info(self, class_id):
        quizzes_by_course = call(
            "mod_quiz_get_quizzes_by_courses",
            url=self.url,
            username=self.username,
            password=self.password,
            courseids=[class_id])
        return list(quizzes_by_course.get('quizzes'))


def get_token(url, username, password):
    token_url = f"https://{url}/login/token.php?username={username}&password={password}&service={SERVICE}"
    resp = post(token_url, verify=False)
    return resp.json()['token']


def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def call(fname, url, username, password, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": get_token(url, username, password), 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = get(f"https://{url}{ENDPOINT}", parameters, verify=False)
    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response
