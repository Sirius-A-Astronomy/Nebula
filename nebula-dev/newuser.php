<?php

class MyDB extends SQLite3 {
   function __construct() {
      $this->open('nebula.db');
   }
}

$db = new MyDB();
if(!$db) {
   echo $db->lastErrorMsg();
}

$sql =<<<EOF
   SELECT user_id, username FROM users;
EOF;


$users = array();
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $users[] = array($row['user_id'], $row['username']);
}

$sql =<<<EOF
   SELECT course_id, course_name FROM courses;
EOF;


$courses = array();
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $courses[] = array($row['course_id'], $row['course_name']);
}

$db->close();

$pagetitle = $title.'Create a new user - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="submit.php"><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
        <form action="adduser.php" id="submit" method="post" name="user_form" role="form">
        <h1>Add a new user</h1>


        <p>
          Your username will be used to track how many questions you have submitted.
        </p>

        <div class="group textinput">
          <input type="text" name="username" required>

          <label for="username">Username<span class="requiredtext">*</span></label>
          <span class="highlight"></span>
          <span class="bar"></span>
        </div>
        <div>
            <button type="submit">Add</button>
        </div>
      </form>
    </section>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
