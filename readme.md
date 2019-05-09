# APP_KIRK (Keeping Information Replicated Kontinuously)

## Background.

### Current Challenges
DataBC's currently uses FME and FME Server as the backbone for most of our 
replications.  FME product uses individual scripts to perform replications.  
At DataBC we try to maintain a single source / destination for each 
replication script.  This has led to the current situation where we
manage more than 400 individual replications scripts.

From a DataBC perspective FME's advertised strength, of providing a visual programming
UI is also its biggest weakness.  While the ability to create complex scripts 
without having to write code can save time, the flip side is maintenance costs can
be significant.

Currently we are in the process of upgrading the SDE / Geodatabase software used
in the database.  The upgrade means that the 'reader' / 'writers' in our replication
scripts need to be updated.  At a ballpark cost of 20 minutes a script multiplied by 
more than 400 the update costs are significant.

### How KIRK will help
While we have many long term plans in terms of how Kirk will evolve, initially it 
will accomplish the following:
- Replication configurations will get stored in a database as oppose to inside 
  individual replication scripts.  This will give us better transparency and reporting
  capacity in terms of what is being replicated when.
- Kirk will re-use individual FMW's.  Most of our replications do not require the 
  full suite of tools available in the FME product.  In fact most replication are 
  copies of data from one place to another, with no transformations in between.
- Re-using FMW's will reduce the number of fmw's that need to get edited when we 
  implement new features like incremental replications or changes to readers / 
  writers.   

 
## Kirk Description:

**KIRK** moves away from conventional [FME](https://www.safe.com/) replication 
configuration model where replication metadata is stored in individual scripts.

Typical Replication metadata is made up of:
   - Source dataset / table
   - Destination dataset / table
   - fieldmapping between source and destination tables
   - Data Transformations 

APP_KIRK re-uses FMW scripts populating them at run time with parameters that 
get retrieved from a database through a rest api.  The approach makes replication 
information more transparent as replication metadata is stored in plain database 
tables as oppose to embedded in individual FME scripts.  

Re-using FMW's also makes it much easier for us to switch to different reader / 
writers.  Also opens up the possibility to complete replications using different 
replications tools.  Currently FME is the only known tool available for writing 
geometries that can be consumed by both ESRI SDE and Oracle SDO.

APP_KIRK is currently under development.

# License
Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
