"""
    org_check.py -- Given a list of deptids, check them against VIVO.
    Report high level missing deptids.  Add lower level deptids to
    existing UF orgs.

    Version 0.1 MC 2014-08-02
    --  Initial version.  Works as expected.
    Version 0.2 MC 2015-09-10
    -- Upgrading to VIVO-ISF
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2015 (c) Michael Conlon"
__license__ = "New BSD License"
__version__ = "0.2"

from vivofoundation import make_deptid_dictionary
from vivofoundation import read_csv
from vivofoundation import assert_data_property
from vivofoundation import rdf_header
from vivofoundation import rdf_footer
from datetime import datetime

# Helper Functions


def skip_deptid(deptid):
    """
    For patterns in a skip list, check deptids to see if deptids should
    be skipped
    """
    skip_list = \
        [
            "^[^0-9]",  # skip the alphabetic deptid
            "^74",  # institutional activities funds
            "^75",  # construction and renovation funds
            "^76",  # institutional activities funds
            "^1831",  # legacy ?
            "^1832",  # legacy ?
            "^1940",  # accounting only
            "^1922",  # accounting only
            "36000000",  # place holder for COM/PHHP joint programs
            "60990000",  # financial reporting only
            "^6121",
            "^6122",
            "^6123",
            "^6124",  # four financial buckets in business affairs
            "64990000",  # financial reporting only
            "27990000",  # financial reporting only
            "95000000",  # place holder for DSO top level
            "^9536"  # accounting only?
        ]
    import re
    skip = False
    for pattern_string in skip_list:
        pattern = re.compile(pattern_string)
        if pattern.search(deptid) is not None:
            skip = True
            break
    return skip

print datetime.now(), "Start"

# Prepare UF deptids

uf_data = read_csv("deptid_list_20150910.csv")
uf_deptids = {}
for row in uf_data.values():
    uf_deptids[row['dept_id']] = row['deptName']
print datetime.now(), "UF has ", len(uf_deptids), "deptids"

# Gather VIVO deptids

vivo = make_deptid_dictionary()
print datetime.now(), "VIVO has ", len(vivo), "deptids"

# Check each deptid

missing_l4 = {}
total = 0
found = 0
skip = 0
needl2 = 0
needl4 = 0
l2add = 0
l4add = 0
l6add = 0
l4miss = 0
ardf = rdf_header()

for deptid in sorted(uf_deptids):
    name = uf_deptids[deptid]
    total = total + 1
    if deptid in vivo:
        found = found + 1
    elif skip_deptid(deptid):
        skip = skip + 1
    elif name.startswith('HN'):  # Harn does not follow the structure
        ardf = ardf + assert_data_property(vivo['57800000'],
            "ufVivo:deptID", deptid)
        print datetime.now(), deptid, "added to Harn"
        l4add = l4add +1
    elif deptid[0:2] in ['05', '06', '07', '08', '35', '47', '52', '63',\
            '67', '69', '72', '81', '82', '83']: # all rolled up to L2
        level2 = deptid[0:2]+'000000'
        if level2 in vivo:
            ardf = ardf + assert_data_property(vivo[level2],
                "ufVivo:deptID", deptid)
            print datetime.now(), deptid, "added to L2", level2
            l2add = l2add + 1
        else:
            print datetime.now(), "L2", level2, "not found for", deptid,\
                  name, "Please add."
            needl2 = needl2 + 1
    elif deptid.endswith('0000'):
        print datetime.now(), deptid, name, \
                  "not found in VIVO.  Please add."
        missing_l4[deptid] = name
        needl4 = needl4 + 1
    else:
        level4 = deptid[0:4]+'0000'
        if level4 in vivo:
            if deptid.endswith('00'):
                ardf = ardf + assert_data_property(vivo[level4],
                    "ufVivo:deptID", deptid)
                print datetime.now(), deptid, "added to L4", level4
                l4add = l4add + 1
            else:
                level6 = deptid[0:6]+'00'
                if level6 in vivo:
                    ardf = ardf + assert_data_property(vivo[level6],
                        "ufVivo:deptID", deptid)
                    print datetime.now(), deptid, "added to L6", level6
                    l6add = l6add + 1
                else:
                    ardf = ardf + assert_data_property(vivo[level4],
                        "ufVivo:deptID", deptid)
                    print datetime.now(), deptid, "added to L4", level4
                    l4add = l4add + 1
        else:
            print datetime.now(), level4, "not found for", deptid, name,\
                "Please add."
            l4miss = l4miss + 1

# write out the RDF to add deptids to existing organizations

ardf = ardf + rdf_footer()
rdf_file = open("deptid_add.rdf", "w")
print >>rdf_file, ardf
rdf_file.close()
print datetime.now(), "Missing L4"
for deptid in sorted(missing_l4):
    name = missing_l4[deptid]
    print datetime.now(), deptid, name
print datetime.now(), total, "deptids processed"
print datetime.now(), skip, "deptids in exceptions. Nothing to do."
print datetime.now(), found, "deptids found in VIVO. Nothing to do."
print datetime.now(), needl2, "L2 needed.  Please add to VIVO or exceptions"
print datetime.now(), needl4, "L4 needed.  Please add to VIVO or exceptions"
print datetime.now(), l4miss, "deptids can not be added. Missing L4"
print datetime.now(), l2add, "deptids added to existing L2"
print datetime.now(), l4add, "deptids added to existing L4"
print datetime.now(), l6add, "deptids added to existing L6"
print datetime.now(), skip+found+needl2+needl4+l4miss+l2add+l4add+l6add, \
    "deptids accounted for by actions"
print datetime.now(), "Finish"
