<?php

$pagetitle = $title.'Index - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="https://www.astro.rug.nl/intranet/siriusa/"><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
      <p>
        This is the Nebula Database by the Kapteyn Learning Community.
      </p>
      <p>
        It is a repository of user-submitted practice questions.
      </p>
    </section>
    <div class="divider"></div>
    <section>
      <h2>Browse the Nebula</h2>
      <h3>Bachelor</h3>
      <p><a href="level.php?level_id=1">1st year</a></p>
      <p><a href="level.php?level_id=2">2nd year</a></p>
      <p><a href="level.php?level_id=3">3rd year</a></p>
      <h3>Master</h3>
      <p><a href="level.php?level_id=4">Courses</a></p>
    </section>
    <div class="divider"></div>
    <section>
      <p><a href="submit.php">Add a question</a></p>
    </section>
  </main>

<?php

include_once 'assets/php-includes/foot.php';

?>
