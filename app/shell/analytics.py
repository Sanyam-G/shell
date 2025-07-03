import csv
from collections import Counter

def show_analytics(log_file):
    try:
        with open(log_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            commands = [row[1] for row in reader]

        if not commands:
            print("No commands logged yet.")
            return

        print("--- Shell Usage Analytics ---")
        print("\nTop 10 Most Used Commands:")
        command_counts = Counter(commands)
        for command, count in command_counts.most_common(10):
            print(f"{command}: {count}")

    except FileNotFoundError:
        print("Log file not found.")
    except Exception as e:
        print(f"An error occurred during analysis: {e}")