<?php
	$name = $_GET["name"];
	$address = $_GET["address"];
	$phone = $_GET["phone"];
	$save = $_GET["save"];
	$body = "$name \n $address \n $phone";
	$stm = "INSERT INTO addressText (Name, Address, Phone) VALUES('$name', '$address', '$phone')";
	$to = "*******@vtext.com";//cellphone number must be added
	$subject = "Address";

	if (mail($to, $subject, $body)) { //sends text message with address
	   echo("<p>Message successfully sent!</p>");
	  } else {
	   echo("<p>Message delivery failed...</p>");
	  }

        if ($save == "yes"){              //enters new addresses to db
		$dbhandle = sqlite_open('db/test.db', 0666, $error);

		if (!$dbhandle) die ($error);
	    
		$ok = sqlite_exec($dbhandle, $stm);
		if (!$ok) die("Cannot execute statement.");

		echo "Data inserted successfully";

		sqlite_close($dbhandle);
        }
?>
