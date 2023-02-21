import csv
import os

selected_rows = []
remove = False

final_csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BeamNG_RF_1_5_selected.csv")
with open(final_csv_dir, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[19] == "safe":
            selected_rows.append(row)
        else:
            if not remove:
                selected_rows.append(row)

            remove = not remove

print(len(selected_rows))

final_csv_file = open(final_csv_dir, "wb")
final_csv_writer = csv.writer(final_csv_file)

fields = [
    "direct_distance",
    "road_distance",
    "num_l_turns",
    "num_r_turns",
    "num_straights",
    "median_angle",
    "total_angle",
    "mean_angle",
    "std_angle",
    "max_angle",
    "min_angle",
    "median_pivot_off",
    "mean_pivot_off",
    "std_pivot_off",
    "max_pivot_off",
    "min_pivot_off",
    "start_time",
    "end_time",
    "duration_seconds",
    "safety",
]
final_csv_writer.writerow(fields)

for row in selected_rows:
    print(row)
    final_csv_writer.writerow(row)
