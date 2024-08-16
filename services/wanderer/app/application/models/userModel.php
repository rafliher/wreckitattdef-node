<?php

namespace Models;

class UserModel {

	private $file;

	public function __construct($file){

		$this->file = $file;

	}

	public function createUser($username, $password) {

		$uuid = exec("uuid");
		$hPassword = hash("sha256", $password);

		$filePath = "/tmp/${username}.user";
		$fileContents = "${uuid}|${hPassword}";

		$this->file->createFile($filePath, $fileContents);
		$this->file->createDir(ROOT . 'user/' . $uuid);

		return array("uuid" => $uuid, "username" => $username, "password" => $hPassword);

	}

	public function getUserByUsername($username) {

		$filePath = "/tmp/${username}.user";
		$fileContents = $this->file->getFile($filePath);

		if($fileContents == false)

			return false;

		$data = explode('|', $fileContents);
		
		return array("uuid" => $data[0], "username" => $username, "password" => $data[1]);

	}

}
