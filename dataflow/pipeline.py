import argparse

from apache_beam import DoFn, ParDo
from apache_beam.io import ReadFromCsv, ReadFromParquet, WriteToBigQuery
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.pipeline import Pipeline


class ConvertNamedtupledToDict(DoFn):
    def process(self, element):
        yield element._asdict()


class Options(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--input_file", help="Project", required=True)
        parser.add_argument("--output_bq_table", help="Pub Sub", required=True)
        parser.add_argument("--project_id", help="Project ID", required=True)
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

    pipeline.run().wait_until_finish()


if __name__ == "main":
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
