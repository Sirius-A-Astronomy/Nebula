<?php

$time = date("Y-m-d H:i:s");
$time = substr($time, 8, 2) . "/" . substr($time, 5, 2) . "/" . substr($time, 0, 4);

$user_id = $_POST["user"];
$title = $_POST["title"];
$course_id = $_POST["course"];
$subject = $_POST["subject"];
$type_of_question = $_POST["type_of_question"];
$source = $_POST["source"];

$questiontext = "<p>".str_replace("\par","</p><p>",stripslashes($_POST["questiontext"]))."</p>";
$answertext = "<p>".str_replace("\par","</p><p>",stripslashes($_POST["answertext"]))."</p>";

$questiontext = str_replace("'", "''", $questiontext);
$answertext = str_replace("'", "''", $answertext);


function str_replace_first($from, $to, $content, $limit)
{
    $from = '/'.preg_quote($from, '/').'/';

    return preg_replace($from, $to, $content, $limit);
}


$questiontext = str_replace("\begin{url}", '<a target="_blank" href="', $questiontext);
$questiontext = str_replace("\end{url}", '"><i class="material-icons">link</i></a>', $questiontext);

$answertext = str_replace("\begin{url}", '<a target="_blank" href="', $answertext);
$answertext = str_replace("\end{url}", '"><i class="material-icons">link</i></a>', $answertext);

$questiontext = str_replace("\begin{imgurl}", '<img style="width: 100%;" src="', $questiontext);
$questiontext = str_replace("\end{imgurl}", '">', $questiontext);

$answertext = str_replace("\begin{imgurl}", '<img style="width: 100%;" "', $answertext);
$answertext = str_replace("\end{imgurl}", '">', $answertext);

$questiontext = str_replace("\begin{enumerate}", "<ol><li>", $questiontext);
$questiontext = str_replace_first("\item", "", $questiontext, 1);
$questiontext = str_replace_first("\item", "</li><li>", $questiontext, $questiontext.count("\item") - 1);
$questiontext = str_replace_first("\end{enumerate}", "</li></ol>", $questiontext, 1);

$answertext = str_replace("\begin{enumerate}", "<ol><li>", $answertext);
$answertext = str_replace_first("\item", "", $answertext, 1);
$answertext = str_replace_first("\item", "</li><li>", $answertext, $answertext.count("\item") - 1);
$answertext = str_replace_first("\end{enumerate}", "</li></ol>", $answertext, 1);

class MyDB extends SQLite3 {
   function __construct() {
      $this->open('nebula.db');
   }
}

/* INITIAL FILL */

$db = new MyDB();
if(!$db) {
   echo $db->lastErrorMsg();
}

$sql =<<<EOF
   SELECT username FROM users WHERE user_id=$user_id;
   SELECT course_name FROM courses WHERE course_id=$course_id;
EOF;


$users = array();
$usersassoc = array();
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $username = $row['username'];
   $coursename = $row['course_name'];
}

if($_POST["Submit"]) {
  //User hit the Submit for Approval button, handle accordingly

  $sql =<<<EOF
      INSERT INTO questions (course_id, user_id, title, date_added, type_of_question, subject, question, answer, source)
      VALUES ('$course_id', '$user_id', '$title', '$time', '$type_of_question', '$subject', '$questiontext', '$answertext', '$source');
EOF;

$ret = $db->exec($sql);
   if(!$ret) {
      echo $db->lastErrorMsg();
   } else {
  }
}

$db->close();

$pagetitle = 'PREVIEW: '.$title.' - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="."><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <?php
    // PREVIEW
    if($_POST["Submit"]) {
      //User hit the Submit for Approval button, handle accordingly
      echo '<section>
        <h1>Your question has been added!</h1>

        <p>
          Your question titled, '.$title.', has been added!
        </p>
      </section>';

      $pagetitle = 'Submitted successfully: '.$title.' - Nebula';

    }

    if($_POST["preview"]) {
      echo '<div class="preview">
        <span class="previewtext">Preview - Course: '.$coursename.'</span>
        <section>
          <h1>'.$title.'</h1>
          <div class="metadata">
            <span class="info">By: '.$author.' | Submitted: '.$date_added.'</span>
            <span class="info">Type: '.$type_of_question.' | Subject: '.$subject.'</span>
          </div>

        <div class="questiontext">
          <h3>The question:</h3>
          '.$questiontext.'
        </div>
        <h3>Solution:</h3>
        <div id="answertext" class="answertext">
          '.$answertext.'
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
        <div class="source"><span class="info">Source:'.$source.' ?></span></div>
      </div>';
    };
    ?>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
