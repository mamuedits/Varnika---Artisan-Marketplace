from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'detail': 'Request could not be processed.',
            'errors': {}
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data and len(response.data) == 1:
                custom_data['detail'] = str(response.data['detail'])
            else:
                custom_data['detail'] = 'Validation failed. Please check the highlighted fields.'
                custom_data['errors'] = response.data
        elif isinstance(response.data, list):
            custom_data['detail'] = str(response.data[0]) if response.data else 'Invalid request.'
            custom_data['errors'] = {'non_field_errors': response.data}

        response.data = custom_data

    return response