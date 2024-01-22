#!/bin/bash

TASK_NAME="bitrix_task"
SERVICE_FILE_NAME="add_task.service"
RUN_SCRIPT_NAME="run_add_task.sh"

# Stop and disable the service
echo "Stopping and disabling the service..."
sudo systemctl stop $TASK_NAME.service
sudo systemctl disable $TASK_NAME.service

# Remove the service file from /etc/systemd/system/
echo "Removing the systemd service file..."
sudo rm /etc/systemd/system/$SERVICE_FILE_NAME

# Reload systemd to apply changes
sudo systemctl daemon-reload

# Remove the run script
echo "Removing the run script..."
rm $RUN_SCRIPT_NAME

echo "Uninstallation completed."
