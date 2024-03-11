"""
List structures all structures in the current AiiDA database

For information on how to run queries:
https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/query.html
https://aiida.readthedocs.io/projects/aiida-core/en/latest/topics/database.html
"""
from aiida.orm import QueryBuilder, StructureData
from aiida import load_profile

load_profile()

qb = QueryBuilder()
qb.append(StructureData, tag='all_structures', project=['*'])

print('{} structures in database:\n'.format(len(qb.all())) + 50*'-' + '\n' +
      'PK\tFormula\n' + 50*'-' )
for row in qb.all():
    structure = row[0]
    print('{}\t{}'.format(row[0].pk, row[0].get_formula()))
print(50*'-')

