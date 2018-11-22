import json
import requests
from sqlalchemy import Column, DateTime, Integer, String

from app.models.basemodel import BaseModel
from pydruid.client import PyDruid
from app.models.druid_datasource import *


class DruidCluster(BaseModel):

    """ORM object referencing the Druid clusters"""

    __tablename__ = 'druid_clusters'
    type = "druid"

    cluster_name = Column(String(250), unique=True)
    coordinator_host = Column(String(255))
    coordinator_port = Column(Integer)
    coordinator_endpoint = Column(String(255), default='druid/coordinator/v1/metadata')
    broker_host = Column(String(255))
    broker_port = Column(Integer)
    broker_endpoint = Column(String(255), default='druid/v2')
    indexer_host = Column(String(255))
    indexer_port = Column(Integer)
    indexer_endpoint = Column(String(255), default='druid/indexer/v1/task')
    metadata_last_refreshed = Column(DateTime)
    cache_timeout = Column(Integer)
    druid_version = ""

    # def __init__(self, cluster_name, coordinator_host, coordinator_port, coordinator_endpoint, broker_host, broker_port, broker_endpoint, indexer_host, indexer_port,indexer_endpoint, cache_timeout ):
    def __init__(self, **kwargs):
        super(DruidCluster, self).__init__(**kwargs)

    def __setitem__(self, key, value):
        self.key = value


    def __repr__(self):
        return self.cluster_name

    def get_pydruid_client(self):
        cli = PyDruid(
            "http://{0}:{1}/".format(self.broker_host, self.broker_port),
            self.broker_endpoint)
        return cli

    def get_datasources(self):
        endpoint = (
            "http://{obj.coordinator_host}:{obj.coordinator_port}/"
            "{obj.coordinator_endpoint}/datasources"
        ).format(obj=self)

        return json.loads(requests.get(endpoint).text)

    def get_druid_version(self):
        endpoint = (
            "http://{obj.coordinator_host}:{obj.coordinator_port}/status"
        ).format(obj=self)
        return json.loads(requests.get(endpoint).text)['version']

    def ingest_datasources_batch_file(self, file_path_s3orlocal):
        endpoint = (
            "http://{obj.indexer_host}:{obj.indexer_port}/{obj.indexer_endpoint}"
        ).format(obj=self)
        return json.loads(requests.post(endpoint).text)
    # TODO Ingestion , depends on the file type

    def refresh_datasources(self, datasource_name=None):
        """Refresh metadata of all datasources in the cluster

        If ``datasource_name`` is specified, only that datasource is updated
        """
        self.druid_version = self.get_druid_version()
        for datasource in self.get_datasources():
                if not datasource_name or datasource_name == datasource:
                    DruidDatasource.sync_to_db(datasource, self)

    @property
    def perm(self):
        return "[{obj.cluster_name}].(id:{obj.id})".format(obj=self)

    @property
    def name(self):
        return self.cluster_name
