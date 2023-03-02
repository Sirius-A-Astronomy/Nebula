# Writing Markdown and LaTeX in Nebula

<script setup lang="ts">
    import MarkdownEditor from '@components/MarkdownEditor.vue'
</script>



Nebula uses [Markdown](https://www.markdownguide.org/) to format text. Markdown is a lightweight markup language with plain text formatting syntax. It is designed so that it can be converted to HTML and many other formats using a tool by the same name. Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

Nebula uses [Mathjax](https://www.mathjax.org/) to render LaTeX math. This means that you can write LaTeX math in your markdown.

::: tip Interactive examples
All examples in this page are interactive. Feel free to play around with them!

Select the `Source` tab to see the markdown source code or select `Side-by-side` to see the rendered markdown and the source code side-by-side.
:::

#### Table of contents
[[toc]]

::: tip Learn more
Sirius A organises a Yearly LaTeX workshop. Keep an eye on the Sirius A announcements chat for more information.

For more information on Markdown, see [Markdown Documentation](https://www.markdownguide.org/).

For more information on Latex, see [here](https://www.overleaf.com/learn/latex/Mathematical_expressions).

For more information on Mathjax, see [here](https://www.mathjax.org/).
:::

## Writing Mathemathics in Nebula


While nebula uses latex style notation for math, not all latex commands are supported. For a list of supported commands, see [here](https://docs.mathjax.org/en/latest/input/tex/macros/index.html). Some notations are slightly different as well. So if you're having trouble with a specific command, take a look at the documentation below, look at documentation for mathjax, or contact Cosmic Web.

Some things to keep in mind:
- You might have to escape `\` characters. For example, in matrices you have to write `\\\\` instead of `\\` to add a new row.

:::tip LaTeX Math Cheat Sheet
A nice LaTeX math cheat sheet can be found [here](https://www.authorea.com/users/77723/articles/110898-how-to-write-mathematical-equations-expressions-and-symbols-with-latex-a-cheatsheet-with-examples).
:::
:::tip Advanced math
More advanced math can be found below in the [More mathematical typesetting](#more-mathematical-typesetting) section.
:::

### Inline math
Inline math is written between dollar signs. For example:

```md
$ x^2 + y^2 = z^2 $
```

... will render as:
<MarkdownEditor 
    preset="docs"
    :content="`$ x^2 + y^2 = z^2 $`"/>

### Display math

Display math is written between double dollar signs. Display math is centered and takes up the full width of the page.

For example:

```md
$$ x^2 + y^2 = z^2 $$
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`$$ x^2 + y^2 = z^2 $$`"/>

### Numbered equations

Numbered equations are written between `\begin{equation}` and `\end{equation}`. For example:

```md
\begin{equation}
    x^2 + y^2 = z^2
\end{equation}

\begin{equation}
    x^2 + y^2 = z^2
\end{equation}
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`\\begin{equation}
    x^2 + y^2 = z^2
\\end{equation}
\
\\begin{equation}
    x^2 + y^2 = z^2
\\end{equation}`"/>

#### References

You can reference numbered equations using `\eqref{}` or `\ref{}`. For example:

```md
\begin{equation}
    x^2 + y^2 = z^2
\label{eq:pythagorean}
\end{equation}

\begin{equation}
    x^2 + y^2 = z^2
\label{eq:pythagorean2}
\end{equation}

Equation \eqref{eq:pythagorean} is the same as equation \eqref{eq:pyrhagorean2}.
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`\\begin{equation}
    x^2 + y^2 = z^2
\\label{eq:pythagorean}
\\end{equation}
\n
\\begin{equation}
    x^2 + y^2 = z^2
\\label{eq:pythagorean2}
\\end{equation}
\n
Equation \\eqref{eq:pythagorean} is the same as equation \\eqref{eq:pythagorean2}.`"/>



## Formatting text with markdown

### Headers

Headers are written with the `#` symbol. The number of `#` symbols determines the size of the header. 

```md
# Header

## Subheader

### Subsubheader
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`# Header
\n
## Subheader
\n
### Subsubheader`"
/>

### Lists


#### Unordered lists

Unordered lists are written with the `-` symbol.

```md
- Item 1
- Item 2
- Item 3
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`- Item 1
- Item 2
- Item 3`"
/>


#### Ordered lists

To create an ordered list use `1.` for each item.

```md
1. Item 1
1. Item 2
1. Item 3
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`1. Item 1
1. Item 2
1. Item 3`"/>


### Images

Images are written with the following syntax:

```md
![Image description](https://example.com/image.png)
```

::: details Example
<MarkdownEditor 
    preset="docs"
    :content="`![A neutron star](https://upload.wikimedia.org/wikipedia/commons/1/1d/Neutron_Star_simulation.png)`"
/>
:::

### Links

Links are written with the following syntax:

```md
[Link description](https://example.com)
```

::: details Example
<MarkdownEditor 
    preset="docs"
    :content="`[Sirius A](https://siriusa.nl)`"
/>
:::

### Tables

Tables are written with the following syntax:

```md
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Item 1   | Item 2   | Item 3   |
| Item 4   | Item 5   | Item 6   |
```

... will render as:

<MarkdownEditor 
    preset="docs"
    :content="`\
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Item 1   | Item 2   | Item 3   |
| Item 4   | Item 5   | Item 6   |`"
/>

::: tip More information

More information on tables can be found [here](https://www.markdownguide.org/extended-syntax/#tables).
:::

### Code

#### Inline code

Inline code is written between backticks.

```md
This is a line with `inline code`!
```

... will render as:

<MarkdownEditor
    preset="docs"
    :content="`This is a line with \`inline code\`!`" />

#### Code blocks

Code blocks are written between triple backticks.

````md
```
def function():
    print("This is a code block!")
```
````

##### Syntax highlighting
A language can be specified after the first set of backticks. This will enable syntax highlighting.


````md
```python
def function():
    print("This is a python code block!")
```

```c
#include<stdio.h>

int main() {
    printf("Hello World with C!");
    return 0;
}
```
````

... will render as:

<MarkdownEditor
    preset="docs"
    :options="{
        tabToIndentToggle: true,
        }"
    :content="`\`\`\`python
def function():
    print('This is a python code block!')
\`\`\`\n
\`\`\`c
#include<stdio.h>\n
int main() {
	printf('Hello World with C!');
	return 0;
}
\`\`\``" />

::: details Supported languages
A list of supported languages can be found [here](https://github.com/shikijs/shiki/blob/main/packages/shiki/src/languages.ts).
:::

## More mathematical typesetting

The following examples will only be shown in the editor. To look at the source code, select the `Source`  or `Side-by-side` tab.

:::info Source
These examples were adapted from [this](https://www.authorea.com/users/3/articles/165181-latex-mathematics-examples) page.
:::


### Equations
<MarkdownEditor
    preset="docs"
    :content="`A simple equation:
\\begin{equation}
 f(x)=(x+a)(x+b)
\\end{equation}
An equation with text:
\\begin{equation}
50 \\text{ apples} \\times 100 \\text{ apples} =
\\textbf{lots of apples}
\\end{equation}
\n
One including subscripts and superscripts:
\\begin{equation}
k_{n+1} = n^2 + k_n^2 - k_{n-1} 
\\end{equation}
`"/>




### Greek Letters

<MarkdownEditor
    preset="docs"
    :content="`$$ \\alpha, \\beta, \\gamma, \\Gamma, \\pi, \\Pi, \\phi, \\varphi, \\mu, \\Phi, \\xi, \\zeta $$
$$ \\cos(2\\theta\\phi) = \\cos^2 \\theta\\phi - \\sin^2 \\theta\\phi $$`"/>

### Delimiters

<MarkdownEditor
    preset="docs"
    :content="`There are many types of delimiters one can use:
$$ ( a ), [ b ], \\{ c \\}, | d |, \\| e \\|,
\\langle f \\rangle, \\lfloor g \\rfloor,
\\lceil h \\rceil, \\ulcorner i \\urcorner $$
\n
See how the delimiters are of reasonable size in these examples
\\begin{equation}
\\left(a+b\\right)\\left[1-\\frac{b}{a+b}\\right]=a,
\\end{equation}
\\begin{equation}
\\sqrt{|xy|}\\leq\\left|\\frac{x+y}{2}\\right|,
\\end{equation}
\n
even when there is no matching delimiter
\n
\\begin{equation}
\\int_a^bu\\frac{d^2v}{dx^2}\\,dx
=\\left.u\\frac{dv}{dx}\\right|_a^b
-\\int_a^b\\frac{du}{dx}\\frac{dv}{dx}\\,dx.
\\end{equation}
\n
whereas vector problems often lead to statements such as
\\begin{equation}
u=\\frac{-y}{x^2+y^2}\\,\\quad
v=\\frac{x}{x^2+y^2}\\,\\quad\\text{and}\\quad
w=0\\.
\\end{equation}
`"/>

### Multiple Fractions

<MarkdownEditor
    preset="docs"
    :content="`
Typesetting continued fractions is easy:
\n
\\begin{equation}
x = a_0 + \\frac{1}{a_1 + \\frac{1}{a_2 + \\frac{1}{a_3 + a_4}}}
\\end{equation}
\n
However, as the fractions continue, they get smaller. If you want to keep the size consistent, use the display style; e.g.
\\begin{equation}
  x = a_0 + \\frac{1}{\\displaystyle a_1
          + \\frac{1}{\\displaystyle a_2
          + \\frac{1}{\\displaystyle a_3 + a_4}}}
\\end{equation}
`"/>

### Arrays

<MarkdownEditor
    preset="docs"
    :content="`
Arrays of mathematics are typeset using one of the matrix environments as
in:
\\begin{equation}
\\begin{bmatrix}
        1 & x & 0 \\\\\\\\
        0 & 1 & -1
\\end{bmatrix}\\begin{bmatrix}
        1  \\\\\\\\
        y  \\\\\\\\
        1
\\end{bmatrix}
=\\begin{bmatrix}
        1+xy  \\\\\\\\
        y-1
\\end{bmatrix}.
\\end{equation}
\n
\\begin{equation}
\\begin{pmatrix}
2 & 3 & 4\\\\\\\\
5 & 6 & 7\\\\\\\\
8 & 9 & 10 \\end{pmatrix} v = 0 
\\end{equation}
\n
Case statements use cases:
\\begin{equation}
|x|=\\begin{cases}
        x, & \\text{if }x\\geq 0\,  \\\\\\\\
        -x, & \\text{if }x< 0\\.
\\end{cases}
\\end{equation}
\n
Many arrays have lots of dots all over the place as in
\\begin{equation}
\\begin{matrix}
    -2 & 1 & 0 & 0 & \\cdots & 0  \\\\\\\\
     1 & -2 & 1 & 0 & \\cdots & 0  \\\\\\\\
     0 & 1 & -2 & 1 & \\cdots & 0  \\\\\\\\
     0 & 0 & 1 & -2 & \\ddots & \\vdots \\\\\\\\
     \\vdots & \\vdots & \\vdots & \\ddots & \\ddots & 1  \\\\\\\\
     0 & 0 & 0 & \\cdots & 1 & -2
\\end{matrix}
\\end{equation}
`"/>

### Accents
<MarkdownEditor
    preset="docs"
    :content="`
Mathematical accents are performed by a short command with one
argument, such as
\\begin{equation}
\\tilde f(\\omega)=\\frac{1}{2\pi}
\\int_{-\\infty}^\\infty f(x)e^{-i\\omega x}dx,
\\end{equation}
or
\\begin{equation}
\\dot{\\vec \\omega}=\\vec r\\times\\vec I.
\\end{equation}
`"/>

### Sets, Proofs, and Logic
<MarkdownEditor
    preset="docs"
    :content="`
For any nonnegative integer $n$, we have
\\begin{equation}
(1+x)^n = \\sum_{i=0}^n {n \\choose i} x^i
\\end{equation}
\n
The Taylor series expansion for the function $e^x$ is given by
\\begin{equation}
e^x = 1 + x + \\frac{x^2}{2} + \\frac{x^3}{6} + \\cdots = \\sum_{n\\geq 0} \\frac{x^n}{n!}
\\end{equation}
\\begin{equation}
\\forall x \\in X, \\quad \\exists y \\leq \\epsilon
\\end{equation}
\\begin{equation}
\\frac{n!}{k!(n-k)!} = \\binom{n}{k}
\\end{equation}
\n
For any sets $A$, $B$ and $C$, we have
\\begin{equation}
(A\\cup B)-(C-A) = A \\cup (B-C)
\\end{equation}
`"/>
