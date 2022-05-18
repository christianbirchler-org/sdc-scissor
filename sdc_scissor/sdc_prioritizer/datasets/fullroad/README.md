# Full Road Datasets

## Feature Extraction Process
We extract two type of full road features, the **general road characteristics** and the **road segment statistics**.
The general road characteristics are attributes that refer to the road as a whole (i.e., length of the road), or general road segment statistics calculated on on metrics involving all road segments as whole (i.e., minimum, mean, maximum angle, or length)

We first extract the path for the test scenario; with this information, we can obtain metrics and features from all relevant road segments and their details. 
The road segment details are used to compute the road segment statistic features

## Structure

### General Road Characteristics

| **Feature**     | **Derived From (AsFault Output)**  | **Description**                                        |**Type**|**Range**  | 
|-----------------|------------------------------------|--------------------------------------------------------|-------|------------|
| Direct Distance | Start, Goal                        | Euclidean distance between start and finish            | float | [0-490]    |
| Road Distance   | Path,Network/Nodes/RLanes          | Total length of the road                               | float | [56-3318]  |
| Num L Turns     | Path,Network/Nodes/RoadType        | Number of left turns on the test track                 | int   | [0-18]     |
| Num R Turns     | Path,Network/Nodes/RoadType        | Number of right turns on the test track                | int   | [0-17]     |
| Num Straight    | Path,Network/Nodes/RoadType        | Number of straight segments on the test track          | int   | [0-11]     |
| Total Angle     | Path,Network/Nodes/Angle           | Total angle turned in road segments on the test track  | int   | [105-6420] |
| Safety          | Execution/OOBS                     | Either safe or unsafe                                  | str   | safe/unsafe|

### Road Segment Statistics

| **Feature**          |**Derived From (AsFault Output)**| **Description**                                                          |**Type**| **Range**| 
|----------------------|--------------------------------|---------------------------------------------------------------------------|-------|-----------|
| Median Angle         | Path,Network/Nodes/Angle       | Median of angle turned in road segment on the test track                  | float | [30-330]  |
| Std Angle            | Path,Network/Nodes/Angle       | Standard deviation of angled turned in road segment on the test track     | int   | [0-150]   |
| Max Angle            | Path,Network/Nodes/Angle       | The maximum angle turned in road segment on the test track                | int   | [60-345]  |
| Min Angle            | Path,Network/Nodes/Angle       | The minimum angle turned in road segment on the test track                | int   | [15-285]  |
| Mean Angle           | Path,Network/Nodes/Angle       | The average angle turned in road segment turned on the test track         | float | [5-47]    |
| Median Pivot Off     | Path,Network/Nodes/Pivot Off   |  Median of radius of road segment on the test track                       | float | [7-47]    |
| Std Pivot Off        | Path,Network/Nodes/Pivot Off   | Standard deviation of radius of turned in road segment on the test track  | float | [0-23]    |
| Max Pivot Off        | Path,Network/Nodes/Pivot Off   | The maximum radius of road segment on the test track                      | int   | [7-47]    |
| Min Pivot Off        | Path,Network/Nodes/Pivot Off   | The minimum radius of road segment on the test track                      | int   | [2-47]    |
| Mean Pivot Off       | Path,Network/Nodes/Pivot Off   | The average radius of road segment turned on the test track               | float | [7-47]    |


### Timing
| **Feature**         | **Type** |
| ---                 | ---      |
| Start Time          | str      |
| End Time            | str      |
| Duration in seconds | float    |


## Labeling

Labeling was done with two diferent lane keeping AIs:
- [BeamNG.AI](https://wiki.beamng.com/Enabling_AI_Controlled_Vehicles#AI_Modes)
- Driver AI

| **Dataset** | **Total#** | **Safe#** | **Unsafe#** |
|-------------|------------|-----------|-------------|
| BNG 1       | 1178       | 866       | 312         |
| BNG 1.5     | 5638       | 3095      | 2543        |
| Driver AI   | 5630       | 4585      | 1045        |
