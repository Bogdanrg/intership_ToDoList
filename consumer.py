import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from analytical_service.services import AnalyticalServices
from config import settings


class AIOConsumer:
    action_handlers = {
        "add_phone": AnalyticalServices.create_phone_document,
        "add_food": AnalyticalServices.create_food_document,
        "search_phone": AnalyticalServices.search_phone_document,
        "search_food": AnalyticalServices.search_food_document
    }

    @staticmethod
    async def consume():
        consumer = AIOKafkaConsumer(
            settings.kafka.KAFKA_TOPIC_NAME,
            bootstrap_servers=[settings.kafka.BOOTSTRAP_SERVER],
            group_id="analyze-group"
        )
        await consumer.start()
        try:
            async for msg in consumer:
                logging.info(f"consumed: {msg.topic}, {msg.partition}, {msg.value}")
                consumed_message = json.loads(msg.value)
                event_type = consumed_message.pop("action")
                event_handler = AIOConsumer.action_handlers.get(event_type)
                await event_handler(consumed_message)
        finally:
            await consumer.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(AIOConsumer.consume())
