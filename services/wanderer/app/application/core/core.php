<?php

namespace Core;
class Core {

    private $module;
    private $action;
    private $instance;

    public function __construct($module = null, $action = null) {

        $this->module = $module;
        $this->action = $action;

    }
    public function run(){

        $this->init();
        $this->getInstance();
        $this->action();

    }
    public function init() {

        $util = new \utils\util();
        $_module = $_GET['module']; 
        $_action = $_GET['action']; 

        if(!isset($_module) && !isset($_action)){

            $tmp = explode('/', $_SERVER['PATH_INFO']);
            $_module = $tmp[1];
            $_action = $tmp[2];
            
        }

        $this->module = $util->alphaNumeric($_module, 'index');
        $this->action = $util->alphaNumeric($_action, 'main');

    }

    public function action() {

        $_instance = $this->instance;
        $_action = $this->action;

        if(method_exists($_instance, $_action)){

            $_instance->$_action(); 

        }

    }

    public function getInstance() {

        $_module = $this->module;

        if(!file_exists(CONT . $_module . 'Controller.php')){

            $_module = 'index';
            $this->module = $_module;
            $this->action = 'main';

        }

        $className = 'controllers\\' . $_module . 'Controller';
        $this->instance = new $className();
        
    }

}