from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import GCS
from diagrams.onprem.client import Users


def generate() -> None:
    with Diagram(
        "GCS File Ingestion to BQ", show=False, filename="docs/diagram", direction="LR"
    ):
        with Cluster("GCP"):
            with Cluster("Source"):
                gcs = GCS("GCS")
            with Cluster("Target"):
                bq = BigQuery("BigQuery")
            cf = Functions("Cloud Function")
            pubsub = PubSub("Pub/Sub")
            dataflow = Dataflow("Dataflow")
        user = Users("User")

        (
            user
            >> Edge(label="put file")
            >> gcs
            >> Edge(label="notify")
            >> pubsub
            >> Edge(label="invoke")
            >> cf
            >> Edge(label="invoke")
            >> dataflow
            >> Edge(label="load")
            >> bq
        )  # pyright: ignore reportUnusedExpression

        (
            dataflow >> Edge(label="read", style="dashed") >> gcs
        )  # pyright: ignore reportUnusedExpression


if __name__ == "__main__":
    generate()
