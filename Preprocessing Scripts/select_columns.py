import csv
from pathlib import Path

# Hardcoded paths. Changing folder tree could mess this up so be careful.
root = Path(__file__).resolve().parent.parent
original = root / "Data" / "Original Data"
processed = root / "Data" / "Processed Data"
participants = [46, 47, 48, 49, 50, 51, 52, 53, 55, 56] # participant ID numbers


### COLUMNS THAT WE WANT TO KEEP ###

# Headset and controller position and rotation data
motion_columns = ["timestamp", "delta_time_ms"]
for device in ["hmd", "left_controller", "right_controller"]:
    for axis in "xyz":
        motion_columns.append(f"{device}_pos_{axis}")
    for axis in "wxyz":
        motion_columns.append(f"{device}_rot_{axis}")

# Eye gaze direction data
eye_columns = ["timestamp", "delta_time_ms"]
for axis in "xyz":
    eye_columns.append(f"gaze_direction_combined_local_{axis}")


### ITERATE THROUGH AND SELECT DATA ###

# Go through each participant and their two recording sessions
for participant in participants:
    person_folder = original / str(participant)
    for session in sorted(person_folder.iterdir()):
        if not session.is_dir():
            continue

        # Process both CSV files from each session
        for filename, columns in [
            ("vr-controllers.csv", motion_columns),
            ("eye-tracking.csv", eye_columns),
        ]:
            source = session / filename
            destination = processed / str(participant) / session.name / filename

            # Create the output folders if they do not exist
            destination.parent.mkdir(parents=True, exist_ok=True)

            # Read the original CSV file
            with source.open(newline="", encoding="utf-8-sig") as infile:
                reader = csv.DictReader(infile)

                # Check that all the columns we want exist
                missing = [column for column in columns if column not in reader.fieldnames]
                if missing:
                    raise ValueError(f"Missing columns in {source}: {missing}")

                # Create or overwrite the processed CSV file
                with destination.open("w", newline="") as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=columns)
                    writer.writeheader()

                    start_time = None

                    # Read rows until five minutes have passed
                    for row in reader:
                        time_ms = float(row["delta_time_ms"])

                        if start_time is None:
                            start_time = time_ms

                        if time_ms - start_time > 300000:  # first 5 minutes
                            break

                        # Copy only the selected columns into the new file
                        writer.writerow({column: row[column] for column in columns})

            print(f"Created: {destination}")
