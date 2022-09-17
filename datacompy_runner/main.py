import pandas as pd
import datacompy
from loguru import logger


def run_datacompy():
    source = pd.read_sql_table("test", "mysql+pymysql://root:example@source/demo")
    dest = pd.read_sql_table("test", "postgresql://postgres:example@destination/postgres")
    results = datacompy.Compare(source,dest, join_columns="id")
    logger.info(results.report())
    return results.matches()


if __name__ == "__main__":
    run_datacompy()