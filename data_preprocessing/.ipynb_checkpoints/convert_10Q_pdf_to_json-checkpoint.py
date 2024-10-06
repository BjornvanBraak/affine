# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: affine-project-kernel
#     language: python
#     name: affine-project-kernel
# ---

# %pip install unstructured-ingest
# %pip install python-dotenv

from dotenv import dotenv_values
ENV = dotenv_values(".env")

# +
#src: https://docs.unstructured.io/api-reference/ingest/source-connectors/local?utm_medium=email&_hsmi=320264015&utm_content=320264015&utm_source=hs_email
import os

from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
    LocalUploaderConfig
)
from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig
from unstructured_ingest.v2.processes.embedder import EmbedderConfig

# Chunking and embedding are optional.

if __name__ == "__main__":
    Pipeline.from_configs(
        context=ProcessorConfig(),
        indexer_config=LocalIndexerConfig(input_path='./data/unprocessed_pdf_data'),
        downloader_config=LocalDownloaderConfig(),
        source_connection_config=LocalConnectionConfig(),
        partitioner_config=PartitionerConfig(
            partition_by_api=True,
            api_key=ENV.get("UNSTRUCTURED_API_KEY"),
            partition_endpoint=ENV.get("UNSTRUCTURED_API_URL"),
            strategy="hi_res",
            additional_partition_args={
                "split_pdf_page": True,
                "split_pdf_allow_failed": True,
                "split_pdf_concurrency_level": 15
            }
        ),
        # chunker_config=ChunkerConfig(chunking_strategy="by_title"),
        # embedder_config=EmbedderConfig(embedding_provider="langchain-huggingface"),
        uploader_config=LocalUploaderConfig(output_dir='./data/preprocessed_pdf_data')
    ).run()

