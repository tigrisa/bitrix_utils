import subprocess
import datetime
import argparse


from add_task.logger import Logger

# logger init
logger = Logger().get_logger()
logger.info("The logger has been successfully initialized in add_task.py")


def wait(max_minutes):
    import time
    import random

    # Generate a random number of minutes between 0 and max_minutes
    random_minutes = random.randint(0, int(max_minutes))
    logger.info(f"Pause for {random_minutes} minutes...")

    # Convert to seconds and sleep
    time.sleep(random_minutes * 60)


def check_if_date_in_the_future(args):
    today = datetime.datetime.now().date()
    # Convert to data object
    try:
        input_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        logger.error(f"Invalid date format: {args.date}. Expected format: YYYY-MM-DD.")
        return True

    # Check if date from args is in the future
    if input_date > today:
        logger.error(f"The provided date {args.date} is in the future.")
        return True

    return False


def run_script(script, args):
    """Runs the script with the specified args and returns its output."""
    try:
        result = subprocess.run(
            [script] + args, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running script {script}: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="date in format YYYY-MM-DD or 'today'")
    parser.add_argument(
        "--randdelay", help="quantity of minutes while script will sleep"
    )
    parser.add_argument("--taskid", default="63718", type=str, help="bitrix taskId")

    args = parser.parse_args()

    if args.date is not None:
        if args.date == "today":
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            if not check_if_date_in_the_future(args):
                date_str = args.date
            else:
                return 1
    else:
        logger.error("No date provided.")
        return 1

    if args.randdelay is not None:
        wait(args.randdelay)

    # Run the day_checker and get a day type
    day_type = run_script("day_checker", ["--date", date_str])

    if day_type in ["workday", "shortened_workday"]:
        # Check if the record for today already exists
        last_records = run_script("tasks", ["--list", "10", "--taskid", args.taskid])

        if date_str not in last_records:
            hours = "8" if day_type == "workday" else "7"
            # Add a task for today
            at_time = datetime.datetime.now().strftime("%H:%M:%S")
            logger.info(f"Adding a task for {date_str} at {at_time} for {hours} hours.")
            run_script(
                "tasks",
                [
                    "--date",
                    date_str,
                    "--time",
                    hours,
                    "--attime",
                    at_time,
                    "--taskid",
                    args.taskid,
                ],
            )


if __name__ == "__main__":
    main()
