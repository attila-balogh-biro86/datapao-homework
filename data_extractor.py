import csv
from datetime import datetime, timedelta
from collections import defaultdict


# Function to parse the CSV file
def parse_csv(file_path):
    data = defaultdict(list)  # Define the date-time range
    start_time = datetime(2023, 2, 1, 00, 0, 0)
    end_time = datetime(2023, 2, 28, 23, 59, 59)
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row['user_id']
            event = row['event_type']
            timestamp = datetime.strptime(row['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if start_time <= timestamp <= end_time:
                data[user_id].append((event, timestamp))
    return data


# Function to calculate the time spent and number of days in the office
def calculate_time_and_days(data):
    results_without_rank = []
    results_with_rank = []
    for user_id, events in data.items():
        events.sort(key=lambda x: x[1])
        total_time = timedelta()
        days_present = set()
        in_time = None
        for event, timestamp in events:
            if event == 'GATE_IN':
                days_present.add(timestamp.date())
                in_time = timestamp
            elif event == 'GATE_OUT' and in_time:
                total_time += timestamp - in_time
                in_time = None
        total_hours = total_time.total_seconds() / 3600
        num_days = len(days_present)
        avg_per_day = total_hours / num_days if num_days else 0
        results_without_rank.append((user_id, total_hours, num_days, avg_per_day))
    results_without_rank.sort(key=lambda x: x[3], reverse=True)
    for rank, result in enumerate(results_without_rank, 1):
        result += (rank,)
        results_with_rank.append(result)
    return results_with_rank


# Function to calculate the longest work session
def calculate_longest_session(data):
    results = []
    max_record = None
    results_single_result = []
    for user_id, events in data.items():
        events.sort(key=lambda x: x[1])
        longest_session = timedelta()
        in_time = None
        for event, timestamp in events:
            if event == 'GATE_IN':
                if in_time:
                    session_time = timestamp - in_time
                    if session_time > timedelta(hours=2):
                        in_time = timestamp
                    else:
                        in_time = timestamp
                else:
                    in_time = timestamp
            elif event == 'GATE_OUT' and in_time:
                session_time = timestamp - in_time
                if session_time > longest_session:
                    longest_session = session_time
                in_time = None
        results.append((user_id, longest_session.total_seconds() / 3600))
    max_record = max(results, key=lambda x: x[1])
    results_single_result.append(max_record)
    return results_single_result


# Function to write the results to CSV
def write_to_csv(file_path, headers, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


# Main function
def main():
    input_file = 'datapao_homework_2023.csv'
    data = parse_csv(input_file)

    # Calculate time and days
    time_and_days_results = calculate_time_and_days(data)
    write_to_csv('output/first.csv', ['user_id', 'time', 'days', 'average_per_day', 'rank'], time_and_days_results)

    # Calculate longest session
    longest_session_results = calculate_longest_session(data)
    write_to_csv('output/second.csv', ['user_id', 'session_length'], longest_session_results)


if __name__ == '__main__':
    main()
