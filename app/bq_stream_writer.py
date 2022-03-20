import random
from datetime import datetime
from typing import Generator, List

from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types
from google.protobuf import descriptor_pb2

from app import logger, settings
from app.customer_pb2 import Customer

_num_of_batches: int = 2000
_batch_count: int = 500
_write_stream: str = f"projects/{settings.BQ_PROJECT_ID}/datasets/{settings.BQ_DATASET_ID}/tables/{settings.BQ_TABLE_ID}/streams/_default"


def faker_pubsub_generator() -> Generator[List[dict], None, None]:
    """Simula um generator do PubSub onde enviamos batchs de mensagens."""
    for _ in range(_num_of_batches):
        msgs = []
        for _ in range(_batch_count):
            now = datetime.now()
            cust_id = f"{now.minute}-{now.microsecond}"
            msgs.append({"id": f"cust-{cust_id}", "name": f"Customer {cust_id}", "score": random.randint(1, 100)})
        # logger.info("yielding fake pubsub batch msgs")
        yield msgs


def create_proto_schema() -> types.ProtoSchema:
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    Customer.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    return proto_schema


_proto_schema = create_proto_schema()


def request_generator(
    pubsub_generator: Generator[List[dict], None, None]
) -> Generator[types.AppendRowsRequest, None, None]:
    for msgs in pubsub_generator:
        rows = types.ProtoRows()
        for msg in msgs:
            customer = Customer()
            customer.id = msg["id"]
            customer.name = msg["name"]
            customer.score = msg["score"]
            rows.serialized_rows.append(customer.SerializeToString())
        proto_data = types.AppendRowsRequest.ProtoData(writer_schema=_proto_schema, rows=rows)
        request = types.AppendRowsRequest(write_stream=_write_stream, proto_rows=proto_data)
        # logger.info("yielding bq request")
        # logger.info(f"sending {len(msgs)} msgs")
        yield request


def run_bq_stream() -> None:
    client = bigquery_storage_v1.BigQueryWriteClient()
    stream = client.append_rows(requests=request_generator(faker_pubsub_generator()))
    count = 1
    for response in stream:
        logger.info(f"batch {count} sent")
        count = count + 1


# média de 500k msg por minuto da minha máquina local (br) para servidor us
# lembrando que as msgs são bem pequenas (é um obj com 3 colunas) e estão sendo criados localmente sem ter qualquer input externo (IO)