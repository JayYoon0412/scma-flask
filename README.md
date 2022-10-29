# Project: SuperCool Mini Amazon Web
Mini Web Amazon running on Flask with DB as PostgreSQL

## Team Members:
###### Jay: responsible for Products client and server </br>
brief updates from Milestone 1: </br>
- Translated entity and tables onto ERD diagram
- Updated create.py to reflect changes to entity attributes and many-to-one relationships
- Updated generate.py for populating larger scale dummy database using Faker
</br>

###### Minwoo: responsible for Cart client and server </br>
brief updates from Milestone 1: </br>
- Made contributions to constructing relevant logic for E/R design
- Contributed to translating E/R diagrams to tables
- Created and organized GitLab repository of the project
</br>

###### Qihan: responsible for Social client and server </br>
brief updates from Milestone 1: </br>
- Contributed to datatables specification, defining assumptions and constraints
- Contributed to page-by-page design
- Contributed to user flow

</br>

###### Yanpeng: responsible for Seller client and server </br>
brief updates from Milestone 1: </br>
- Contributed to E/R design, setting up entity primary key and relations
- Contributed to page design
</br>

###### Michael: responsible for User client and server </br>
brief updates from Milestone 1: </br>
- Contributed to E/R design, removing any redundancies in design
- Contributed to page-by-page design, and user flow focusing on content
</br>

## Running Sample Database
1. install dependencies (run on environment) </br>
```
source env/bin/activate
```
2. generate appropriate dummy data using Faker by running gen.py </br>
```
cd db/generated
python gen.py
```
3. populate and set up sample amazon psql database </br>
```
cd super-cool-mini-amazon-project
./setup.sh
```
4. to see sample database, open amazon db on terminal </br>
```
cd
psql amazon
```
to see all created tables:
```
\dt
```
to see data in specific table (populated with dummy data for now):
```
TABLE (tablename);
```
5. to change number of dummy data generated (number of instances of each entity), edit num_(entity_name) variable located in gen.py