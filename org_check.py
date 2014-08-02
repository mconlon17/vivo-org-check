"""
    org_check.py -- Given a list of deptids, check them against VIVO.
    Report high level missign deptids.  Add lowe level deptids to
    existing UF orgs.

    Version 0.1 MC 2014-08-02
    --  Initial version.  Untested

    To do:
    --  update for VIVO-ISF
    --  update for tools 2.0
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import make_deptid_dictionary
from vivotools import read_csv
from vivotools import add_data_property
from vivotools import rdf_header
from vivotools import rdf_footer
from datetime import datetime
from operator import itemgetter

print datetime.now(), "Start"

# Prepare UF depids

uf_data = read_csv("deptids.txt")
uf_deptids = {}
for row_number, row in uf_data:
    uf_deptids[row['dept_id']] = row['deptName']

# Gather VIVO deptds

vivo = make_deptid_dictionary()

# Check each deptid

found = 0
ardf = rdf_header()

for deptid, name in sort(uf_deptids.items(), key=itemgetter(1)):
    if deptid in vivo:
        found = found + 1
    elif deptid.endswith('0000'):
        print deptid, name, "not found in VIVO.  Please add."
    else:
        level4 = deptid[0:4]+'0000'
        if level4 in vivo:
            if deptid.endswith('00'):
                ardf = ardf + add_data_property(vivo[level4],
                    "ufVivo:deptid", deptid)
                print deptid, "added to ", level4
            else:
                level6 = deptid[0:6]
                if level6 in vivo:
                    ardf = ardf + add_data_property(vivo[level6],
                        "ufVivo:deptid", deptid)
                    print deptid, "added to ", level6
                else:
                    ardf = ardf + add_data_property(vivo[level4],
                        "ufVivo:deptid", deptid)
                    print deptid, "added to ", level4
        else:
            print level4, "not found for", deptid, name, "Please add."

# write out the RDF to add deptids to existing orgs

ardf = ardf + rdf_footer()
rdf_file = open("deptid_add.rdf", "w")
print >>rdf_file, ardf
rdf_file.cose()
print found, "deptids found in VIVO"
print datetime.now(), "Finish"
