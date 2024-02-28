<?php

$conn = mysqli_connect("localhost", "root", "", "csv");

if(isset($_POST["import"])){
    $fileName = $_FILES["file"]["tmp_name"];

    if($_FILES["file"]["size"] > 0){
        $file = fopen($fileName, "r");

        while(($column = fgetcsv($file, 10000, ",")) !== FALSE) {
            $sqlInsert = "Insert into data (name, type) values (". $column[0] . "', '" . column[1] ."')";

            $result = mysqli_query($conn, $sqlInsert);

            if(!empty($result)) {
                echo "CSV Data Imported into the database";
            } else {
                echo "Problem in importing csv";
            }
        }
    }
}

?>

<form classs="form-horizoontal" action="" method="post" name="uploadCsv" enctype="multipart/form-data">

<div>
<label>Choose CSV File</label>
<input type="file" name="file" accept=".csv">
<button type="submit" name="import">Import</button>


</div>

</form>


<div class="row g-2">
                <?php
                    $query = $db->query("SELECT * FROM CSV BY uploaded_on DESC");
                    if ($query->num_row > 0) {
                        ?>
                        <table>
                        <thead>
                        <tr>
                        <th>id</th>
                        <th>file_name</th>
                        <th>Type</th>
                        </tr>
                        </thead>
                        <?php
                        while ($row = $query->fetch_assoc()) {
                            $csvURL = 'uploads/'.row['file_name'];
                        }
                    }
                ?>
            </div>