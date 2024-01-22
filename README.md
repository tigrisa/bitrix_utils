# Add Task

## Description

"Add Task" is a command-line utility designed for automatically adding tasks to a task management system based on the type of the day. It determines if the day is a workday or a shortened workday, checks if there's already a task for that day, and adds a task if necessary.

You can automate this routine by adding a scheduler. For Windows, use the make_scheduler.bat file. For Linux, use the make_scheduler.sh file

The scheduler will execute `add_task --date today --randdelay 59` every day at 17:00

# Prerequisites

-   Create webhook and setup its permissions (Разработчикам - Другое - Входящий вебхук)

    This tool requires the following permissions:

    -   `task`
    -   `crm`

-   Create `credentials.json` with the following contents:
    ```json
    {
        "USER_ID": "userId",
        "SECRET": "token"
    }
    ```
-   Add this file to the root project directory
-   Install python, pip and pipx
    -   For win: pip install pipx
    -   For linux: sudo apt install pipx && pipx ensurepath
-   For the Linux scheduler your system must use systemd

## Installation

`pipx install .` in the root folder
or just run make_scheduler.\* file

## Usage

-   To add the scheduler to Windows, run the make_scheduler.bat file
-   To remove the scheduler in Windows, run the remove_scheduler.bat file
-   To add the scheduler to Linux, run the make_scheduler.sh file
-   To remove the scheduler in Linux, run the remove_scheduler.bat file
-   To run the script manually, use the following command:

```bash
add_task --date [DATE] --randdelay [MINUTES]
```

### Parameters

-   `--date` - The date for which the task needs to be added. Use 'today' for the current date. Format: YYYY-MM-DD.
-   `--randdelay` - The number of minutes for a random delay before executing the script. This is useful for preventing simultaneous execution when scheduled.

### Examples

Run the script to add a task for today with a 5-minute delay:

```bash
add_task --date today --randdelay 5
```

## Logging

The utility includes logging support to track actions and errors. Logs are saved in a root location and can be used for debugging and monitoring.

## Dependencies

-   pipx
-   Python 3.9+
-   Additional dependencies are listed in `pyproject.toml`.
