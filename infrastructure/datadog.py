from datadog import initialize, api


def configure_datadog():
    options = {
        "api_key": '92676c44d10b7268d0399c5ea6b47ea7',
        "app_key": 'd71e5800fb925e2aab6a85c0377e40c82ea3d458'
    }

    initialize(**options)