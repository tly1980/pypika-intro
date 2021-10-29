# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all example_0_no_quote'] = '''SELECT name,
       email,
       address
FROM customers;'''

snapshots['test_all example_1_with_quote'] = '''SELECT `name`,
       `email`,
       `address`
FROM `customers`;'''

snapshots['test_all example_2_groupby'] = '''SELECT department.name,
       employee.name,
       MAX(employee.salary) top_salary
FROM department
LEFT JOIN employee ON department.emp_id=employee.emp_id
GROUP BY 1,
         2
ORDER BY 3 DESC;'''

snapshots['test_all example_3_rank'] = '''SELECT department.name,
       employee.name,
       employee.salary,
       RANK() OVER(PARTITION BY department.name
                   ORDER BY employee.salary DESC) sal_rank
FROM department
LEFT JOIN employee ON department.emp_id=employee.emp_id
ORDER BY 1,
         4;'''

snapshots['test_all example_4_custom_function'] = '''SELECT usr_id,
       MY_FUN(a, b)
FROM customer_info;'''

snapshots['test_all example_5_schema_and_config_driven'] = '''WITH v_A AS
  (SELECT usr_id,
          a1,
          a2
   FROM A
   WHERE ref_dt='2021-01-01'
     AND usr_part='123'),
     v_B AS
  (SELECT usr_id,
          b3,
          b4
   FROM B),
     v_C AS
  (SELECT usr_id,
          c1,
          c4
   FROM C
   WHERE ref_dt='2021-01-01'
     AND usr_part='123')
SELECT v_A.usr_id,
       v_A.a1,
       v_A.a2,
       v_B.b3,
       v_B.b4
FROM v_A
JOIN v_B ON v_A.usr_id=v_B.usr_id
JOIN v_C ON v_B.usr_id=v_C.usr_id;'''
