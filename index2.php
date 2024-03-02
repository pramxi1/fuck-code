<?php
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

        .box1 {
            display: grid;
        }

        .box1-con{
            padding: 1rem;
            display: grid;
            grid-template-columns: 1fr 1fr;
        }

        .box1-info{
            justify-content: right;
        }

        .box1-info h4 {
            font-size: 1.5rem;
            color: #fff;
            margin: 0;
            padding: 0;
            position: relative;
            top: 0px;
            right: -145px;
        }

        .box1-info img {
            padding: 1rem;
            width: 80%;
            position: relative;
            top: 0px;
            right: -30px;
        }

        .box1-info h5 {
            font-size: 1.4rem;
            color: #fff;
            margin: 0;
            padding: 0;
            position: relative;
            top: 50px;
            right: -20px;
        }

        .box1-info h6 {
            font-size: 1.5rem;
            color: #fd0000;
            margin: 0;
            padding: 0;
            position: relative;
            top: 100px;
            right: -20px;
        }

        .box1-info .blog-btn {
            display: inline-block;
            background-color: #fff;
            color: #000000;
            padding: .5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            align-items:end ;
            position: relative;
            top: 271px;
            right: -400px;
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
                    <h3>REQUIREMENTS</h3>
                </div>
            </div>
        </div>
    </section>

    <section class="box1">
        <div class="container">
            <div class="box1-con">
                <div class="box1-info">
                    <h4>EXAMPLE DATA</h4>
                    <img src="assets/img/table.png" alt="">
                </div>

                <div class="box1-info">
                    <h5>- Please import File in file.csv format.</h5>
                    <h5>- The file format must have 2 columns.</h5>
                    <h5>- The header of first column must be named Date.</h5>
                    <h5>- The header of the second column must be named Y.</h5>
                    <h6>Warning: If the data does not meet the requirements The file will not be usable. and will not be able to predict</h6>
                    <a href="index3.php" class="blog-btn">NEXT</a>
                </div>
            </div>
        </div>
    </section>

</body>
</html>