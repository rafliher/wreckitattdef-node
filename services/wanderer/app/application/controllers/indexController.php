<?php

namespace Controllers;

class IndexController {

    private $tpl;
    public function __construct() {

    }

    public function main() {

        $this->tpl = new \utils\template(VIEW . 'index.tpl');
        $this->tpl->render(["test"=>"foo"]);
        
    }

}