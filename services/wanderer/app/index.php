<?php

define('ROOT', __DIR__ . '/');
require_once ROOT . 'application/core/bootstrap.php';

$core = new \core\core();
$core->run();