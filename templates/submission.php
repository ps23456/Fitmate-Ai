<?php
// Establish database connection
$con = new mysqli("localhost", "root", "", "database");

// Check if the connection was successful
if ($con->connect_error) {
    die("Connection failed: " . $con->connect_error);
}

// Check if the form data is set
if (isset($_POST['name']) && isset($_POST['email']) && isset($_POST['age']) && isset($_POST['weight']) && isset($_POST['height']) && isset($_POST['bmi']) && isset($_POST['PhoneNumber']) && isset($_POST['healthhistory']) && isset($_POST['password'])) {
    // Sanitize and escape form inputs
    $name = mysqli_real_escape_string($con, $_POST['name']);
    $email = mysqli_real_escape_string($con, $_POST['email']);
    $age = mysqli_real_escape_string($con, $_POST['age']);
    $weight = mysqli_real_escape_string($con, $_POST['weight']);
    $height = mysqli_real_escape_string($con, $_POST['height']);
    $bmi = mysqli_real_escape_string($con, $_POST['bmi']);
    $PhoneNumber = mysqli_real_escape_string($con, $_POST['PhoneNumber']);
    $healthhistory = mysqli_real_escape_string($con, $_POST['healthhistory']);
    $password = mysqli_real_escape_string($con,$_POST['password']);

    // Prepare SQL statement
    $sql = "INSERT INTO signup (name, email,age,weight,height,bmi,PhoneNumber,healthhistory,password) VALUES (?, ?, ?,?,?,?,?,?,?)";
    $result = mysqli_prepare($con, $sql);

    // Check if the statement was prepared successfully
    if ($result === false) {
        die("Error: " . mysqli_error($con));
    }

    // Bind parameters
    mysqli_stmt_bind_param($result, "sssssss", $name, $email,$age,$weight,$height,$bmi,$PhoneNumber,$healthhistory,$password);

    // Execute the statement
    $check = mysqli_stmt_execute($result);

    // Check if the statement was executed successfully
    if ($check) {
        echo "Data inserted successfully";
    } else {
        die("Error: " . mysqli_error($con));
    }
} else {
    echo "Error: Required form fields not set.";
}

// Close the database connection
mysqli_close($con);
?>
