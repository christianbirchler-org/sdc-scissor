# SWAT test generator #

The module "road_gen" generates the commands to build the road such as "go straight n meters",
"turn left n degrees", "turn right n degrees" and the module car_road executes them to produce the
road points. Swat_generator is the main module. To execute the tests run the competition.py file.
For example, using the mock executor:
python3 competition.py \
        --visualize-tests \
        --time-budget 100 \
        --executor mock \
        --map-size 200 \
        --module-name swat_gen.swat_generator \
        --class-name SwatTestGenerator


[Requirements](requirements-37.txt): contains the list of the required packages.


## Contacts ##

Dmytro Humeniuk  - dmytro.humeniuk@polymtl.ca

