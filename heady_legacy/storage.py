from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CloudArchiveConfig:
    provider: str
    bucket_name: str
    region: str
    kms_key_id: str


class CloudArchiveClient:
    def __init__(self, config: CloudArchiveConfig) -> None:
        self._config = config

    def build_object_uri(self, object_name: str) -> str:
        if self._config.provider.lower() == "aws":
            return f"s3://{self._config.bucket_name}/{object_name}"
        if self._config.provider.lower() == "gcp":
            return f"gs://{self._config.bucket_name}/{object_name}"
        return f"{self._config.provider}://{self._config.bucket_name}/{object_name}"

    def encryption_metadata(self) -> Dict[str, str]:
        return {
            "kms_key_id": self._config.kms_key_id,
            "encryption": "server-side",
            "region": self._config.region,
        }

    def prepare_upload_manifest(self, object_name: str) -> Dict[str, str]:
        return {
            "object_uri": self.build_object_uri(object_name),
            **self.encryption_metadata(),
        }
