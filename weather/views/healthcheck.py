from healthcheck import HealthCheck
from weather.views import ApiJsonHandler


class HealthcheckApi(ApiJsonHandler):

    # @staticmethod
    # def __check_database():
    #     db_driver = DBDriver()
    #     db_driver.db_session.query("1").from_statement("SELECT 1").all()
    #     return True, "database ok"

    def get(self, *args, **kwargs):
        health = HealthCheck()

        # health.add_check(self.__check_rabbitmq)

        message, status_code, headers = health.run()
        self.set_status(status_code)
        self.finish(message)
