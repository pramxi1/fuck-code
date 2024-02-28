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
            top: 80px;
        }

        .hero-info {
            width: 100%;
            padding: 2rem;
        }

        .hero-info h3 {
            font-size: 7rem;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .hero-info p {
            color: #fff;
            margin: 0;
            margin: 0;
            padding: 0;
        }

        .hero-info a {
            justify-content: right;  
        }

        .blog{
            color: #000000;
            background-color: #000000;
        }

        .blog-con{
            display: grid;
            grid-template-columns: 1fr 1fr;
        }

        .blog-item .blog-btn {
            display: inline-block;
            background-color: #fff;
            color: #000000;
            padding: .5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            align-items:end ;
            position: relative;
            top: 245px;
            right: -400px;
        }

        .hero-img {
            width: 100%;
            padding: 2rem;
        }

        .blog-item img {
            width: 200%;
            position: relative;
            top: -50px;
            right: 90px;
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
                    <h3>ANALYZE TIME SERIES DATA</h3>
                </div>
            </div>
        </div>
    </section>

    <section class="blog">
        <div class="container">
            <div class="blog-con">
                <div class="blog-item">
                    <img src="1.png" alt="">
                </div>

                <div class="blog-item">
                    <a href="index2.php" class="blog-btn">NEXT</a>
                </div>

            </div>
        </div>
    </section>

</body>
</html>