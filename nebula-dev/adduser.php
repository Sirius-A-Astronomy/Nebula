<?php
  try
{

class MyDB extends SQLite3 {
   function __construct() {
      $this->open('nebula.db');
   }
}

//open the database
$db = new MyDB();
if(!$db) {
   echo $db->lastErrorMsg();
}

$username = $_POST["username"];
$time     = date("Y-m-d H:i:s");

//Insert record

$db->exec("INSERT INTO users (username, date_added) VALUES ('$username', '$time');");

//now output the data to a simple html table...

$db = NULL;
}
catch(PDOException $e)
{
print 'Exception : ' .$e->getMessage();
}

$pagetitle = $title.'User created! - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="submit.php"><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
        <form action="newuser.php" id="submit" method="post" name="user_form" role="form">
        <h1>New user added!</h1>

        <p>
          Your user, <?php echo $username; ?>, has been created!
        </p>

      </form>
    </section>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
