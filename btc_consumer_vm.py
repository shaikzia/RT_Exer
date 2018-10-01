import json 
from kafka import KafkaConsumer 

# To consume latest messages and auto-commit offsets 
consumer = KafkaConsumer('vm_btc',
#                          group_id='program',
                          bootstrap_servers=['127.0.0.1:9092'])

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
					 message.offset, message.key,
					 message.value))

# Consume earliest messages, don't commit offsets 
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# Consume JSON messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# Stop Iteration if no message after 1 sec 
KafkaConsumer(consumer_timeout_ms=1000)


