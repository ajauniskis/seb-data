# hadolint global ignore=DL3008,DL3013,DL3015,DL3006
FROM gcr.io/dataflow-templates-base/python311-template-launcher-base

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="/template/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/pipeline.py"
ENV FLEX_TEMPLATE_PYTHON_PY_OPTIONS=""
ENV FLEX_TEMPLATE_PYTHON_EXTRA_PACKAGES=""
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE=""

WORKDIR /template

# Copy pipeline files and requirements
COPY pipeline.py /template/
COPY requirements.txt /template/

RUN apt-get update \
    # Install any apt packages if required by your template pipeline.
    && apt-get install -y libffi-dev git \
    && rm -rf /var/lib/apt/lists/* \
    # Upgrade pip and install the requirements.
    && pip install --no-cache-dir --upgrade pip \
    # Install dependencies from requirements file in the launch environment.
    && pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE

# Set the entry point for the pipeline
ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
