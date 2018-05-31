<?php
$hashtags = $_GET['hashtags'];


//echo("hello world");
//echo($hashtags);
//echo("            a                   ");
$searches = split("-" , $hashtags);

foreach ($searches as $hold){
	//echo($hold);
	$link = "https://enigmatic-falls-63876.herokuapp.com/tweets/";
	$search = $link . $hold;
	//echo("   ");
	//echo($search);
	$coordinates .= file_get_contents($search);
	$coordinates .= ",";
}

echo(str_replace(array( '(', ')', '[', ']'), '', $coordinates));

//echo(str_replace('['$coordinates));

?>