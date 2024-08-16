<?php

namespace Controllers;

class UserController {

    private $file;
    private $user;
    private $util;
    public function __construct() {

        $this->util = new \utils\util();
        $this->file = new \models\fileModel();
        $this->user = new \models\userModel($this->file);
    }

    public function login() {

        if($_SERVER['REQUEST_METHOD'] == 'POST'){

            $_POST['username'] = str_replace(array('.', '/', '\\'), '_', $_POST['username']);
            if(empty($_POST['username']) || empty($_POST['password'])) 
            
                $this->util->alertExit("username or password is empty");

            $userData = $this->user->getUserByUsername($_POST['username']);
            $hPassword = hash("sha256", $_POST['password']);
            if($userData['password'] == $hPassword) 

                $_SESSION['userData'] = $userData;

            else 

                $this->util->alertExit("username or password is wrong");
            
            $this->util->alertExit("Login Success");
        }
        $tpl = new \utils\template(VIEW . 'login.tpl');
        $tpl->render([]);

    }

    public function register() {

        if($_SERVER['REQUEST_METHOD'] == 'POST'){

            $_POST['username'] = str_replace(array('.', '/', '\\'), '_', $_POST['username']);
            if(empty($_POST['username']) || empty($_POST['password'])) 
            
                $this->util->alertExit("username or password is empty");

            if(strlen($_POST['username']) < 10) 
            
                $this->util->alertExit("username length must be greater than 10");

            $userData = $this->user->getUserByUsername($_POST['username']);
            if($userData != null)
            
                $this->util->alertExit("username already exists");

            $this->user->createUser($_POST['username'], $_POST['password']);
            $this->util->alertExit("Register Success");
        }
        $tpl = new \utils\template(VIEW . 'register.tpl');
        $tpl->render([]);

    }

    public function logout() {

        session_destroy();
        $this->util->alertExit("Logout Success");

    }

}