import argparse

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
        # temp_path: str,
        # staging_path: str,
        region: str,
        job_name: str,
    ):
        self.input_file = input_file
        self.output_bq_table = output_bq_table
        self.project_id = project_id
        self.region = region
        # self.temp_path = temp_path
        # self.staging_path = staging_path
        # self.job_name = job_name

    def run(self):
        pipeline_options = PipelineOptions(
            # runner="DataflowRunner",
            # project=self.project_id,
            # region=self.region,
            # temp_location=self.temp_path,  # Specify a GCS temp location
            # staging_location=self.staging_path,  # Specify GCS staging location
            # job_name=self.job_name,  # Unique job name
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
                    # custom_gcs_temp_location=self.temp_path,
                )  # pyright: ignore reportUnusedExpression
            )

        pipeline.run()


class Options(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--input_file", help="Project", required=True)
        parser.add_argument("--output_bq_table", help="Pub Sub", required=True)
        parser.add_argument("--project_id", help="Pub Sub", required=True)
        parser.add_argument(
            "--template_location",
            default="gs://seb-data-edge-artifacts/dataflow/gcs-to-bq-tpl.json",
        )


def run_pipeline(input_file, output_bq_table, beam_options):
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


if __name__ == "main":
    # args = Options()
    parser = argparse.ArgumentParser()
    _, beam_args = parser.parse_known_args()

    beam_options = PipelineOptions(beam_args)
    args = beam_options.view_as(Options)
    print(args)
    print(beam_options)

    run_pipeline(
        input_file=args.input_file,
        output_bq_table=args.output_bq_table,
        beam_options=beam_options,
    )

    # GcsToBigQueryPipeline(
    #     input_file=args.input_file,
    #     output_bq_table=args.output_bq_table,
    #     project_id=args.project_id,
    # ).run()
