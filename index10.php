<?php
    include_once 'dbConfig.php';
?>

<!DOCTYPE html>
<html lang="en">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
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

        .box1-info .blog-btn {
            display: inline-block;
            background-color: #fff;
            color: #000000;
            padding: .5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            align-items:end ;
            position: relative;
            top: 459px;
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
                    <h3>Forecast Accuracy</h3>
                </div>
            </div>
        </div>
    </section>

    <section class="box1">
        <div class="container">
            <div class="box1-con">
                <div class="box1-info">
                    <h4>DATA</h4>
                    <canvas id="myChart" style="width:100%;max-width:600px"></canvas>
                    <script>
                    const xValues = [50,60,70,80,90,100,110,120,130,140,150];
                    const yValues = [7,8,8,9,9,9,10,11,14,14,15];

                    new Chart("myChart", {
                        type: "line",
                        data: {
                            labels: xValues,
                            datasets: [{
                                fill: false,
                                lineTension: 0,
                                backgroundColor: "rgba(0,0,255,1.0)",
                                borderColor: "rgba(0,0,255,0.1)",
                                data: yValues
                            }]
                        },
                        options: {
                            legend: {display: false},
                            scales: {
                                yAxes: [{ticks: {min: 6, max:16}}],
                            }
                        }
                    });
                    </script>
                </div>

                <div class="box1-info">
                    <a href="index10.php" class="blog-btn">NEXT</a>
                </div>
            </div>
        </div>
    </section>

</body>
</html>