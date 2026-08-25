from confluent_kafka import Producer
from logging import getLogger
from settings import settings
from schemas import Payment

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

def produce_message(message: str):
    try:
        producer.produce(
            topic='payment',
            key=f"payment",
            value=message,
            callback=producer_callback,
        )
        producer.flush()
    except Exception as e:
        logger.error(f"Error producing message: {e}")

def publish_payment_success(payment: Payment):
    produce_message(f"""{
        "user_id": {payment.user_id},
        "subscription_id": {payment.subscription_id},
        "payment_id": {payment.yookassa_payment_id}
        }""")
