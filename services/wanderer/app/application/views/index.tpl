<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WONDERER PAGE</title>
    <style>
        body {
            background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
            color: #fff;
            font-family: 'Roboto', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            padding: 0;
        }

        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 5px;
        }

        a {
            display: inline-block;
            margin: 10px 20px;
            padding: 10px 30px;
            border-radius: 30px;
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s ease, color 0.3s ease;
        }

        a:hover {
            background: #00b3ff;
            color: #1f1f1f;
        }

        hr {
            width: 80%;
            margin: 30px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .edit-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .edit-links a {
            background: #555;
        }

        .edit-links a:hover {
            background: #ff007a;
        }

        @keyframes glow {
            0% {
                box-shadow: 0 0 5px #00b3ff, 0 0 10px #00b3ff, 0 0 20px #00b3ff, 0 0 40px #00b3ff;
            }
            100% {
                box-shadow: 0 0 10px #ff007a, 0 0 20px #ff007a, 0 0 40px #ff007a, 0 0 80px #ff007a;
            }
        }

        a:hover {
            animation: glow 0.5s ease-in-out infinite alternate;
        }
    </style>
</head>
<body>
    <h1>Dashboard</h1>
    <a href="index.php?module=user&action=login">Login</a>
    <a href="index.php?module=user&action=register">Register</a>
    <a href="index.php?module=user&action=logout">Logout</a>
    <br><hr>
    <a href="index.php?module=page&action=samplePage">Create Sample Page</a>
    <a href="index.php?module=page&action=viewPage">View Page</a>
    <br><hr>
    <div class="edit-links">
        <span>Edit:</span>
        <a href="index.php?module=page&action=edit&type=html">HTML</a>
        <a href="index.php?module=page&action=edit&type=js">JS</a>
        <a href="index.php?module=page&action=edit&type=css">CSS</a>
    </div>
</body>
</html>
