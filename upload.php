<?php

session_start();
include_once 'dbConfig.php';


// file uploads path
$targetDir = "uploads/";

if (isset($_POST['submit'])) {
    if (!empty($_FILES["file"]["name"])) {
        $fileName = basename($_FILES["file"]["name"]);
        $targetFilePath = $targetDir . $fileName;
        $fileType = pathinfo($targetFilePath, PATHINFO_EXTENSION);

        // Allow certain file formats
        $allowTypes = array('csv');
        if (in_array($fileType, $allowTypes)) {
            if (move_uploaded_file($_FILES['file']['tmp_name'], $targetFilePath)) {
                $insert = $db->query("INSERT INTO CSV(file_name, uploaded_on) VALUE ('".$fileName."', NOW())");
                if ($insert) {
                    $_SESSION['statusMsg'] = "The flies <b>" . $fileName . "</b> has been uploaded successfully.";
                    header("location: index3.php");
                } else {
                    $_SESSION['statusMsg'] = "File upload failed, please try again.";
                    header("location: index3.php");
                }
            } else {
                $_SESSION['statusMsg'] = "Sorry, there was an error uploading your file.";
                header("location: index3.php");
            }
        } else {
            $_SESSION['statusMsg'] = "Sorry, only CSV files are allowed to upload.";
            header("location: index3.php");
        }
    } else {
        $_SESSION['statusMsg'] = "Please select a file to upload.";
        header("location: index3.php");
    }
}

?>