### example_0_no_quote

with following code:
```python
def example_0_no_quote():
    t1 = Table('customers')
    qry = Query.from_(t1).select(
        'name',
        'email',
        'address'
    )
    return qry.get_sql(quote_char='')

```

you will get following SQL:
```SQL
SELECT name,
       email,
       address
FROM customers;
```


### example_1_with_quote

with following code:
```python
def example_1_with_quote():
    t1 = Table('customers')
    qry = Query.from_(t1).select(
        'name',
        'email',
        'address'
    )
    return qry.get_sql(quote_char='`')

```

you will get following SQL:
```SQL
SELECT `name`,
       `email`,
       `address`
FROM `customers`;
```


### example_2_groupby

with following code:
```python
def example_2_groupby():
    e = Table('employee')
    d = Table('department')
    qry = Query.from_(d).join(e)
    qry = Query.from_(d).left_join(e).on(d.emp_id==e.emp_id).select(
        d.name,
        e.name,
        Max(e.salary).as_('top_salary')
    ).groupby(1, 2).orderby(3, order=Order.desc)
    return qry.get_sql(quote_char='')

```

you will get following SQL:
```SQL
SELECT department.name,
       employee.name,
       MAX(employee.salary) top_salary
FROM department
LEFT JOIN employee ON department.emp_id=employee.emp_id
GROUP BY 1,
         2
ORDER BY 3 DESC;
```


### example_3_rank

with following code:
```python
def example_3_rank():
    e = Table('employee')
    d = Table('department')
    qry = Query.from_(d).join(e)
    qry = Query.from_(d).left_join(e).on(d.emp_id==e.emp_id).select(
        d.name,
        e.name,
        e.salary,
        Rank().over(d.name).orderby(e.salary, order=Order.desc).as_('sal_rank')
    ).orderby(1, 4)
    return qry.get_sql(quote_char='')

```

you will get following SQL:
```SQL
SELECT department.name,
       employee.name,
       employee.salary,
       RANK() OVER(PARTITION BY department.name
                   ORDER BY employee.salary DESC) sal_rank
FROM department
LEFT JOIN employee ON department.emp_id=employee.emp_id
ORDER BY 1,
         4;
```


### example_4_custom_function

with following code:
```python
def example_4_custom_function():
    from pypika.functions import Function

    class MyFunction(Function):
        def __init__(self, *args, **kwargs):
            super(MyFunction, self).__init__(
                'MY_FUN', *args, **kwargs)

    t = Table('customer_info')
    qry = Query.from_(t).select(t.usr_id, MyFunction(t.a, t.b))
    return qry.get_sql(quote_char='')

```

you will get following SQL:
```SQL
SELECT usr_id,
       MY_FUN(a, b)
FROM customer_info;
```


### example_5_schema_and_config_driven

with following code:
```python
def example_5_schema_and_config_driven():
    '''
    If I have a list of tables to land from somewhere
    and I want to apply a ref_dt=2021-01-01 to which ever has ref_dt field,
    and I want to apply a usr_part=123 to which ever has a usr_part,
    and I want to join all tables when it has user_id field.
    '''
    REF_DT = '2021-01-01'
    USR_PART = '123'

    join_fields = ['usr_id']
    accepted_fields = ['a1', 'a2', 'b3', 'b4', 'c1', 'c4']

    tables = [
        {
            'name': 'A',
            'columns': ['ref_dt', 'usr_part', 'usr_id', 'a1', 'a2', 'a3', 'a4'],
        },
        {
            'name': 'B',
            'columns': ['usr_id', 'b1', 'b2', 'b3', 'b4'],
        },
        {
            'name': 'C',
            'columns': ['ref_dt', 'usr_part', 'usr_id', 'c1', 'c2', 'c3', 'c4'],
        },
    ]

    views = []
    qry = Query()
    for t in tables:
        the_table = Table(t['name'])
        fields = []
        alias_name = f"v_{t['name']}"
        alias_qry = AliasedQuery(alias_name)

        for c in t['columns']:
            if c in accepted_fields or c in join_fields:
                fields.append(Field(c))
        views.append({
            'alias_name': alias_name,
            'alias_qry': alias_qry,
            'fields': fields
        })
        sub_qry = Query.from_(the_table).select(*fields)
        if 'ref_dt' in t['columns']:
            sub_qry = sub_qry.where(the_table.ref_dt == REF_DT)
        if 'usr_part' in t['columns']:
            sub_qry = sub_qry.where(the_table.usr_part == USR_PART)

        qry = qry.with_(sub_qry, alias_name)

    prev_v = views.pop(0)
    # fields = [f.name for f in prev_v['fields']]
    fields = [getattr(prev_v['alias_qry'], f.name) for f in prev_v['fields']]
    qry = qry.from_(prev_v['alias_qry']).select(*fields)
    seen_fields = [f.name for f in prev_v['fields']]

    for v in views:
        alias_qry = v['alias_qry']
        # fields = [f.name for f in v['fields'] if f.name not in seen_fields]
        fields = [getattr(alias_qry, f.name) for f in v['fields'] if f.name not in seen_fields]
        seen_fields = seen_fields + fields
        qry = qry.join(alias_qry).on(
            prev_v['alias_qry'].usr_id == alias_qry.usr_id).select(*fields)
        prev_v = v


    return qry.get_sql(quote_char='')

```

you will get following SQL:
```SQL
WITH v_A AS
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
JOIN v_C ON v_B.usr_id=v_C.usr_id;
```


