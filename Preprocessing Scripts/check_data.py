
import csv
import math
from pathlib import Path

# Paths
root = Path(__file__).resolve().parent.parent
processed = root / "Data" / "Processed Data"
participants = [46, 47, 48, 49, 50, 51, 52, 53, 55, 56] # participant ID numbers


# Go through each participant and their recording sessions
for participant in participants:
    person_folder = processed / str(participant)

    for session in sorted(person_folder.iterdir()):
        if not session.is_dir():
            continue

        print(f"\nParticipant {participant} - {session.name}")

        # Check both motion and eye tracking files
        for filename in ["vr-controllers.csv", "eye-tracking.csv"]:
            file_path = session / filename

            rows = 0
            missing = 0
            invalid = 0
            duplicates = 0
            backwards = 0
            gaps = 0

            previous_time = None

            # Read the CSV file
            with file_path.open(newline="", encoding="utf-8-sig") as infile:
                reader = csv.DictReader(infile)

                for row in reader:
                    rows += 1

                    # Check each sensor measurement
                    for column, value in row.items():

                        # Skip timestamps for the sensor value checks
                        if column in ["timestamp", "delta_time_ms"]:
                            continue

                        # Check for empty measurements
                        if value is None or value.strip() == "":
                            missing += 1
                            continue

                        # Check for values that are not valid numbers
                        try:
                            number = float(value)
                            if not math.isfinite(number):
                                invalid += 1
                        except ValueError:
                            invalid += 1

                    # Check elapsed timestamps
                    try:
                        current_time = float(row["delta_time_ms"])
                    except (ValueError, TypeError):
                        invalid += 1
                        continue

                    if not math.isfinite(current_time):
                        invalid += 1
                        continue

                    if previous_time is not None:
                        difference = current_time - previous_time

                        if difference == 0:
                            duplicates += 1
                        elif difference < 0:
                            backwards += 1
                        elif difference > 1000:
                            gaps += 1

                    previous_time = current_time

            # Print results for this file
            print(f"  {filename}")
            print(f"    Rows: {rows}")
            print(f"    Missing sensor values: {missing}")
            print(f"    Invalid values: {invalid}")
            print(f"    Duplicate timestamps: {duplicates}")
            print(f"    Backward timestamps: {backwards}")
            print(f"    Gaps over 1 second: {gaps}")
