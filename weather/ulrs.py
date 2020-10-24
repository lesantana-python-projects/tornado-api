from weather.views.healthcheck import HealthcheckApi

routes = [
    (r'/api/healthcheck', HealthcheckApi),
]
