from parse_it import ParseIt
from alert_on_rain.functions.weather_forecast.forecast import *
from alert_on_rain.functions.alerts.email import *
from alert_on_rain.functions.alerts.telegram import *


def init():
    """
    Run the logic which will take the variables (OWM api key & location) no matter how they are provided and will alert
    if it looks like it will rain there tomorrow
    """
    parser = ParseIt(recurse=False, config_type_priority=["envvars"])
    owm_api_key = parser.read_configuration_variable("owm_api_key", required=True)
    city = parser.read_configuration_variable("city", required=True)
    country_code = parser.read_configuration_variable("country_code", required=True)
    smtp_server = parser.read_configuration_variable("smtp_server", required=True)
    sender_email = parser.read_configuration_variable("sender_email", required=True)
    receiver_email = parser.read_configuration_variable("receiver_email", required=True)
    email_password = parser.read_configuration_variable("email_password", required=True)
    email_port = parser.read_configuration_variable("email_port", required=True)
    telegram_token = parser.read_configuration_variable("telegram_token", required=True)
    chat_id = parser.read_configuration_variable("chat_id", required=True)

    owm_object = WeatherForecast(owm_api_key, city, country_code)
    telegram_object = Telegram(telegram_token)

    if owm_object.rain_tomorrow() is True:
        telegram_object.send_alert(chat_id)
        email_alert(smtp_server, sender_email, receiver_email, email_password, email_port)
