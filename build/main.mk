#vim: set ts=2 sw=2 sts=2 ai noet :
.PHONY: help list clean plan
.DEFAULT_GOAL := help    ## no-help
.ONESHELL: ;             # recipes execute in same shell
.EXPORT_ALL_VARIABLES: ; # send all vars to shell

SHELL        := $(shell which bash)
.SHELLFLAGS = -c

UID            := $(shell id -u)
GID            := $(shell id -g)
interactive    := $(shell [ -t 0 ] && echo 1)
CREATED_BY     ?= $(shell id -u -n)
PLAN_FILE      ?= $(TF_VAR_env).plan

SELF_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

define SELF_DIR_NAME
$(shell printf '%s' $${PWD##*/}/..)
endef

BIN ?= $(SELF_DIR_NAME)

## Platform Specific Variables
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    BASE64_FLAGS := -w 0
  DOCKER_GID = $(shell stat -c %g /var/run/docker.sock)
endif
ifeq ($(UNAME_S),Darwin)
    BASE64_FLAGS :=
  DOCKER_GID := 50
endif

ifeq (1,$(interactive))
	TERRAFORM_ARGS := -it
endif

REGISTRY    ?= registry.hub.docker.io
REPO_NAME   ?= trinitronx/$(BIN)
REPO        ?= $(REGISTRY)/$(REPO_NAME)
ENV         ?= dev
BUILD_IMAGE ?= $(REGISTRY)/python

DOCKER_CONFIG  ?= ./.docker

# Always trash an old docker config right away.
$(shell find $(DOCKER_CONFIG) -mmin +720 -exec rm -f '{}' \; 2>/dev/null)

DOCKER         ?= docker --config $(DOCKER_CONFIG)
JQ_DOCKER      ?= $(DOCKER) run --rm -i -u $(UID):$(GID) stedolan/jq

CONTAINER_SOURCE_PATH  ?= /src/$(REPO_NAME)
CONTAINER_SOURCE_FLAGS ?= -v $(PWD):$(CONTAINER_SOURCE_PATH) -w $(CONTAINER_SOURCE_PATH)

ifdef TRAVIS_BUILD_NUMBER
	DEPLOY_TAG ?= $(TRAVIS_BUILD_NUMBER)
else
	DEPLOY_TAG ?= $(shell TZ=UTC date +'%Y%m%dT%H%M%S')-$(shell git rev-parse --short HEAD)
endif


ifndef TRAVIS_PULL_REQUEST_BRANCH
	ifeq ($(TRAVIS_BRANCH),master)
		NOT_LATEST :=
		DEPLOY_TAG := $(shell cat VERSION)
	else
		NOT_LATEST := true
	endif
else
	NOT_LATEST := true
endif

# Auto-documented Makefile
# Source: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Shows this generated help info for Makefile targets
	@grep -Eh '^[a-zA-Z_-]+:.*?(## )?.*$$' $(MAKEFILE_LIST) | sort | awk '{ c=split($$0,resultArr,/:+/) ; if ( !(resultArr[c-1] in targets) ) { if ( /:.*##/ ) { if ( ! /no-help/ ) { sub(/^.*## ?/," ",resultArr[c]); targets[resultArr[c-1]] = resultArr[c]; } } else { targets[resultArr[c-1]] = "" } } } END { for (target in targets) { printf "\033[36m%-30s\033[0m %s\n", target, targets[target] } }' | sort

list: ## Just list all Makefile targets without help
	@$(MAKE) -pRrq $(addprefix -f ,$(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | uniq | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | grep -v 'DEFAULT_GOAL' | xargs

$(DOCKER_CONFIG)/config.json:
	if docker login --help  | grep -q '\-e'; then \
	  $(DOCKER) login -e="$(DOCKER_EMAIL)" -u="$(DOCKER_USERNAME)" -p="$(DOCKER_PASSWORD)" ; \
	else \
	  $(DOCKER) login -u="$(DOCKER_USERNAME)" -p="$(DOCKER_PASSWORD)" ; \
	fi

.packaged: ${PACKAGE_DEPENDENCIES}
	if [ ! -z "$$($(DOCKER) images  $(REPO):$(DEPLOY_TAG))" ]; then                  \
		$(DOCKER) build  $(DOCKER_BUILD_ARGS) -t $(REPO):$(DEPLOY_TAG) . ;           \
		if [ -z "$(NOT_LATEST)" ]; then                                             \
			$(DOCKER) tag "$(REPO):$(DEPLOY_TAG)" "$(REPO):latest";                  \
		fi;                                                                          \
	fi
	echo "$(DEPLOY_TAG)" > $@

package: .packaged ## Generates a docker image for this project.
	$(info  TRAVIS_EVENT_TYPE:          $(TRAVIS_EVENT_TYPE))
	$(info  TRAVIS_BRANCH:              $(TRAVIS_BRANCH))
	$(info  TRAVIS_PULL_REQUEST:        $(TRAVIS_PULL_REQUEST))
	$(info  TRAVIS_PULL_REQUEST_BRANCH: $(TRAVIS_PULL_REQUEST_BRANCH))
	$(info  NOT_LATEST:                 $(NOT_LATEST))
	$(info  DEPLOY_TAG:                 $(DEPLOY_TAG))

$(REPO_NAME).tar: .packaged
	$(eval DEPLOY_TAG := $(shell cat .packaged))
	docker save --output "$@" "$(REPO):$(DEPLOY_TAG)"

save-image: $(REPO_NAME).tar ## Perform `docker save` on the packaged image.

.shipped: .packaged | $(DOCKER_CONFIG)/config.json
	$(eval DEPLOY_TAG := $(shell cat .packaged))
	if [ -z "$$(cat $@)" ]; then                                \
	  rm $@;                                                    \
	  $(DOCKER) push $(REPO):$(DEPLOY_TAG);                     \
	  if [ -z "$(NOT_LATEST)" ]; then                           \
	    $(DOCKER) tag "$(REPO):$(DEPLOY_TAG)" "$(REPO):latest"; \
	    $(DOCKER) push "$(REPO):latest";                        \
	  fi;                                                       \
	fi
	echo "$(DEPLOY_TAG)" > $@

ship: .shipped ## Pushes the packaged docker image to the docker registry (ECR). Tags image with `VERSION` specified  and `latest` (unless the parameter `NOT_LATEST` is set)

# Override in files including this one to execute before `.docker-container-*` calls `make` (inside the container).
CONTAINER_PRE_BUILD_COMMAND ?=
# This is to match UID from build host so file owners match during container-* targets
CREATE_SRC_OWNER_UID_AND_SU := getent group $(DOCKER_GID) 2>&1 1>/dev/null || groupadd -g $(DOCKER_GID) docker ; useradd --uid $(UID) --gid $(DOCKER_GID) --shell /bin/sh --no-create-home --home-dir $(HOME) $(USER) && /bin/su --preserve-environment $(USER) --command /bin/sh

.PHONY: container-%
container-%: | $(DOCKER_CONFIG)/config.json
	$(DOCKER) run                                                 \
	--rm                                                          \
	-e HOME                                                       \
	-e ENV                                                        \
	-v ${HOME}                                                    \
	-v /var/run/docker.sock:/var/run/docker.sock                  \
	--name "$(REPO_NAME)-$(DEPLOY_TAG)-$*"                        \
	--env-file <(env)                                             \
	--entrypoint /bin/bash                                        \
	$(DOCKER_AWS_CREDENTIALS)                                     \
	$(CONTAINER_SOURCE_FLAGS)                                     \
	"$(BUILD_IMAGE)" -c "$(CREATE_SRC_OWNER_UID_AND_SU) $(CONTAINER_PRE_BUILD_COMMAND) ; make $*;"

.PHONY: clean
clean:: ## Remove temporary / build files.
	rm -f $(REPO_NAME).tar
	rm -rf $(DOCKER_CONFIG)
	rm -rf .deploy*
	rm -rf .docker*
	rm -f .packaged
	rm -f .shipped
