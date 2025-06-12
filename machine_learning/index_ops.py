import logging
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from google.oauth2 import service_account

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MatchingEngineWrapper:
    def __init__(self, project: str, location: str, key_path: str):
        creds = service_account.Credentials.from_service_account_file(key_path)
        aiplatform.init(project=project, location=location, credentials=creds)
        self.project = project
        self.location = location

    def list_indexes(self, filter: Optional[str] = None) -> List[aiplatform.MatchingEngineIndex]:
        logger.info("Listing indexes in %s/%s ...", self.project, self.location)
        indexes = aiplatform.MatchingEngineIndex.list(filter=filter)  # type: ignore
        logger.info("Found %d indexes", len(indexes))
        return indexes

    def create_index(self,
        display_name: str,
        contents_delta_uri: str,
        dimensions: int,
        distance_measure_type: str = "DOT_PRODUCT_DISTANCE",
        index_update_method: str = "STREAM_UPDATE",
        labels: Optional[Dict[str, str]] = None
    ) -> aiplatform.MatchingEngineIndex:
        logger.info("Creating index %s ...", display_name)
        idx = aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=display_name,
            contents_delta_uri=contents_delta_uri,
            dimensions=dimensions,
            distance_measure_type=distance_measure_type,
            index_update_method=index_update_method,
            labels=labels or {},
        )
        logger.info("Index created: %s", idx.resource_name)
        return idx

    def get_index(self, index_name: str) -> aiplatform.MatchingEngineIndex:
        logger.info("Fetching index %s ...", index_name)
        idx = aiplatform.MatchingEngineIndex(index_name=index_name)
        logger.info("Found index: %s", idx.resource_name)
        return idx

    def upsert_datapoints(self, idx: aiplatform.MatchingEngineIndex, datapoints: List[Dict[str, Any]]):
        logger.info("Upserting %d datapoints ...", len(datapoints))
        resp = idx.upsert_datapoints(datapoints=datapoints)
        logger.info("Upsert completed.")
        return resp

    def remove_datapoints(self, idx: aiplatform.MatchingEngineIndex, ids: List[str]):
        logger.info("Removing %d datapoints ...", len(ids))
        resp = idx.remove_datapoints(datapoint_ids=ids)
        logger.info("Remove completed.")
        return resp

    def update_metadata(self,
        idx: aiplatform.MatchingEngineIndex,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None
    ):
        logger.info("Updating metadata for index %s", idx.resource_name)
        resp = idx.update_metadata(
            display_name=display_name,
            description=description,
            labels=labels
        )
        logger.info("Metadata update completed.")
        return resp

    def update_embeddings(self,
        idx: aiplatform.MatchingEngineIndex,
        contents_delta_uri: str,
        is_complete_overwrite: bool = False
    ):
        logger.info("Updating embeddings for index %s via URI %s (overwrite=%s)",
                    idx.resource_name, contents_delta_uri, is_complete_overwrite)
        resp = idx.update_embeddings(
            contents_delta_uri=contents_delta_uri,
            is_complete_overwrite=is_complete_overwrite
        )
        logger.info("Embeddings update initiated.")
        return resp
