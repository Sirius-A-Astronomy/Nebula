<?php

$pagetitle = $title.'Nebular LaTeX - Nebula';

include_once 'assets/php-includes/head.php';

?>
  <div class="back-arrow">
    <a href="submit.php"><i class="material-icons">arrow_back</i></a>
  </div>
  <main id="Main" class="question">
    <section>
      <h2>Nebular LaTeX</h2>
      <p>
        The Nebula uses the open-source JavaScript display engine <span class="code">MathJax</span> to display your LaTeX code. It however has some peculiarities you should keep in mind.
      </p>

      <h3>Important things to keep in mind</h3>
      <p>
        You have to explicitly declare new paragraphs with <span class="code">\par</span>
      </p>
      <p>
        The <span class="code tex2jax_ignore">enumerate</span> environment is enabled in the Nebula for numbered lists in your questions. So:
        <br><br><span class="code tex2jax_ignore" >\begin{enumerate} <br> \item ... <br> \item ... <br> \end{enumerate}</span><br><br>
        <i>should</i> work (if you typed it right).
      </p>
      <h3>Package and custom command support</h3>
      <p>
        The packages <span class="code">physics</span>, except all its matrix commands, and <span class="code">siunitx</span> are enabled.
      </p>
      <p>
        You can declare new commands using commands like <span class="code">\newcommand</span>, but you have to wrap it in math delimiters (so <span class="code tex2jax_ignore">$\newcommand ... $</span>).
      </p>
      <h3>Smart tips for tough-cookie Nebular writers.</h3>
      <p>
        You can use the 'preview' button to see if your LaTeX code works, it will open a seperate window, but keeps your original code here.
      </p>
      <p>
      Your questions are not saved if you close the submission page, it may be advised to first create your question in a seperate LaTeX environment, that autosaves (like Overleaf).
      </p>
      <h3>External urls and images</h3>
      <p>
        You can add external links to your questions with the LaTeX quasi-code:<br>
        <br><span class="code tex2jax_ignore" >\begin{url} <br> ... your url ... <br> \end{url}</span>
      </p>
      <p>
        You can add externally hosted images to your questions with: <br>
        <br><span class="code tex2jax_ignore" >\begin{imgurl} <br> ... your url ... <br> \end{imgurl}</span>
      </p>
    </section>
  </main>

<?php


include_once 'assets/php-includes/foot.php';

?>
