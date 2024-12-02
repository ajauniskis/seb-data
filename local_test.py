from apache_beam import DoFn, ParDo
from apache_beam.io import ReadFromCsv, ReadFromParquet, WriteToBigQuery
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.pipeline import Pipeline


class ConvertNamedtupledToDict(DoFn):
    def process(self, element):
        yield element._asdict()


def run_pipeline(
    input_file: str,
    output_bq_table: str,
    beam_options: PipelineOptions,
) -> None:
    with Pipeline(options=beam_options) as pipeline:
        # Determine file type and read accordingly
        if input_file.endswith(".parquet"):
            data = pipeline | "ReadParquet" >> ReadFromParquet(input_file)
        else:
            data = (
                pipeline
                | "ReadCSV" >> ReadFromCsv(input_file)
                | "ConvertToDict" >> ParDo(ConvertNamedtupledToDict())
            )

        # Write data to BigQuery
        data | "WriteToBigQuery" >> WriteToBigQuery(
            output_bq_table,
            schema="SCHEMA_AUTODETECT",
            write_disposition=BigQueryDisposition.WRITE_APPEND,
            create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
        )  # pyright: ignore reportUnusedExpression


run_pipeline(
    "gs://seb-data-edge-data/input/yellowtrip/yellow_tripdata_2023-01.parquet",
    "seb-data:data.yellowtrip",
    PipelineOptions(
        runner="DataflowRunner",
        project="seb-data",
        region="us-east1",
        job_name="test-local",
    ),
)
