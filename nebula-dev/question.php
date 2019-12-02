<?php

$question_id = htmlspecialchars($_GET["question_id"]);


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
   SELECT * FROM questions WHERE question_id=$question_id;
EOF;

$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $title = $row['title'];
   $course_id = $row['course_id'];
   $user_id = $row['user_id'];
   $subject = $row['subject'];
   $type_of_question = $row['type_of_question'];
   $date_added = $row['date_added'];
   $question = $row['question'];
   $answer = $row['answer'];
   $source = $row['source'];
   $comment = $row['comment'];
}

$sql =<<<EOF
   SELECT username FROM users WHERE user_id=$user_id;
EOF;

$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $author = $row['username'];
}
$db->close();

$pagetitle = $title.' - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href=<?php echo "course.php?course_id=" . $course_id ?>><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
      <h1><?php echo $title ?></h1>
      <div class="metadata">
        <span class="info">By: <?php echo $author ?> | Submitted: <?php echo $date_added ?></span>
        <span class="info">Type: <?php echo $type_of_question ?> | Subject: <?php echo $subject ?></span>
      </div>

    <div class="questiontext">
      <h3>The question:</h3>
      <?php echo $question ?>
    </div>
    <h3>Solution:</h3>
    <div id="answertext" class="answertext">
      <?php echo $answer ?>
    </div>
    <script>
    function expandAnswer() {
            var x = document.querySelector("#answertext");
            var y = document.querySelector("#expand");
            var z = document.querySelector("#contract");
            x.style.maxHeight = "2500px";
            y.style.maxHeight = "0px";
            y.style.padding = "0";
            z.style.maxHeight = "32px";
            z.style.padding = "4px";
            };

    function contractAnswer() {
            var x = document.querySelector("#answertext");
            var y = document.querySelector("#expand");
            var z = document.querySelector("#contract");
            x.style.maxHeight = "0px";
            y.style.maxHeight = "32px";
            y.style.padding = "4px";
            z.style.maxHeight = "0px";
            z.style.padding = "0px";
            };
    </script>

    <div id="expand" onclick="expandAnswer()" class="expand material-icons">
      expand_more
    </div>
    <div id="contract" onclick="contractAnswer()" class="expand material-icons" style="max-height: 0px; padding: 0px;">
      expand_less
    </div>
    <div class="source"><span class="info">Source: <?php echo $source ?></span></div>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
