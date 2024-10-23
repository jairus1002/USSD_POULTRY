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

// Query to get the latest row from the remind table
$sql_remind = "SELECT action, poultry_type FROM remind2 ORDER BY id DESC LIMIT 1";
$result_remind = $conn->query($sql_remind);

if ($result_remind->num_rows > 0) {
    // Fetch result
    $row_remind = $result_remind->fetch_assoc();
    $latest_action = $row_remind["action"];
    $latest_poultry_type = $row_remind["poultry_type"];

    // Check if the latest action is "vaccinate" and poultry type is "broilers"
    if (($latest_action === "vaccination") && ($latest_poultry_type === "broilers")) {
        // Define an array to map broilers' vaccination types to corresponding Python scripts
        $broilers_vaccination_scripts = array(
            "Marek" => "Marek2.py",
            "bronchitis1" => "bronchitis2_dose1.py",
            "Newcastle1" => "Newcastle2_dose1.py",
            "bronchitis2" => "bronchitis2_dose2.py",
            "Newcastle2" => "Newcastle2_dose2.py"
        );

        // Iterate over the array to check each broilers' vaccination type
        foreach ($broilers_vaccination_scripts as $vaccination_type => $script_name) {
            // Query to get the latest updated date for the broilers' vaccination type
            $sql = "SELECT $vaccination_type FROM vaccination_c ORDER BY id DESC LIMIT 1";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                // Fetch result
                $row = $result->fetch_assoc();
                $latest_date = $row[$vaccination_type];

                // Get current date
                $current_date = date("Y-m-d");

                // Debug printouts
                echo "Current Date: " . $current_date . "\n";
                echo "Latest Date ($vaccination_type): " . $latest_date . "\n";

                // Check if current date matches the latest updated date for this broilers' vaccination type
                if ($current_date === $latest_date) {
                    // Call Python script to send SMS
                    $output = [];
                    exec("python $script_name", $output);
                    echo implode("\n", $output);
                } else {
                    echo "Dates do not match for $vaccination_type";
                }
            } else {
                echo "No data found for $vaccination_type";
            }
        }
    } else {
        echo "Latest action is not 'vaccinate' for broilers";
    }
} else {
    echo "No data found in the remind table";
}

// Close connection
$conn->close();
?>
