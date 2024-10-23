<?php
// Database connection parameters
$servername = "localhost";
$username = "root"; // Your MySQL username
$password = ""; // Your MySQL password
$dbname = "ussd"; // Your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Use prepared statement to avoid SQL injection
$sql = "SELECT hatching_date, poultry_type, action FROM remind2 ORDER BY id DESC LIMIT 1";
$result = $conn->query($sql);

if ($result === false) {
    // Log query error
    echo "Error: Could not retrieve data from remind2 table. " . $conn->error;
    exit();
}

if ($result->num_rows > 0) {
    // Fetch the last row
    $row = $result->fetch_assoc();
    $hatchDate = $row["hatching_date"];
    $poultryType = $row["poultry_type"];
    $action = $row["action"];

    // Debugging: Display fetched data
    echo "Hatching Date: " . $hatchDate . "<br>";
    echo "Poultry Type: " . $poultryType . "<br>";
    echo "Action: " . $action . "<br>";

    // Initialize feeding schedule array with default values
    $feedingSchedule = array(
        'starter_feed' => "",
        'grower_feed' => "",
        'layer_feed' => "",  // For layers
        'finisher_feed' => "" // For broilers
    );

    switch ($action) {
        case "management":
            if (empty($hatchDate)) {
                echo "Error: Hatching date is missing.";
                break;
            }

            $hatchDate = strtotime($hatchDate);
            if ($hatchDate === false) {
                echo "Error: Invalid hatching date format.";
                break;
            }

            // Handling for layers
            if ($poultryType === "layers") {
                $feedingSchedule['starter_feed'] = date('Y-m-d', strtotime('+0 weeks', $hatchDate));
                $feedingSchedule['grower_feed'] = date('Y-m-d', strtotime('+0 weeks', $hatchDate));
                $feedingSchedule['layer_feed'] = "Not applicable";

                // Prepared statement to avoid SQL injection
                $insertSql = $conn->prepare("INSERT INTO layers2 (starter, grower, layer) VALUES (?, ?, ?)");
                $insertSql->bind_param('sss', $feedingSchedule['starter_feed'], $feedingSchedule['grower_feed'], $feedingSchedule['layer_feed']);

                if ($insertSql->execute()) {
                    echo "Confirmation success.";
                } else {
                    echo "Error: " . $conn->error;
                }
                $insertSql->close();
            } 
            // Handling for broilers
            elseif ($poultryType === "broilers") {
                $feedingSchedule['starter_feed'] = date('Y-m-d', strtotime('+0 weeks', $hatchDate));
                $feedingSchedule['grower_feed'] = date('Y-m-d', strtotime('+0 weeks', $hatchDate));
                $feedingSchedule['finisher_feed'] = date('Y-m-d', strtotime('+0 weeks', $hatchDate));

                // Prepared statement to avoid SQL injection
                $insertSql = $conn->prepare("INSERT INTO broiler1 (starterb, growerb, finisher) VALUES (?, ?, ?)");
                $insertSql->bind_param('sss', $feedingSchedule['starter_feed'], $feedingSchedule['grower_feed'], $feedingSchedule['finisher_feed']);

                if ($insertSql->execute()) {
                    echo "Press finish button to finalize.";
                } else {
                    echo "Error: " . $conn->error;
                }
                $insertSql->close();
            }
            break;

        case "vaccination":
            if (empty($hatchDate)) {
                echo "Error: Hatching date is missing.";
                break;
            }

            $hatchDate = strtotime($hatchDate);
            if ($hatchDate === false) {
                echo "Error: Invalid hatching date format.";
                break;
            }

            // Vaccination schedule for layers
            if ($poultryType === "layers") {
                $vaccinationScheduleLayers = array(
                    'marek' => date('Y-m-d', $hatchDate),
                    'newcastle_1' => date('Y-m-d', strtotime('+2 weeks', $hatchDate)),
                    'bronchitis_1' => date('Y-m-d', strtotime('+4 weeks', $hatchDate)),
                    'newcastle_2' => date('Y-m-d', strtotime('+6 weeks', $hatchDate)),
                    'bronchitis_2' => date('Y-m-d', strtotime('+8 weeks', $hatchDate)),
                    'fowl_pox' => date('Y-m-d', strtotime('+12 weeks', $hatchDate))
                );

                $insertSql = $conn->prepare("INSERT INTO vaccination_b (Marek, Newcastle1, bronchitis1, Newcastle2, bronchitis2, Fowl_pox) 
                              VALUES (?, ?, ?, ?, ?, ?)");
                $insertSql->bind_param(
                    'ssssss',
                    $vaccinationScheduleLayers['marek'],
                    $vaccinationScheduleLayers['newcastle_1'],
                    $vaccinationScheduleLayers['bronchitis_1'],
                    $vaccinationScheduleLayers['newcastle_2'],
                    $vaccinationScheduleLayers['bronchitis_2'],
                    $vaccinationScheduleLayers['fowl_pox']
                );

                if ($insertSql->execute()) {
                    echo "Confirmation success.";
                } else {
                    echo "Error: " . $conn->error;
                }
                $insertSql->close();
            }
            // Vaccination schedule for broilers
            elseif ($poultryType === "broilers") {
                $vaccinationScheduleBroilers = array(
                    'marek' => date('Y-m-d', $hatchDate),
                    'bronchitis_1' => date('Y-m-d', strtotime('+1 week', $hatchDate)),
                    'newcastle_1' => date('Y-m-d', strtotime('+2 weeks', $hatchDate)),
                    'bronchitis_2' => date('Y-m-d', strtotime('+3 weeks', $hatchDate)),
                    'newcastle_2' => date('Y-m-d', strtotime('+4 weeks', $hatchDate))
                );

                $insertSql = $conn->prepare("INSERT INTO vaccination_c (Marek, bronchitis1, Newcastle1, bronchitis2, Newcastle2) 
                              VALUES (?, ?, ?, ?, ?)");
// Insert vaccination schedule into vaccination_c table
$insertSql = $conn->prepare("INSERT INTO vaccination_c (Marek, bronchitis1, Newcastle1, bronchitis2, Newcastle2) 
                              VALUES (?, ?, ?, ?, ?)");

if ($insertSql === false) {
    // Output error information
    die("Error preparing statement: " . $conn->error);
}

// Bind parameters
$insertSql->bind_param(
    'sssss',
    $vaccinationScheduleBroilers['marek'],
    $vaccinationScheduleBroilers['bronchitis_1'],
    $vaccinationScheduleBroilers['newcastle_1'],
    $vaccinationScheduleBroilers['bronchitis_2'],
    $vaccinationScheduleBroilers['newcastle_2']
);

// Execute the statement and check for errors
if ($insertSql->execute()) {
    echo "Vaccination schedule inserted for broilers.<br>";
} else {
    echo "Error executing statement: " . $insertSql->error;
}

// Close the prepared statement
$insertSql->close();

            }
            break;

        default:
            echo "Error: Invalid action type.";
    }
} else {
    echo "No records found in remind2 table.";
}

// Close connection
$conn->close();
?>
