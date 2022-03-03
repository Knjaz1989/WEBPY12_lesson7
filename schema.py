CREATE_USER = {
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'pattern': '^([a-z0-9_\.-]+)@([a-z0-9_\.-]+)\.([a-z\.]{2,6})$'
        },
        'password': {
            'type': 'string',
            'pattern': '(?=.*[a-z])(?=.*[A-Z])[0-9!@#$%^&*a-zA-Z]{6,}'
        },
        'first_name': {
            'type': 'string'
        },
        'last_name': {
            'type': 'string'
        },
        'user_login': {
            'type': 'string'
        }
    },
    'required': ['email', 'password', 'user_login'],
    "additionalProperties": False
}

CREATE_ADV = {
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
    },
    'required': ['title'],
    "additionalProperties": False
}