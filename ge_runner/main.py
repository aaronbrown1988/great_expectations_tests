import great_expectations as ge
from great_expectations.core.batch import BatchRequest
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)

context = ge.get_context()

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