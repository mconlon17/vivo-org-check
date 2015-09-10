# Check VIVO Orgs

_This is a UF specific repository_

At UF, organizations have eight digit department identifiers knows as "deptids".  People are appointed
to deptids.  in UF VIVO, an ontology extension records a person's deptid as home department, and 
an inverse property of the home department records the associations with people.

When adding people to VIVO, HR data indicates the home department via deptid.  The deptid must be found in
in VIVO, otherwise the person can not be added.'

Deptids have structure, often (but not always) indicating the level of the organization at the university.

    aabbccdd
	
* aa is a two digit number indicating the highest level, college or vice president's office.  16 is the College of 
Liberal Arts and Sciences.  29 is the College of Medicine.  01 is the Office of th President.  
* bb is the highest level sub units, often academic departments, within the higher level unit.  2968 is the Clinical
and Translational Science Institute.
* cc is the highest level sub units of the aabb unit.  These are sometimes called Divisions, but the practice is uneven.  
In some cases the word "Division" is used for a higher level unit.  In other cases, the aabbcc level units are
called programs, or centers, or many other terms.
* dd is the lowest level organization in a deptid.  This level is rarely used.

Most faculty are appointed at the aabb level.  It is rare to see people appointed at the aabbccdd level.

## Checking the deptids

A list of deptids is checked against a list of deptids in VIVO.  If a deptid is missing from VIVO it can be added
to an existing organization by "rolling" up to the existing 6 or 4 level org.  

## Adding deptids to an existing org

Many orgs in VIVO have multiple deptids associated with them.  VIVO does not attempt to model every 
deptid as an org.  Many departments use deptids as an accounting convenience with no particular 
association with organizational structure.

When a deptid is not found in VIVO, it casn be added to the 6 level org (aabbcc00) if it exists, or to
the four level org (aabb0000) if it does not, and the four level org exists.  

Adding a deptid to an exsting org in sures that people will be associated with the existing org.

## Adding new orgs to VIVO

At the lower levels of the UF org structure, it is safe to assume that aabbccdd is a sub unit of aabbcc00.
At the highest level, the dept id contains no information of parent organization. 

When a deptid is missing from VIVO, and is at aa or aabb level, it must be reported as an exception and added
manually after review of administrative documents -- memos, web sites -- indicating, the name, type and
location in the hierarchy of the new organization at UF.

org_check never adds orgs to VIVO.  This is always done manually.

## Remodeling an org

Occasionally, VIVO has rolled up sub structure where a unit would prefer to show the substructure.  It is 
a simple matter 
to work with the unit to determine the amount of sub structure they wish to have represented, create
the appropriate sub units, and assign them their deptids.

## Impact on Person Ingest

The person ingest expects to find a person's deptid in VIVO.  When it does not, it produces a line in the
exception report for the ingest.  

If the deptid of the person does not match the current home department association in VIVO, the person
is moved to the new deptid.


