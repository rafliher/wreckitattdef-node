<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wonderer Your Page</title>
    <script src="{{script}}"></script>
    <link rel="stylesheet" href="{{css}}">
    <style>
        body {
            background: linear-gradient(135deg, #101010, #303030);
            color: #ffffff;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        h1, h2, h3 {
            color: #00b3ff;
            text-transform: uppercase;
            margin: 20px 0;
            text-align: center;
            letter-spacing: 2px;
        }

        p, li {
            font-size: 1.1em;
            line-height: 1.6em;
            margin: 10px 0;
            color: #dddddd;
        }

        a {
            color: #00b3ff;
            text-decoration: none;
            border-bottom: 1px solid rgba(0, 179, 255, 0.3);
            transition: color 0.3s ease, border-bottom 0.3s ease;
        }

        a:hover {
            color: #ff007a;
            border-bottom: 1px solid rgba(255, 0, 122, 0.5);
        }

        button {
            padding: 10px 20px;
            border-radius: 5px;
            background: #00b3ff;
            color: #ffffff;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            border: none;
            transition: background 0.3s ease, box-shadow 0.3s ease;
        }

        button:hover {
            background: #ff007a;
            box-shadow: 0 0 10px #ff007a, 0 0 20px #ff007a, 0 0 40px #ff007a;
        }

        input[type="text"], input[type="password"], textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 1em;
        }

        input[type="text"]:focus, input[type="password"]:focus, textarea:focus {
            background: rgba(255, 255, 255, 0.2);
            outline: none;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        table, th, td {
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            text-align: left;
        }

        th {
            background: #00b3ff;
            color: #101010;
        }

        td {
            background: rgba(255, 255, 255, 0.1);
        }

        th, td {
            transition: background 0.3s ease;
        }

        td:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    {{html}}
</body>
</html>
