from django.http import HttpResponse
from django.template import Context, Template
from django.utils.functional import Promise
from django.utils.encoding import force_unicode

try:
    from simplejson import JSONEncoder
except ImportError:
    try:
        from json import JSONEncoder
    except ImportError:
        from django.utils.simplejson import JSONEncoder

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

def render_json_response(data):
    json_serializer = LazyEncoder()
    return HttpResponse(json_serializer.encode(data), mimetype='application/json')

def render_form(form):
    data = {'valid': True}
    data['html'] = render_string("{{ form }}", {'form': form})
    return render_json_response(data)

def render_string(tmpl, ctx):
    return Template(tmpl).render(Context(ctx))

"""
def render_json_response(data):
    return HttpResponse(simplejson.dumps(data), mimetype='text/html')#application/json
"""
