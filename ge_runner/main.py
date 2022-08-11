import great_expectations as ge
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig, DatasourceConfig, FilesystemStoreBackendDefaults
from great_expectations.core.batch import BatchRequest
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)
from ruamel import yaml



data_context_config = DataContextConfig(
    config_version=2,
    plugins_directory=None,
    config_variables_file_path=None,
    datasources={
        "my_mysql_datasource": DatasourceConfig(
            class_name="Datasource",
            execution_engine={
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": "mysql+pymysql://root:example@source/demo"
            },
            data_connectors={
                "default_inferred_data_connector_name": {
                    "class_name": "InferredAssetSqlDataConnector",
                    "include_schema_name": True,
                    
                }
            },
        ),
        "my_postgresql_datasource": DatasourceConfig(
            class_name="Datasource",
            execution_engine={
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": "postgresql+psycopg2://postgres:example@destination/postgres"
            },
            data_connectors={
                "default_inferred_data_connector_name": {
                    "class_name": "InferredAssetSqlDataConnector",
                    "include_schema_name": True,
                    
                }
            },
        ),
    },
    stores={
        "expectations_S3_store": {
            "class_name": "ExpectationsStore",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory":  "/opt/great_expectations/great_expectation_stores/my_expectations_store_prefix",
            },
        },
        "checkpoint_store": {
            "class_name": "CheckpointStore",
            "store_backend": {
               "class_name": "TupleFilesystemStoreBackend",
                "base_directory":  "/opt/great_expectations/great_expectation_stores/my_checkpoint_store_prefix",
            },
        },
        "validations_S3_store": {
            "class_name": "ValidationsStore",
            "store_backend": {
               "class_name": "TupleFilesystemStoreBackend",
                "base_directory":  "/opt/great_expectations/great_expectation_stores/my_validations_store_prefix",
            },
        },
        "evaluation_parameter_store": {"class_name": "EvaluationParameterStore"},
    },
    expectations_store_name="expectations_S3_store",
    validations_store_name="validations_S3_store",
    evaluation_parameter_store_name="evaluation_parameter_store",
    checkpoint_store_name="checkpoint_store",
    data_docs_sites={
        "s3_site": {
            "class_name": "SiteBuilder",
            "store_backend": {
                "class_name": "TupleFilesystemStoreBackend",
                "base_directory":  "/opt/great_expectations/great_expectation_stores/docs",
            },
            "site_index_builder": {
                "class_name": "DefaultSiteIndexBuilder",
                "show_cta_footer": True,
            },
        }
    },
    validation_operators={
        "action_list_operator": {
            "class_name": "ActionListValidationOperator",
            "action_list": [
                {
                    "name": "store_validation_result",
                    "action": {"class_name": "StoreValidationResultAction"},
                },
                {
                    "name": "store_evaluation_params",
                    "action": {"class_name": "StoreEvaluationParametersAction"},
                },
                {
                    "name": "update_data_docs",
                    "action": {"class_name": "UpdateDataDocsAction"},
                },
            ],
        }
    },
    anonymous_usage_statistics={
      "enabled": True
    }
)

context = BaseDataContext(project_config=data_context_config)

mysql_batch_request = BatchRequest(
    datasource_name="my_mysql_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="demo.test",
)

pg_batch_request = BatchRequest(
    datasource_name="my_postgresql_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="public.test",
)

validator = context.get_validator(batch_request=mysql_batch_request)

profiler = UserConfigurableProfiler(
    profile_dataset=validator,
    excluded_expectations=[
        "expect_column_quantile_values_to_be_between",
        "expect_column_mean_to_be_between",
    ],
)

expectation_suite_name = "compare_two_tables"
suite = profiler.build_suite()
context.save_expectation_suite(
    expectation_suite=suite, expectation_suite_name=expectation_suite_name
)

my_checkpoint_name = "comparison_checkpoint"

yaml_config = f"""
name: {my_checkpoint_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: "%Y%m%d-%H%M%S-my-run-name-template"
expectation_suite_name: {expectation_suite_name}
"""

context.add_checkpoint(**yaml.load(yaml_config))


results = context.run_checkpoint(
    checkpoint_name=my_checkpoint_name, batch_request=pg_batch_request
)