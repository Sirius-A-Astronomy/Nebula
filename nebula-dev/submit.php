<?php

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
   SELECT user_id, username FROM users;
EOF;


$users = array();
$usersassoc = array();
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $users[] = array($row['user_id'], $row['username']);
   $usersassoc[] = array($row['user_id'] => $row['username']);
}

$sql =<<<EOF
   SELECT course_id, course_name FROM courses;
EOF;


$courses = array();
$ret = $db->query($sql);
while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
   $courses[] = array($row['course_name'], $row['course_id']);
};

sort($courses);

if($_POST["approve"]) {
  //User hit the Submit for Approval button, handle accordingly
}


$db->close();

$pagetitle = $title.'Submit a question - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="."><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <?php
    // PREVIEW

    if($_POST["preview"]) {
      $time = date("Y-m-d H:i:s");
      $time = substr($time, 8, 2) . "/" . substr($time, 5, 2) . "/" . substr($time, 0, 4);

      $user_id = $_POST["user"];
      $title = $_POST["title"];
      $course_id = $_POST["course"];
      $subject = $_POST["subject"];
      $type_of_question = $_POST["type_of_question"];
      $source = $_POST["source"];
      $questiontext = "<p>".str_replace("\par","</p><p>",stripslashes($_POST["questiontext"]))."</p>";
      $answertext = $_POST["answertext"];

      echo '<div class="preview">
        <span class="previewtext">Preview</span>
        <section><h1>'.$title.'</h1></section>
        <section>
          <span class="info">By: '.$usersassoc[$user_id].' | Submitted: '.$time.'</span>
          <span class="info">Type:'.$type_of_question.' | Subject: '.$subject.'</span>
        </section>
        <section class="questiontext">
          <h3>The question:</h3>
          '.$questiontext.'
        </section>
        <div class="divider"></div>
        <section class="answertext">
          <h3>Solution:</h3>
          '.$answertext.'
        </section>
        <section>
          <span class="info">Source '.$source.'</span>
        </section>
      </div>';
    };
    ?>
    <section>
        <form action="preview.php"  target="_blank" class="form-horizontal" id="submit" method="post" name="register_form" role="form">
        <h1>Submit a question</h1>
        <span class="requiredtext" style="margin-bottom:16px;">*required</span>
        <p>
          Here you can submit your question, it will first be reviewed by members of the KLC.

        </p>
        <h3>Identifier</h3>

        <p>
          Your username will be used to track how many questions you have submitted.
        </p>

        <div class="mdl-selectfield group ">
            <label for="course required">Username<span class="requiredtext">*</span></label>
            <select id="user" name="user" required>
              <option value="" disabled invalid selected></option>
              <?php
              foreach ($users as $user) {
                echo "<option value='".$user[0]."'>".$user[1]."</option>";
              }
              ?>
            </select>

        </div>

        <p style="display: flex; align-items: center;">
          <a href="newuser.php" target="_blank"><i class="material-icons" style="font-size: 16px;">add</i> Add a new user</a>
        </p>

        <h3>Question details</h3>

        <p>
          This is the additional data that makes your question easy to find.
        </p>

        <div class="group textinput">
          <input name="title" type="text" required>
          <label>Title<span class="requiredtext">*</span></label>
          <span class="highlight"></span>
          <span class="bar"></span>
        </div>

        <div class="mdl-selectfield group">
            <label for="course">Course<span class="requiredtext">*</span></label>
            <select id="course" name="course" class="browser-default" required>
              <option value="" disabled selected></option>
              <?php
              foreach ($courses as $course) {
                echo "<option value='".$course[1]."'>".$course[0]."</option>";
              }
              ?>
            </select>
        </div>

          <div class="group textinput">
            <input name="subject" type="text">
            <label>Subject </label>
            <span class="highlight"></span>
            <span class="bar"></span>
          </div>
          <span class="helpertext">(e.g. Cosmic dynamics, Mathematical induction)</span>

          <div class="group textinput">
            <input name="type_of_question" type="text">
            <label>Question type </label>
            <span class="highlight"></span>
            <span class="bar"></span>
          </div>
          <span class="helpertext">(e.g. Conceptual question, Derivation, Calculation)</span>

          <div class="group textinput">
            <input name="source" type="text">
            <label>Source(s)</label>
            <span class="highlight"></span>
            <span class="bar"></span>
          </div>
          <span class="helpertext">(e.g. Morrison, Wikipedia)</span>

          <h3>Question content</h3>
          <a></a>
          <p>
            This is written using modified LaTeX code, <a href="latexsupport.php" target="_blank">an explanation here</a>.
          </p>


          <div class="group textinput">
            <label >The question<span class="requiredtext">*</span></label>
            <textarea style="margin-top: 8px;" name="questiontext" type="text" required></textarea>

            <span class="highlight"></span>
            <span class="bar"></span>
          </div>

          <div class="group textinput">
            <label >The answer<span class="requiredtext">*</span></label>
            <textarea style="margin-top: 8px;" name="answertext" type="text" required></textarea>

            <span class="highlight"></span>
            <span class="bar"></span>
          </div>

          <div class="submitter">
            <input type="submit" value="Preview" name="preview"/>
            <input type="submit" value="Submit" name="Submit" />
          </div>
      </form>
    </section>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
