<?php

$level_id = htmlspecialchars($_GET["level_id"]);


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
   SELECT * FROM levels WHERE level_id=$level_id;
EOF;

$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $level_id = $row['level_id'];
   $level_name = $row['level_name'];
   $study_type = $row['study_type'];
}


$sql =<<<EOF
   SELECT * FROM courses WHERE level_id=$level_id;
EOF;

$ret = $db->query($sql);


$pagetitle = $level_name . ', ' . $study_type . ' - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="index.php"><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
      <h1 style="margin-bottom: 0;"><?php echo $study_type . " - " . $level_name ?></h1>
    </section>
    <div class="divider"></div>
    <section style="padding: 0;">
      <div class="list">
        <div><span class='title'>Course</span></div>
        <?php
        while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
           $course_id = $row['course_id'];
           $level_id = $row['level_id'];
           $course_name = $row['course_name'];
           $course_abbr = $row['course_abbr'];
           $course_descr = $row['course_descr'];
           echo "<a href='course.php?course_id=" . $course_id . "'><span>"  . $course_name . "</span></a>";

        }
         ?>
      </div>
    </section>

  </main>

<?php
$db->close();
include_once 'assets/php-includes/foot.php';

?>
