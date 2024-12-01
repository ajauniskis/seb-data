from apache_beam import DoFn, ParDo
from apache_beam.io import ReadFromCsv, ReadFromParquet, WriteToBigQuery
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.pipeline import Pipeline


class ConvertNamedtupledToDict(DoFn):
    def process(self, element):
        yield element._asdict()


class GcsToBigQueryPipeline:
    def __init__(
        self,
        input_file: str,
        output_bq_table: str,
        project_id: str,
        temp_path: str,
        staging_path: str,
        region: str,
        job_name: str,
    ):
        self.input_file = input_file
        self.output_bq_table = output_bq_table
        self.project_id = project_id
        self.region = region
        self.temp_path = temp_path
        self.staging_path = staging_path
        self.job_name = job_name

    def run(self):
        pipeline_options = PipelineOptions(
            runner="DataflowRunner",
            project=self.project_id,
            region=self.region,
            temp_location=self.temp_path,  # Specify a GCS temp location
            staging_location=self.staging_path,  # Specify GCS staging location
            job_name=self.job_name,  # Unique job name
            save_main_session=True,
        )

        # Start the pipeline
        with Pipeline(options=pipeline_options) as pipeline:
            if self.input_file.endswith(".parquet"):
                data = pipeline | "ReadParquet" >> ReadFromParquet(
                    self.input_file,
                )
            else:
                data = (
                    pipeline
                    | ReadFromCsv(self.input_file)
                    | ParDo(ConvertNamedtupledToDict())
                )

            (
                data
                | "WriteToBigQuery"
                >> WriteToBigQuery(
                    self.output_bq_table,
                    # Let BigQuery auto-detect the schema from file
                    schema="SCHEMA_AUTODETECT",
                    write_disposition=BigQueryDisposition.WRITE_APPEND,
                    create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                    custom_gcs_temp_location=self.temp_path,
                )  # pyright: ignore reportUnusedExpression
            )
