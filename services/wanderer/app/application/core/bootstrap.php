<?php

define('APP', ROOT . 'application/');
define('CORE', APP . 'core/');
define('CONT', APP . 'controllers/');
define('VIEW', APP . 'views/');
#ini_set('display_errors', 1);

function autoload($class) {
    
    $class = str_replace('\\', '/', $class);
    $classFilePath = APP . "$class.php";
    
    if (file_exists($classFilePath)) {
    
        require_once($classFilePath);
    
    }
    
}

spl_autoload_register("autoload");
session_start();
