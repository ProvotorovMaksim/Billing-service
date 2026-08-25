from confluent_kafka import Producer
from logging import getLogger
from settings import settings

logger = getLogger("kafkaproducer")
logger.setLevel("INFO")

producer_config = {
    'bootstrap.servers': settings.KAFKA_BROKER_URL,
    'acks': 'all',
    'enable.idempotence': True,
    'retries': 5,
    'delivery.timeout.ms': 1000,
}

producer = Producer(producer_config)

def producer_callback(*args):
    for arg in args:
        logger.info(arg)

def produce_message(message):
    try:
        producer.produce(
            topic='multi-partition',
            key=f"auth",
            value=message,
            callback=producer_callback,
        )
        producer.flush()
    except Exception as e:
        logger.error(f"Error producing message: {e}")