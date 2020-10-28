from healthcheck import HealthCheck

from weather.models import DBDriver
from weather.views import ApiJsonHandler


class HealthcheckApi(ApiJsonHandler):

    @staticmethod
    def check_database():
        db_driver = DBDriver()
        response = [True, "database ok"]
        try:
            with db_driver.db_engine.connect() as conn:
                conn.execute("SELECT * FROM pg_stat_activity")
        except Exception as err:
            response = False, str(err)
        return response

    def get(self, *args, **kwargs):
        """
        ---
        tags:
        - Healthcheck
        summary: Get Healthcheck
        description: 'validate api dependencies'
        produces:
        - application/json
        responses:
            200:
              description: list of dependencies
        """
        health = HealthCheck()

        health.add_check(self.check_database)

        message, status_code, headers = health.run()
        self.set_status(status_code)
        self.finish(message)
