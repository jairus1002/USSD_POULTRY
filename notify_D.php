<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "ussd";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Define an array to map feeding types to corresponding Python scripts
$feeding_scripts = array(
    "starterb" => "starterb.py",
    "growerb" => "growerb.py",
    "finisher" => "finisher.py" // Add finisher feed with its corresponding Python script
);

// Iterate over the array to check each feeding type
foreach ($feeding_scripts as $feeding_type => $script_name) {
    // Query to get the latest updated date for the feeding type
    $sql = "SELECT $feeding_type FROM broiler1 ORDER BY id DESC LIMIT 1";
    $result = $conn->query($sql);

    if ($result === false) {
        // Log the error if the query fails
        echo "SQL Error: " . $conn->error . "\n";
    } else if ($result->num_rows > 0) {
        // Fetch result
        $row = $result->fetch_assoc();
        $latest_date = $row[$feeding_type];

        // Get current date
        $current_date = date("Y-m-d");

        // Debug printouts
        echo "Current Date: " . $current_date . "\n";
        echo "Latest Date ($feeding_type): " . $latest_date . "\n";

        // Check if current date matches the latest updated date for this feeding type
        if ($current_date === $latest_date) {
            // Call Python script to send SMS
            $output = [];
            exec("python $script_name", $output);
            echo implode("\n", $output);
        } else {
            echo "Dates do not match for $feeding_type\n";
        }
    } else {
        echo "No data found for $feeding_type\n";
    }
}

// Close connection
$conn->close();
?>
