<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit {{type}}</title>
    <style>
        body {
            background: linear-gradient(135deg, #1a1a1a, #333333);
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: #00b3ff;
        }

        form {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 179, 255, 0.3);
            text-align: center;
            width: 100%;
            max-width: 900px;
        }

        textarea {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff;
            font-size: 1em;
            font-family: 'Courier New', Courier, monospace;
            resize: vertical;
        }

        textarea:focus {
            background: rgba(255, 255, 255, 0.3);
            outline: none;
        }

        input[type="submit"] {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background: #00b3ff;
            color: #ffffff;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s ease, box-shadow 0.3s ease;
            margin-top: 20px;
        }

        input[type="submit"]:hover {
            background: #ff007a;
            box-shadow: 0 0 10px #ff007a, 0 0 20px #ff007a, 0 0 40px #ff007a;
        }
    </style>
</head>
<body>
    <h1>Edit {{type}}</h1>
    <form action="" method="POST">
        <textarea name="data" cols="100" rows="20">{{data}}</textarea><br>
        <input type="hidden" name="type" value="{{type}}">
        <input type="submit" value="Save">
    </form>
</body>
</html>
