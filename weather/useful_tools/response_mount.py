def weather_response(obj):
    return {'id': obj.id,
            'name_station': str(obj.name_station),
            'latitude': str(obj.latitude),
            'longitude': str(obj.longitude)}
