<?php
    if (isset($_GET['image'])) {
        $image = $_GET['image'];
        
        header('Content-Type: image/png');
        include($image);

        die();
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokémon Fetcher</title>

    <!-- Pokémon Font -->
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Press Start 2P', sans-serif;
            background: url('/bg.gif');
            background-size: cover;
            background-repeat: no-repeat;
            color: #333;
            text-align: center;
            padding: 50px;
            margin: 0 !important;
            height: 100vh;
            box-sizing: border-box;
        }
        h1 {
            color: #ffcb05;
            text-shadow: 2px 2px #3b4cca;
            margin-bottom: 40px;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            font-size: 1.2em;
            margin-right: 10px;
        }
        input[type="text"] {
            font-size: 1em;
            padding: 10px;
            width: 200px;
            border: 2px solid #3b4cca;
            border-radius: 5px;
            text-align: center;
        }
        button {
            font-size: 1em;
            padding: 10px 20px;
            background-color: #3b4cca;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px;
        }
        button:hover {
            background-color: #2b3b9c;
        }
        h2 {
            color: #3b4cca;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        img {
            width: 500px;
            background-color: wheat;
            height: auto;
            border: 5px solid #ffcb05;
            border-radius: 15px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
        }
        p {
            font-size: 1.2em;
            color: #cc0000;
        }
    </style>
</head>
<body>
    <h1>Pokémon Fetcher</h1>
    <form method="post" action="">
        <label for="pokemon_name">Enter Pokémon Name:</label>
        <input type="text" id="pokemon_name" name="pokemon_name" required>
        <button type="submit">Fetch Pokémon</button>
    </form>

    <audio id="bgMusic" loop>
        <source src="/bgintro.mp3" type="audio/mpeg">
    </audio>

    <script>
        function play(){
            var bgMusic = document.getElementById('bgMusic');
            if (bgMusic.paused) {
                bgMusic.play();
            }
        }
        document.body.addEventListener('click', function() {
            play()
        }, { once: true });
        document.body.addEventListener('mouseover', function() {
            play()
        }, { once: true });
    </script>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $pokemon_name = $_POST["pokemon_name"];
        $command = "curl -s https://pokeapi.co/api/v2/pokemon/" . ($pokemon_name);
        $output = shell_exec($command);

        $pokemon_data = json_decode($output, true);

        if (isset($pokemon_data['name'])) {
            $pokemon_name = ucfirst($pokemon_data['name']);
            $pokemon_image_url = $pokemon_data['sprites']['front_default'];
            $pokemon_image_file = strtolower($pokemon_name) . ".png";

            // Download the image and save it as a file
            file_put_contents($pokemon_image_file, file_get_contents($pokemon_image_url));

            // Display the Pokémon name and image
            echo "<h2>Pokémon: $pokemon_name</h2>";
            echo "<div>";
            echo "<img src='data:image/png;base64,".base64_encode(file_get_contents($pokemon_image_file))."' alt=\"$pokemon_name\">";
            echo "</div>";
        } else {
            echo "<p>Pokémon not found. Please try again.</p>";
        }
    }
    ?>
</body>
</html>
