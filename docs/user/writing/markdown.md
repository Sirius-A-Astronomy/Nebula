# Writing Markdown and LaTeX in Nebula

<script setup lang="ts">
    import MarkdownEditor from '../../../nebula/src/js/components/MarkdownEditor.vue'
</script>



Nebula uses [Markdown](https://www.markdownguide.org/) to format text. Markdown is a lightweight markup language with plain text formatting syntax. It is designed so that it can be converted to HTML and many other formats using a tool by the same name. Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

Nebula uses [Mathjax](https://www.mathjax.org/) to render LaTeX math. This means that you can write LaTeX math in your markdown.

#### Table of contents
[[toc]]

::: tip Learn more
Sirius A organises a Yearly LaTeX workshop. Keep an eye on the Sirius A announcements chat for more information.

For more information on Markdown, see [Markdown Documentation](https://www.markdownguide.org/).

For more information on Latex, see [here](https://www.overleaf.com/learn/latex/Mathematical_expressions).

For more information on Mathjax, see [here](https://www.mathjax.org/).
:::

## Writing Mathemathics in Nebula

### Inline math
Inline math is written between dollar signs. For example:

```
$ x^2 + y^2 = z^2 $
```

will render as:
<MarkdownEditor 
    :content="`$ x^2 + y^2 = z^2 $`"/>

### Display math

Display math is written between double dollar signs. Display math is centered and takes up the full width of the page.

For example:

```
$$ x^2 + y^2 = z^2 $$
```

will render as:

<MarkdownEditor 
    :content="`$$ x^2 + y^2 = z^2 $$`"/>

## Formatting text with markdown

### Headers

Headers are written with the `#` symbol. The number of `#` symbols determines the size of the header. 

```
# Header

## Subheader

### Subsubheader
```

will render as:

<MarkdownEditor 
    :content="`# Header
\n
## Subheader
\n
### Subsubheader`"
/>

### Lists


#### Unordered lists

Unordered lists are written with the `-` symbol.

```
- Item 1
- Item 2
- Item 3
```

... will render as:

<MarkdownEditor 
    :content="`- Item 1
- Item 2
- Item 3`"
/>


#### Ordered lists

To create an ordered list use `1.` for each item.

```
1. Item 1
1. Item 2
1. Item 3
```

... will render as:

<MarkdownEditor 
    :content="`1. Item 1
1. Item 2
1. Item 3`"/>


### Images

Images are written with the following syntax:

```
![Image description](https://example.com/image.png)
```

::: details Example
<MarkdownEditor 
    :content="`![A neutron star](https://upload.wikimedia.org/wikipedia/commons/1/1d/Neutron_Star_simulation.png)`"
/>
:::

### Links

Links are written with the following syntax:

```
[Link description](https://example.com)
```

::: details Example
<MarkdownEditor 
    :content="`[Sirius A](https://siriusa.nl)`"
/>
:::

### Tables

Tables are written with the following syntax:

```
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Item 1   | Item 2   | Item 3   |
| Item 4   | Item 5   | Item 6   |
```

... will render as:

<MarkdownEditor 
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

```
This is a line with `inline code`!
```

... will render as:

<MarkdownEditor
    :content="`This is a line with \`inline code\`!`" />

#### Code blocks

Code blocks are written between triple backticks.

````
```
def function():
    print("This is a code block!")
```
````

##### Syntax highlighting
A language can be specified after the first set of backticks. This will enable syntax highlighting.


````
```python
def function():
    print("This is a code block!")
```
````

... will render as:

<MarkdownEditor
    :options="{
        tabToIndentToggle: true,
        }"
    content="```python
def function():
    print('This is a code block!')
```
" />

::: details Supported languages
A list of supported languages can be found [here](https://github.com/shikijs/shiki/blob/main/packages/shiki/src/languages.ts).
:::


## Some examples of using markdown and LaTeX in Nebula

<MarkdownEditor 
    :content="`# This is an example of markdown and latex in Nebula
\n
As a test we're going to find the mass of a neutron star using the following equation:
\n
$$ M = \\frac{4 \\pi}{3} R^3 \\rho $$
\n
where $M$ is the mass of the neutron star, $R$ is the radius of the neutron star and $\\rho$ is the density of the neutron star.
\n
We can now use this equation to find the mass of a neutron star with a radius of 10 km and a density of 1.4 g/cm^3.
\
$$ M = \\frac{4 \\pi}{3} (10 \\text{ km})^3 (1.4 \\text{ g/cm}^3) = 1.4 \\times 10^6 \\text{ kg} $$
\
This is a pretty big mass!
\n
## Let's now add a picture of a neutron star
\n
![A neutron star](https://upload.wikimedia.org/wikipedia/commons/1/1d/Neutron_Star_simulation.png)
`"
/>