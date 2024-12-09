#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

############################################################
#
# Fitness Tracker Endpoints
#
############################################################

set_goal() {
  user_id=$1
  goal_type=$2
  target_value=$3
  end_date=$4

  echo "Setting goal ($goal_type, target: $target_value) for user $user_id..."
  response=$(curl -s -X POST "$BASE_URL/set-goals" -H "Content-Type: application/json" \
    -d "{\"user_id\":$user_id, \"goal_type\":\"$goal_type\", \"target_value\":$target_value, \"end_date\":\"$end_date\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Goal set successfully for user $user_id."
  else
    echo "Failed to set goal for user $user_id."
    echo "$response"
    exit 1
  fi
}

get_goals() {
  user_id=$1

  echo "Retrieving goals for user $user_id..."
  response=$(curl -s -X GET "$BASE_URL/get-goals/$user_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Goals retrieved successfully for user $user_id."
    if [ "$ECHO_JSON" = true ]; then
      echo "Goals JSON for user $user_id:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve goals for user $user_id."
    echo "$response"
    exit 1
  fi
}

update_goal() {
  goal_id=$1
  target_value=$2
  end_date=$3

  echo "Updating goal ID $goal_id..."
  response=$(curl -s -X PUT "$BASE_URL/update-goal" -H "Content-Type: application/json" \
    -d "{\"goal_id\":$goal_id, \"target_value\":$target_value, \"end_date\":\"$end_date\"}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Goal updated successfully for goal ID $goal_id."
  else
    echo "Failed to update goal ID $goal_id."
    echo "$response"
    exit 1
  fi
}

track_progress() {
  user_id=$1

  echo "Tracking progress for user $user_id..."
  response=$(curl -s -X GET "$BASE_URL/track-progress/$user_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Progress tracked successfully for user $user_id."
    if [ "$ECHO_JSON" = true ]; then
      echo "Progress JSON for user $user_id:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to track progress for user $user_id."
    echo "$response"
    exit 1
  fi
}

log_workout() {
  user_id=$1
  workout_type=$2
  duration=$3
  calories_burned=$4

  echo "Logging workout ($workout_type, duration: $duration mins, calories burned: $calories_burned) for user $user_id..."
  response=$(curl -s -X POST "$BASE_URL/log-workout" -H "Content-Type: application/json" \
    -d "{\"user_id\":$user_id, \"workout_type\":\"$workout_type\", \"duration\":$duration, \"calories_burned\":$calories_burned}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Workout logged successfully for user $user_id."
  else
    echo "Failed to log workout for user $user_id."
    echo "$response"
    exit 1
  fi
}

get_recommendations() {
  goal_type=$1
  num_recommendations=$2

  echo "Getting recommendations for goal type $goal_type..."
  response=$(curl -s -X GET "$BASE_URL/get-recommendations?goal_type=$goal_type&num_recommendations=$num_recommendations")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Recommendations retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Recommendations JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get recommendations."
    echo "$response"
    exit 1
  fi
}

############################################################
#
# Run Tests
#
############################################################

# Health checks
check_health
check_db

# Fitness Tracker tests
set_goal 1 "weight_loss" 10 "2024-12-31"
get_goals 1
update_goal 1 15 "2025-01-01"
track_progress 1
log_workout 1 "Running" 45 400
get_recommendations "cardio" 2
