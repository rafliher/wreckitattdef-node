<?php

namespace Controllers;

class PageController {

    private $file;
    private $userData;
    private $util;
    public function __construct() {

        $this->util = new \utils\util();
        $this->file = new \models\fileModel();
        $this->userData = $_SESSION['userData'];
        if(!isset($this->userData)) $this->util->alertExit("Login Dulu bang!!");
    }

    public function samplePage() {

        $this->file->copyFile(ROOT . 'public/sample.html', ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.html');
        $this->file->copyFile(ROOT . 'public/sample.js', ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.js');
        $this->file->copyFile(ROOT . 'public/sample.css', ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.css');
        $this->util->alertExit("Create Success");

    }

    public function viewPage() {

        $tpl = new \utils\template(VIEW . 'page.tpl');
        $tpl->render([
            "script" => './user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.js',
            "css" => './user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.css',
            "html" => $this->file->getFile(ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.html')
        ]);

    }

    public function edit() {

        if(!in_array($_REQUEST['type'], ['html', 'js', 'css'])) $this->util->alertExit("Invalid type");

        if($_SERVER['REQUEST_METHOD'] == 'POST'){

            $this->file->createFile(ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.' . $_POST['type'], $_POST['data']);
            $this->util->alertExit("Edit Success");
        }

        $tpl = new \utils\template(VIEW . 'textarea.tpl');
        $tpl->render(["type" => $_GET['type'], "data" => $this->file->getFile(ROOT . 'user/' . $this->userData['uuid'] . '/' . $this->userData['uuid'] . '.' . $_GET['type'])]);

    }

}