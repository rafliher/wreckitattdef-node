<?php
namespace Utils;
class Template {

    private $source;
    private $stream;
    private $assetsDir;
    private $debug;
    public function __construct($source = '') {

        $this->debug = 0;
        $this->source = $source;
        $this->stream = file_get_contents($source);
        $this->setAssetsDir(ROOT);

    }
    public function setSource($source) {

        $this->source = $source;
        $this->stream = file_get_contents($source);

    }
    public function load($data) {

        foreach($data as $k => $v){

            $this->stream = str_replace('{{'.$k.'}}', $v, $this->stream);

        }

    }
    public function setAssetsDir($dir)
    {

        if (!empty($_SERVER['PATH_INFO'])) {

            $dir = preg_replace('/\/index\.php\/\w+\/\w+\//', '', rtrim($_SERVER['REQUEST_URI'], '/') . '/');
            $this->assetsDir = $dir;
            return ;
        }

        $dir = rtrim($dir, '/') . '/';
        $this->assetsDir = $dir;
        
    }
    public function fixPaths(){

        $regexp = '!(src|href)=(["\']?)([a-z0-9/\:_.-]+)(["\'\s>])!i';
        return preg_replace_callback($regexp, [$this, 'fileCallback'], $this->stream);
    
    }
    public function fileCallback($matches){

        $file = $matches[3];
        if (preg_match('/\.(js|css|less|ico|png|svg|jpeg)$/', $file)) {
            $file = $this->fileMod($file);
        }
        return $matches[1] . '=' . $matches[2] . $file . $matches[4];
    
    }
    public function fileMod($file){

        $time  = 0;
        if($file[0] != '/'){
            if ($time = @filemtime($this->assetsDir . $file)) {
                $file .= '?s=' . $time;
            }
        }
        else{
            if ($time = @filemtime(ROOT . $file)) {
                $file .= '?s=' . $time;
            }
        } 
        return $file;
        
    }
    public function render($data) {

        $this->load($data);
        $this->stream = $this->fixPaths();

    }
    public function __destruct(){

        if($this->debug) {
            echo "========== DEBUG Start ==========\n";
            echo file_get_contents($this->source);
            echo "========== DEBUG End ==========\n";
        }
        echo $this->stream;
        
    }

}