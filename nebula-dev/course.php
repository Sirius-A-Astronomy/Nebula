<?php

$course_id = htmlspecialchars($_GET["course_id"]);


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
   SELECT * FROM courses WHERE course_id=$course_id;
EOF;

$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $course_id = $row['course_id'];
   $level_id = $row['level_id'];
   $course_name = $row['course_name'];
   $course_abbr = $row['course_abbr'];
   $course_descr = $row['course_descr'];
}


$sql =<<<EOF
   SELECT * FROM questions WHERE course_id=$course_id;
EOF;

$ret = $db->query($sql);


$pagetitle = $course_name.' - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href=<?php echo "level.php?level_id=" . $level_id ?>><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
      <h1 style="margin-bottom: 0;"><?php echo $course_name ?></h1>
      <p style="padding-top: 16px;"><?php echo $course_descr ?></p>
    </section>
    <section style="padding:0;">
      <div class="list">
        <div><span class='title'>Title</span><span class='time'>Added</span></div>

          <?php
          while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
             $title = $row['title'];
             $question_id = $row['question_id'];
             $subject = $row['subject'];
             $type_of_question = $row['type_of_question'];
             $date_added =  $row['date_added'];
             echo "<a href='question.php?question_id=" . $question_id . "'><span class='title'>" . $title . "</span><div class='descript'><span class='subject'><b>Subject: </b>" . $subject . "</span><span class='type'><b>Type: </b>" . $type_of_question . "</span></div><span class='time'>" . $date_added . "</span></a>";
          }
           ?>
      </div>
    </section>
  </main>

<?php
$db->close();
include_once 'assets/php-includes/foot.php';

?>
