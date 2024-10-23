<?php
// Database connection parameters
$servername = "localhost";  // Update with your database host
$username = "root";  // Update with your database username
$password = "";  // Update with your database password
$dbname = "ussd";  // Update with your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve the POST data from the USSD request
$hatching_date = $_POST['hatching_date'];
$phone_number = $_POST['phone_number'];
$action = $_POST['option'];  // This is the 'action' column in the database (either Vaccination or Management)
$poultry_type = $_POST['poultry_type'];

// Prepare and bind the SQL statement
$stmt = $conn->prepare("INSERT INTO remind2 (hatching_date, phone_number, action, poultry_type) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ssss", $hatching_date, $phone_number, $action, $poultry_type);

// Execute the SQL query
if ($stmt->execute()) {
    echo "Success";
} else {
    echo "Error: " . $stmt->error;
}

// Close the connection
$stmt->close();
$conn->close();
?>
