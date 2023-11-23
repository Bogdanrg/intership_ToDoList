import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from base.classes import IndexRegistryBase
from config import settings


class AIOConsumer:

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
                event_handler = IndexRegistryBase.INDEX_METHODS_REGISTRY.get(event_type)
                await event_handler(consumed_message)
        finally:
            await consumer.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(AIOConsumer.consume())
