<?php

namespace Models;

class FileModel {

	public function __construct(){}

	public function createFile($filePath, $fileContents){

		return @file_put_contents($filePath, $fileContents);

	}
	public function getFile($filePath){

		return @file_get_contents($filePath);
	
	}
	public function copyFile($filePathSrc, $filePathDst){

		return copy($filePathSrc, $filePathDst);

	}
	public function createDir($dirPath){

		return mkdir($dirPath, 0777);
	
	}

}
