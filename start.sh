#!/bin/bash

# Open a new terminal and run a command
start_service() {
    xterm -hold -e "$1" &
}

# Start process-centric layer
start_service "cd process_centric/ && flask run"

# Start data_layer
start_service "cd data_layer/ && flask run -p 5051"

# Start Gear service
start_service "cd business_logic/Gear/ && flask run -p 5004"

# Start Huts service
start_service "cd business_logic/Huts/ && flask run -p 5003"

# Start Trails service
start_service "cd business_logic/Trails/ && flask run -p 5002"

# Start Weather service
start_service "cd business_logic/Weather/ && flask run -p 5001"

# Start adapter layer 
start_service "cd adapter_layer/ && flask run -p 5050"
