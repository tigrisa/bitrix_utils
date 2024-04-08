from odf.opendocument import load as ods_load
from odf.table import Table, TableRow, TableCell
from odf import teletype
from odf.style import Style
import datetime
import argparse

import os


from add_task.logger import Logger

# logger init
logger = Logger().get_logger()
logger.info("The logger has been successfully initialized in day_checker.py")


def load_ODS(file_path):
    # Load the ODS file
    doc = None
    try:
        doc = ods_load(file_path)
        logger.info(f"The file {file_path} is successfully loaded.")
    except FileNotFoundError:
        logger.error(f"The file {file_path} is not found.")
    except PermissionError:
        logger.error(f"You don't have rights for reading the file {file_path}.")
    except Exception as e:
        logger.error(f"An error has occurred while loading the file: {e}")

    return doc


def calc_repeated_offset(cells, col_pos):
    offset = 0
    i = 0
    while i < col_pos:
        r_cols = cells[i].getAttribute("numbercolumnsrepeated")
        if r_cols is not None:
            offset += int(r_cols) - 1
            col_pos -= offset
        i += 1
    return offset


def get_cell(sheet, col_pos, row_pos):
    rows = sheet.getElementsByType(TableRow)
    if row_pos < len(rows):
        row = rows[row_pos]
        cells = row.getElementsByType(TableCell)
        # calc offset for repeated columns
        col_pos = col_pos - calc_repeated_offset(cells, col_pos)
        if col_pos >= 0 and col_pos < len(cells):
            return cells[col_pos]

    return None


def calc_month_pos(date_obj):
    x = (date_obj.month - 1) % 3  # mod
    y = (date_obj.month - 1) // 3  # div
    return (1 + x * 9, 3 + y * 9)


def find_day_pos(sheet, date_obj):
    col, row = calc_month_pos(date_obj)
    col = col + date_obj.weekday()

    for i in range(0, 5):
        day_cell = get_cell(sheet, col, row)
        day = teletype.extractText(day_cell)
        if day != "" and int(day) == date_obj.day:
            return col, row
        row = row + 1

    return None


from enum import Enum


class DayType(Enum):
    workday = 0
    day_off = 1
    shortened_workday = 2
    vacation_day = 3
    unknown_day = 4


def determine_day_type_by_color(color):
    color_to_day_type = {
        "#ffa6a6": DayType.day_off,  # light red 2
        "#b4c7dc": DayType.shortened_workday,  # light blue 2
        "#77bc65": DayType.vacation_day,  # light green 2
    }

    return color_to_day_type.get(color, "unknown_day")


def get_day_type(doc, cell):
    # Retrieve the style of the cell
    cell_style_name = cell.getAttribute("stylename")
    # Search for the style within the document's automatic styles
    styles = doc.automaticstyles.getElementsByType(Style)
    cell_style = None
    for style in styles:
        # If the style name matches, store the style object
        if style.getAttribute("name") == cell_style_name:
            cell_style = style
            break
    # If the style is found, extract the background color
    if cell_style:
        for child_nodes in cell_style.childNodes:
            background_color = child_nodes.getAttribute("backgroundcolor")
            if background_color:
                return determine_day_type_by_color(background_color)

    return DayType.workday


# Function to check the day type from an ODS file
def check_day_type_ods(file_path, date_obj):

    doc = load_ODS(file_path)
    # a first table in the ODS document
    sheet = doc.spreadsheet.getElementsByType(Table)[0]
    if sheet:
        pos = find_day_pos(sheet, date_obj)
        if pos:
            return get_day_type(doc, get_cell(sheet, pos[0], pos[1]))

    return DayType.unknown_day


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="date in format YYYY-MM-DD or 'today'")
    args = parser.parse_args()

    if args.date is not None:
        if args.date == "today":
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            date_str = args.date
    else:
        # If there is an error parsing the date, return unknown_day for error
        print(DayType.unknown_day.name)
        return 1

    # Relative path to the file
    ods_relative_path = "calendar_2024.ods"

    # Absolute path to the file
    ods_absolute_path = os.path.join(os.path.dirname(__file__), ods_relative_path)

    # Convert date from str to obj
    date_object = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    day_type = check_day_type_ods(ods_absolute_path, date_object)
    print(day_type.name)
    if day_type != DayType.unknown_day:
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()
