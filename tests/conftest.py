from cloud_function.main import Settings

mock_cf_settings = Settings(
    project_id="test-project",
    service="test-service",
    env="test-env",
    dataflow_job_name="test-job",
    dataflow_bucket="test-bucket",
    region="test-region",
    bq_dataset_name="test-dataset",
    dataflow_sa="test-sa@test-project.iam.gserviceaccount.com",
)
