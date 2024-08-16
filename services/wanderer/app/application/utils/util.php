<?php
namespace Utils;
class Util {

    public function isAlphaNumeric($str){

        return preg_match("/^[a-zA-Z0-9]+$/", $str) ? true : false;

    }
    public function alphaNumeric($str, $default = ''){

        return preg_match("/^[a-zA-Z0-9]+$/", $str) ? $str : $default;

    }

    public function alertExit($str, $back = 1){
        echo "<script>alert(`$str`); window.location.href = '/';</script>; if($back) history.back();";
        ;
        exit();

    }

}
