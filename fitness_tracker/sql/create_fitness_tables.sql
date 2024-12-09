-- Create the goals table
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_type TEXT NOT NULL, -- e.g., "weight_loss", "exercise"
    target_value REAL NOT NULL, -- The target value for the goal
    progress REAL DEFAULT 0, -- Progress made toward the goal
    start_date TEXT DEFAULT (DATE('now')), -- When the goal starts
    end_date TEXT NOT NULL -- When the goal should be completed
);

-- Create the workouts table
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, -- Foreign key to the user
    workout_type TEXT NOT NULL, -- e.g., "Running", "Cycling"
    duration INTEGER NOT NULL, -- Duration in minutes
    calories_burned REAL NOT NULL, -- Calories burned in the workout
    date TEXT DEFAULT (DATE('now')) -- Date of the workout
);

-- Optionally, create additional tables, such as users, if needed
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE, -- Username for the user
    email TEXT NOT NULL UNIQUE, -- Email address of the user
    password TEXT NOT NULL -- Hashed password for authentication
);
