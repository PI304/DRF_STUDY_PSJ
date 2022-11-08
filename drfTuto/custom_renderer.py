from rest_framework import renderers

class CustomRenderer(renderers.BaseRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get('response')

        response = {
            'status': response_data.status_text,
            'data': data
        }
        
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)