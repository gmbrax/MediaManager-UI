
JAVA_FILES := $(shell find MediaManager-core/src -name "*.java")
CORE_CLASSES := MediaManager-core/target/classes
CORE_JAR := ./MediaManager-core/target/MediaManager-Core-0.0.1-SNAPSHOT.jar
PROTO_SRC := MediaManager-core/target/generated-sources/protobuf/java
PROTO_DEST := ./src/MediaManager-UI/proto
PROTO_COPIED := $(PROTO_DEST)/.copied
PROTO_GENERATED := $(PROTO_SRC)/.generated
CONFIG_FILE := ./MediaManager-core/src/main/resources/config.properties
CONFIG_TEMPLATE := config.properties.example

PYTHON := python
VENV := .venv
VENV_BIN := $(VENV)/bin
DIST_DIR := dist
EXECUTABLE := $(DIST_DIR)/mediamanager-ui

.PHONY: ALL Clean JClean  JMakePythonProtoBuf Config

ALL: Config CopyProto

Config: $(CONFIG_FILE)

$(CONFIG_FILE):
	cp $(CONFIG_TEMPLATE) $(CONFIG_FILE)

JClean:
	cd MediaManager-core && mvn clean

JCompile: $(CORE_CLASSES)

$(CORE_CLASSES): $(JAVA_FILES)
	cd MediaManager-core && mvn compile
	touch $(CORE_CLASSES)

JMakePythonProtoBuf: $(PROTO_GENERATED)

$(PROTO_GENERATED): $(CORE_JAR)
	cd MediaManager-core && mvn protobuf:compile-python
	touch $(PROTO_GENERATED)

JPackage: ./MediaManager-core/target/MediaManager-Core-0.0.1-SNAPSHOT.jar

MediaManager-core/target/MediaManager-Core-0.0.1-SNAPSHOT.jar: $(JAVA_FILES)
	cd MediaManager-core && mvn package

CopyProto: $(PROTO_COPIED)

$(PROTO_COPIED): $(PROTO_GENERATED)
	mkdir -p ./src/MediaManager-UI/proto
	cp MediaManager-core/target/generated-sources/protobuf/java/*_pb2.py ./src/MediaManager-UI/proto
	touch $(PROTO_COPIED)

Clean:
	rm -rf ./src/MediaManager-UI/proto
	rm MediaManager-core/src/main/resources/config.properties
	cd MediaManager-core && mvn clean

Setup: $(VENV_BIN)/activate

$(VENV_BIN)/activate:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install protobuf nuitka