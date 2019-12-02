<?php /*
$dir = new DirectoryIterator($dir[0]);
foreach ($dir as $fileinfo) {
  if (!$fileinfo->isDot()) { ?>
    <div class="understik-list">
      <div class="understik-ikoan-container">
        <i class="material-icons understik-ikoan">attachment</i>
      </div>
      <div class="understik-tekst-container">
        <p class="understik-tekst"><a href=<?php echo $fileinfo->getPathname() ?> target='blank_' ><?php echo $fileinfo->getFilename() ?></a></p>
      </div>
      <div class="understik-tekst-container" style="margin-left: auto; margin-right: 16px;">
        <p class="understik-tekst" style="opacity: 0.34; font-weight: 400;"><?php echo date('d/m/y', $fileinfo->getMTime()) ?></p>
      </div>
    </div> <?php
  }
} */
?>
<div class="back-arrow">
  <a href="../"><i class="material-icons">arrow_back</i></a>
</div>
<main id="Main">
  <section>
    <h1 style="align-self: center;">\Nebula</h1>
    <p class="intro">
      <?php echo $intro; ?>
    </p>
  </section>
  <section>
    <?php
    // Initiate array
    $Files = array();

    // Iterate over the directory
    foreach (new DirectoryIterator('.') as $fileInfo) {

    if($fileInfo->isDot()) continue;
    if($fileInfo->isFile()) continue;

    $fileName = $fileInfo->getFilename();
    $fileHuman = str_replace("_", " ", $fileName);

    $dirs[] = array(
                        "humanName" => $fileHuman,
                        "dirName"   => $fileName
                     );
    };

    // Sort alphabetically
    asort( $dirs );

    // Print
    foreach ($dirs as $dir) {
      /*Card Element*/
      $cardlink     =   $dir["dirName"];
      $cardtitle    =   $dir["humanName"];
      $cardimage    =   '';
      include "../assets/php-includes/card.php";
    }
    ?>
  </section>
</main>
