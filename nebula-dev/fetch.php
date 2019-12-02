
<?php
   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('nebula.db');
      }
   }

   $db = new MyDB();
   if(!$db) {
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully<br>";
   }

   $sql =<<<EOF
      SELECT * from questions;
EOF;

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
      echo "ID = ". $row['question_id'] . "<br>";
      echo "Title = ". $row['title'] ."<br>";
   }
   echo "Operation done successfully\n";
   $db->close();
?>
