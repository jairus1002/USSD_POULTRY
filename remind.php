<?php
// Database connection parameters
$servername = "localhost";
$username = "root"; // Your MySQL username
$password = ""; // Your MySQL password
$dbname = "poultry2"; // Your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve form data
    $hatchingDate = $_POST["hatchingDate"];
    $poultryType = $_POST["poultryType"];
    $phoneNumber = $_POST["phoneNumber"];
    $country = $_POST["country"];
    $action = $_POST["action"];

    // Prepare SQL statement to insert data into remind table
    $insertQuery = "INSERT INTO remind (hatching_date, poultry_type, phone_number, country, action) 
                    VALUES ('$hatchingDate', '$poultryType', '$phoneNumber', '$country', '$action')";

    if ($conn->query($insertQuery) === TRUE) {
        echo "Reminder set successfully procceed to  comfirmation";
    } else {
        echo "Error: " . $insertQuery . "<br>" . $conn->error;
    }
}

// Close connection
$conn->close();
?>
