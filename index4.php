<?php
    include_once 'dbConfig.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/papaparse@5.3.0/papaparse.min.js"></script>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" ></script>


    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            background-color: #fff;
        }

        .container {
            max-width: 1140px;
            margin: 0 auto;
            background-color: #000000;
        }

        section {
            background-color: #000000;
        }

        nav{
            padding: 1rem;
            background-color: #000000;
        }

        .nav-con {
            display: flex;
            justify-content: space-between;
            background-color: #000000;
        }

        .logo a{
            font-size: 2rem;
            color: #fff;
            text-decoration: none;
            background-color: #000000;
            padding: 1rem 0;
        }

        .menu {
            display: flex;
            list-style: none;
            align-items: center;
            background-color: #000000;
        }

        .menu li {
            margin: 0 1rem;
            background-color: #000000;
        }

        .menu li a {
            color: #fff;
            text-decoration: none;
            background-color: #000000;
        }

        .container .graph {
            background-color: #000000;
        }

        .container .graph1 {
            background-color: #000000;
        }

        section {
            padding: 0rem;
            background-color: #000000;
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
            background-color: #000000;
        }

        .hero-info h3 {
            font-size: 2rem;
            background-color: #000000;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .hero-info h4 {
            font-size: 1.5rem;
            background-color: #000000;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .graph1 {
            background-color: #000000;
        }

        .graph1 .blog-btn {
            display: inline-block;
            background-color: #fff;
            color: #000000;
            padding: .5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            align-items:end ;
            position: relative;
            top: 104px;
            right: -958px;
        }

        .graph1 {
            background-color: #000000;
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

            <div class="hero-con">
                <div class="hero-info">
                    <h3>REQUIREMENTS</h3>
                </div>
                <div class="hero-info">
                    <h4>PLOT GRAPH</h3>
                </div>
            </div>
        </div>
    </nav>

    <section>
        <div class="container">
            <div class="graph">
                <div class="graph1"></div>
                    <canvas id="myChart" width="400" height="100"></canvas>

                    <script>
                        // โหลดไฟล์ CSV ด้วย Fetch API
                        fetch('uploads/7.csv')
                        .then(response => response.text())
                        .then(csvString => {
                            // แปลงข้อมูล CSV เป็นอาร์เรย์ของอ็อบเจ็กต์
                            Papa.parse(csvString, {
                            header: true,
                            dynamicTyping: true,
                            complete: function(results) {
                                const dates = results.data.map(row => row.date);
                                const sales = results.data.map(row => row.sale);

                                // สร้างกราฟและแสดงใน Canvas
                                const ctx = document.getElementById('myChart').getContext('2d');
                                new Chart(ctx, {
                                type: 'line',
                                data: {
                                    labels: dates,
                                    datasets: [{
                                    label: 'Sale',
                                    data: sales,
                                    fill: false,
                                    borderColor: 'black',
                                    tension: 0.1
                                    }]
                                },
                                options: {
                                    scales: {
                                    x: {
                                        time: {
                                        unit: 'date' // แสดงแกน X ในรูปแบบวัน
                                        }
                                    },
                                    y: {
                                        // ปรับแกน Y ให้เริ่มต้นที่ 0
                                        beginAtZero: true
                                    }
                                    }
                                }
                                });
                            }
                            });
                        });
                    </script>
                </div>

                <div class="graph1">
                    <a href="index5.php" class="blog-btn">NEXT</a>
                </div>
            </div>
        </div>
    </section>

    <section>
        <div class="container">
            <div class="graph-1">
                <div class="graph2"></div>
                <img src="assets/img/Black.png" alt="">
                </div>
            </div>
        </div>
    </section>
</body>
</html>
