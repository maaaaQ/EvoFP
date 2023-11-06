from kombu import Connection, Exchange, Producer, Queue


class BrokerManager:
    def set_connection_dsn(self, dsn):
        self.connection_dsn = Connection(dsn)
        self.producer = self.connection_dsn.Producer()

    def publish_message(self, exchange_name, routing_key, message):
        with Connection(self.connection_dsn) as connection:
            exchange = Exchange(exchange_name)
            queue = Queue(exchange=exchange, routing_key=routing_key)

            with connection.Producer() as producer:
                producer.publish(
                    message,
                    exchange=queue.exchange,
                    routing_key=queue.routing_key,
                )


broker_manager: BrokerManager = BrokerManager()


def inject_brokers(connection_dsn: str):
    broker_manager.set_connection_dsn(connection_dsn)


async def get_broker_manager() -> BrokerManager:
    yield broker_manager
