venv_dir = .venv

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: venv-setup install-poetry ## Install all dependencies
	poetry install --no-root

venv-setup: ## Setup Python virtual environment
	python3.11 -m venv ${venv_dir}

install-poetry: ## Install Poetry
	curl -sSL https://install.python-poetry.org | python3.11 -

tf-plan:
	cd terraform && terraform plan --var-file tfvars/common.tfvars --var-file tfvars/edge.tfvars

tf:
	cd terraform && terraform apply --var-file tfvars/common.tfvars --var-file tfvars/edge.tfvars

tf-destroy:
	cd terraform && terraform destroy --var-file tfvars/common.tfvars --var-file tfvars/edge.tfvars
