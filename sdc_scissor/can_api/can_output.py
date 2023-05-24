import abc
import datetime
import logging
from pathlib import Path

import can
import cantools
import click
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

from sdc_scissor.config import CONFIG

_logger = logging.getLogger(__file__)


class ICANBusOutput(abc.ABC):
    @abc.abstractmethod
    def output_can_msg(self, msg: can.Message):
        pass


class NoCANBusOutput(ICANBusOutput):
    def output_can_msg(self, msg):
        pass


class AbstractOutputDecorator(ICANBusOutput, abc.ABC):
    def __init__(self, wrappee: ICANBusOutput):
        self.wrappee = wrappee

    @abc.abstractmethod
    def output_can_msg(self, msg: can.Message):
        pass


class CANBusOutputDecorator(AbstractOutputDecorator):
    def __init__(self, wrappee: ICANBusOutput):
        super().__init__(wrappee)
        # Configuration is according to: https://python-can.readthedocs.io/en/stable/bus.html
        self.bus = can.interface.Bus(
            interface=CONFIG.CAN_INTERFACE, channel=CONFIG.CAN_CHANNEL, bitrate=CONFIG.CAN_BITRATE
        )

    def output_can_msg(self, msg: can.Message):
        try:
            self.bus.send(msg)
        except can.CanError as err:
            logging.error(err)
        self.wrappee.output_can_msg(msg)


class StdOutDecorator(AbstractOutputDecorator):
    """
    StdOutDecorator Objects are used to offer a flexible output_handler for th CAN messages.
    """

    def __init__(self, wrappee: ICANBusOutput):
        super().__init__(wrappee)

    def output_can_msg(self, msg: can.Message):
        """
        Decorator class to output CAN messages to the console

        :param msg: The CAN message that should be sent to the output_handler.
        :return:
        """
        click.echo(click.style(msg, fg="green"))
        self.wrappee.output_can_msg(msg)


def _write_influxdb_data_record(api, bucket: str, org: str, record: Point):
    _logger.info("write to influxdb")
    try:
        api.write(bucket=bucket, org=org, record=record)
    except Exception as ex:
        logging.error("cannot write record: {}\texception: {}".format(record, ex))


def _influxdb_bucket_setup(write_client: InfluxDBClient, bucket, org):
    bucket_api = write_client.buckets_api()
    if bucket_api.find_bucket_by_name(bucket_name=bucket) is None:
        bucket_api.create_bucket(bucket_name=bucket, org=org)


class InfluxDBDecorator(AbstractOutputDecorator):
    def __init__(self, wrappee: ICANBusOutput, write_client: InfluxDBClient, bucket: str, org: str):
        super().__init__(wrappee)
        _influxdb_bucket_setup(write_client, bucket, org)
        self.write_client = write_client
        self.write_api = write_client.write_api(write_options=ASYNCHRONOUS, batch_size=500)
        self.bucket = bucket
        self.org = org
        self.can_db = cantools.db.load_file(Path(CONFIG.CAN_DBC_PATH))
        self.cache = []

    def output_can_msg(self, msg: can.Message):
        for msg_specs in self.can_db.messages:
            decoded_msg = None
            try:
                decoded_msg = self.can_db.decode_message(msg_specs.frame_id, msg.data)
            except Exception as ex:
                _logger.info("can msg: {}\tdecoded msg: {}\texception: {}".format(msg, decoded_msg, ex))
                continue

            point = Point(CONFIG.EXECUTION_START_TIME).tag("test_id", CONFIG.CURRENT_TEST_ID)
            for signal_name, signal_value in decoded_msg.items():
                msg_sample_time = datetime.datetime.utcfromtimestamp(msg.timestamp)
                print("utc: {}\traw: {}".format(msg_sample_time, msg.timestamp))
                point = point.field(field=signal_name, value=signal_value).time(str(msg_sample_time))
                _write_influxdb_data_record(self.write_api, CONFIG.INFLUXDB_BUCKET, CONFIG.INFLUXDB_ORG, point)

        self.wrappee.output_can_msg(msg)
