<?php
    session_start();
    include_once 'dbConfig.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Upload CSV System</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            /*overflow:hidden;*/
            background-color: #000000;
        }

        nav{
            padding: 1rem;
            background-color: #000000;
        }

        .container {
            max-width: 1140px;
            margin: 0 auto;
        }

        .nav-con {
            display: flex;
            justify-content: space-between;
        }

        .logo a{
            font-size: 2rem;
            color: #fff;
            text-decoration: none;
        }

        .menu {
            display: flex;
            list-style: none;
            align-items: center;
        }

        .menu li {
            margin: 0 1rem;
        }

        .menu li a {
            color: #fff;
            text-decoration: none;
        }

        .hero {
            background-color: #000000;
            display: grid;  
        }

        .hero-con {
            background-color: #000000;
            position: relative;
            top: 20px;
        }

        .hero-info {
            width: 100%;
            padding: 2rem;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .hero-info h3 {
            font-size: 2rem;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .hero-info a {
            justify-content: right;
        }

        .text-center h6 {
            font-size: 1rem;
            color: #fff;
        }

        .text-center p {
            font-size: 1rem;
            color: #fff;
        }

        .d-sm-flex input {
            background-color: #fff;
            color: #000000;
            font-size: 1rem;
            padding: .5rem 1rem;
            position: relative;
            top: 0px;
            right: 517px;
        }

        .blog-item a {
            display: inline-block;
            background-color: #fff;
            color: #000000;
            padding: .5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            align-items:end ;
            position: relative;
            top: 256px;
            right: -958px;
        }
    </style>
</head>

<body>
    <nav>
        <div class="container">
            <div class="nav-con">
            <div class="logo">
                <a href="http://www.cmustat.com/statistics/">Statistics CMU</a>
            </div>
            <ul class="menu">
                <li><a href="index.php">HOME</a></li>
                <li><a href="#">ABOUT US</a></li>
                <li><a href="#">WORK</a></li>
                <li><a href="#">PORTFOLIO</a></li>
                <li><a href="#">CONTACT US</a></li>
            </ul>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="container">
            <div class="hero-con">
                <div class="hero-info">
                    <h3>IMPORT FILE</h3>
                </div>
            </div>
        </div>
    </section>

    <section class="box1">
        <div class="container">
            <div class="row mt-12">
                <div class="col-12">
                    <form action="upload.php" method="POST" enctype="multipart/form-data">
                        <div class="text-center justify-content-center align-items-center p-4 border-2 border-dashed rounded-3">
                            <h6 class="my-2">Select CSV file to Upload</h6>
                            <input type="file" name="file" class="form-control streched-link" accept=".csv">
                            <p class="small mb-0 mt-2"><b>NOTE:</b> Only CSV file are Allowed to Upload</p>
                        </div>

                        <div class="d-sm-flex justify-content-end mt-2">
                            <input type="submit" name="submit" value="Upload" class="btn btn-sm btn-primary mb-3">
                        </div>

                        <div class="blog-item">
                            <a href="index4.php" class="blog-btn">NEXT</a>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row">
                <?php if (!empty($_SESSION['statusMsg'])) { ?>
                    <div class="alert alert-success" role="alert">
                        <?php 
                            echo $_SESSION['statusMsg']; 
                            unset($_SESSION['statusMsg']);
                        ?>
                    </div>
                <?php } ?>
            </div>
        </div>
    </section>

</body>
</html>