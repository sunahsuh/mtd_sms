from twilio.twiml import Response
from django_twilio.decorators import twilio_view
from cumtd import CumtdApi
import os

@twilio_view
def reply_to_sms_message(request):
    text = request.REQUEST['Body']
    mtd = CumtdApi(os.environ['CUMTD_API_KEY'])
    stops = mtd.get_stops_by_search(text)
    buses = mtd.get_departures_by_stop(stops['stops'][0]['stop_id'])
    r = Response()
    response_text = 'Departures at ' + stops['stops'][0]['stop_name'] + '\n'
    for trip in buses['departures']:
        response_text += trip['headsign'] + ' in ' + str(trip['expected_mins']) + ' mins\n'
    r.sms(response_text[:159])
    return r


