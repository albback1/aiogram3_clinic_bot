import pytz

def convert_to_moscow_time(utc_time):
    """Конвертирование UTC времени к московскому"""
    moscow_tz = pytz.timezone('Europe/Moscow')  # Московский часовой пояс
    return utc_time.replace(tzinfo=pytz.utc).astimezone(moscow_tz)