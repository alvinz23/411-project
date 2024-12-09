#!/bin/bash

# Base URL for the Flask API
BASE_URL="http://127.0.0.1:5000"

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  response=$(curl -s "$BASE_URL/health")
  echo "$response" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to create a user
create_account() {
  echo "Creating a test user account..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' "$BASE_URL/create-account")
  echo "$response" | grep -q '"message": "Account created successfully."'
  if [ $? -eq 0 ]; then
    echo "Account creation passed!"
  else
    echo "Account creation failed."
    exit 1
  fi
}

# Function to test login
login() {
  echo "Testing user login..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' "$BASE_URL/login")
  echo "$response" | grep -q '"message": "Login successful."'
  if [ $? -eq 0 ]; then
    echo "Login passed!"
  else
    echo "Login failed."
    exit 1
  fi
}

# Function to update the user's password
update_password() {
  echo "Testing password update..."
  response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "new_password": "newpassword123"}' "$BASE_URL/update-password")
  echo "$response" | grep -q '"message": "Password updated successfully."'
  if [ $? -eq 0 ]; then
    echo "Password update passed!"
  else
    echo "Password update failed."
    exit 1
  fi
}

# Function to add a workout
add_workout() {
  workout_id=$1
  echo "Adding workout ID $workout_id..."
  response=$(curl -s -X POST "$BASE_URL/workouts/$workout_id")
  echo "$response" | grep -q '"message": "Workout added to memory."'
  if [ $? -eq 0 ]; then
    echo "Add workout passed!"
  else
    echo "Add workout failed."
    exit 1
  fi
}

# Function to list workouts
list_workouts() {
  echo "Listing all workouts..."
  response=$(curl -s -X GET "$BASE_URL/workouts")
  echo "$response" | grep -q '"stored_workouts"'
  if [ $? -eq 0 ]; then
    echo "List workouts passed!"
  else
    echo "List workouts failed."
    exit 1
  fi
}

# Function to update a workout
update_workout() {
  workout_id=$1
  echo "Updating workout ID $workout_id..."
  response=$(curl -s -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Workout", "description": "Updated Description"}' "$BASE_URL/workouts/$workout_id")
  echo "$response" | grep -q '"message": "Workout updated."'
  if [ $? -eq 0 ]; then
    echo "Update workout passed!"
  else
    echo "Update workout failed."
    exit 1
  fi
}

# Function to delete a workout
delete_workout() {
  workout_id=$1
  echo "Deleting workout ID $workout_id..."
  response=$(curl -s -X DELETE "$BASE_URL/workouts/$workout_id")
  echo "$response" | grep -q '"message": "Workout deleted and logged."'
  if [ $? -eq 0 ]; then
    echo "Delete workout passed!"
  else
    echo "Delete workout failed."
    exit 1
  fi
}

# Function to list deleted workouts
list_deleted_workouts() {
  echo "Listing all deleted workouts..."
  response=$(curl -s -X GET "$BASE_URL/workouts/deleted")
  echo "$response" | grep -q '"deleted_workouts"'
  if [ $? -eq 0 ]; then
    echo "List deleted workouts passed!"
  else
    echo "List deleted workouts failed."
    exit 1
  fi
}

############################################
# Execute Smoke Tests
############################################

check_health

create_account
login
update_password

# Using valid workout IDs: 85 and 86, some ids dont work because they arent valid IDs in the API 
add_workout 85
add_workout 86
list_workouts

update_workout 85
delete_workout 85
list_deleted_workouts

echo "All smoke tests passed successfully!"
