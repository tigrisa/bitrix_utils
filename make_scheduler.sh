#!/bin/bash

TASK_NAME="bitrix_task"
SERVICE_FILE_NAME="add_task.service"
RUN_SCRIPT_NAME="run_add_task.sh"
EXECUTABLE_NAME="add_task"

# Is pipx installed?
# You have to install it mannualy
if ! command -v pipx &> /dev/null; then
    echo "pipx is not installed."
    echo "Please install pipx using 'pip install pipx' and then run 'pipx ensurepath'"
    exit 1
fi

# Install add_task 
echo "Installing the add_task project using pipx..."
pipx install .

# Create a run add_task script...
echo "Creating the run script..."
cat > $RUN_SCRIPT_NAME <<EOF
#!/bin/bash

# Get the full path to the directory containing this script
WORKING_DIR=\$(dirname "\$(realpath "\$0")")

# Go to the working directory
cd "\$WORKING_DIR" || exit

# Execute the task
$EXECUTABLE_NAME --date today --randdelay 59
EOF


# Make exec script executable
chmod +x $RUN_SCRIPT_NAME

# Create a unit systemd file
echo "Creating the systemd service file..."
cat > $SERVICE_FILE_NAME <<EOF
[Unit]
Description=$TASK_NAME Service

[Service]
ExecStart=\$(pwd)/$RUN_SCRIPT_NAME

[Install]
WantedBy=multi-user.target
EOF

# Copy the service file to /etc/systemd/system/
sudo cp $SERVICE_FILE_NAME /etc/systemd/system/

# Enable and start the service
echo "Enabling and starting the service..."
sudo systemctl enable $TASK_NAME.service
sudo systemctl start $TASK_NAME.service

echo "Installation completed."
