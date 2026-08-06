import logging
from dataclasses import dataclass
from typing import AsyncIterator

import orjson
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)

from infrastructure.message_brokers.base import BaseMessageBroker


logger = logging.getLogger(__name__)


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def send_message(self, key: bytes, topic: str, value: bytes) -> None:
        logger.debug('publishing: topic=%s key=%s, value=%s', topic, key, value)
        await self.producer.send(topic=topic, value=value, key=key)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        logger.debug('start consuming %s', topic)
        self.consumer.subscribe(topics=[topic])

        async for message in self.consumer:
            logger.debug(
                'consuming: topic=%s key=%s value=%s timestamp_ms=%s',
                message.topic,
                message.key,
                message.value,
                message.timestamp,
            )
            yield orjson.loads(message.value)

    async def stop_consuming(self) -> None:
        logger.debug('stop consuming')
        self.consumer.unsubscribe()

    async def start(self) -> None:
        logger.debug('start producer and consumer.')
        await self.producer.start()
        await self.consumer.start()

    async def close(self) -> None:
        logger.debug('stop producer and consumer.')
        await self.producer.stop()
        await self.consumer.stop()
