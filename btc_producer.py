import requests, time
from bs4 import BeautifulSoup
from kafka import KafkaProducer

def get_btc_prices():
    curr_data = requests.get("https://openexchangerates.org/api/currencies.json")
    b_url = "https://api.coindesk.com/v1/bpi/currentprice/"

    curr = curr_data.json()
    btc_price_list = []

    for k,v in curr.items():
        api = str(b_url) + str(k) + str('.json')
        price = requests.get(api)
        if price.status_code == 200:
            code = (price.json()['bpi'][k]['code'])
            description = (price.json()['bpi'][k]['description'])
            date_time = (price.json()['time']['updated'])
            rate = (price.json()['bpi'][k]['rate'])
            temp =  [date_time,rate,k,v]
            btc_price_list.append(temp)
        else:
            None
    return btc_price_list


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

def connect_kafka_producer():
    btc_producer = None
    try:
        btc_producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return btc_producer

if __name__ == '__main__':
    all_prices = get_btc_prices()
    if len(all_prices) > 0:
        kafka_producer = connect_kafka_producer()
        for i in all_prices:
            btc_data = str(i)
            publish_message(kafka_producer, 'btcprices', 'pricedata', btc_data)

        if kafka_producer is not None:
            kafka_producer.close()
            


