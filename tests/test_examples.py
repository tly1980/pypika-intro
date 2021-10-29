from examples import *


def test_all(snapshot):
    funs = [
        example_0_no_quote,
        example_1_with_quote,
        example_2_groupby,
        example_3_rank,
        example_4_custom_function,
        example_5_schema_and_config_driven
    ]

    for f in funs:
       func_name, _, sql = get_src_and_sql(f)
       snapshot.assert_match(sql, func_name)
