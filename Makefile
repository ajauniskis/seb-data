help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

tf-plan:
	cd terraform && terraform plan --var-file tfvars/common.tfvars --var-file tfvars/edge.tfvars

tf:
	cd terraform && terraform apply --var-file tfvars/common.tfvars --var-file tfvars/edge.tfvars
