<script setup lang="ts">
/*
    This component is used directly in the documentation.

    This is done to show how the current markdown would be rendered.

    To keep this possible relative imports are used as the
    docs don't have access to the aliases and have a different rootDir.
*/

import { onMounted, ref, watch, type Ref } from "vue";

import DOMPurify from "dompurify";

import { throttle } from "throttle-debounce";

import { useMathJax } from "../lib/mathjax";
import useMarkdown from "markdown-it";
import { BUNDLED_LANGUAGES } from "shiki";
import { getShikiHighlighter } from "../lib/highlighter";

const props = defineProps<{
  content: string;
  options?: {
    disableMathJax?: boolean;
    disableMarkdown?: boolean;
  };
}>();

let highlighter: any; // initialised in onMounted
let mathjax: any; // initialised in onMounted

const markdownElement: Ref<HTMLDivElement | null> = ref(null);
const sanitizedMarkdown: Ref<string> = ref("");

const markdown: any = useMarkdown({
  highlight: (str, lang) => {
    if (!str || !str.trim()) {
      return `<pre><code>${markdown.utils.escapeHtml(str)}</code></pre>`;
    }
    try {
      if (!highlighter.getLoadedLanguages().includes(lang)) {
        const bundles = BUNDLED_LANGUAGES.filter((bundle) => {
          // Languages are specified by their id, they can also have aliases (i. e. "js" and "javascript")
          return bundle.id === lang || bundle.aliases?.includes(lang);
        });
        if (bundles.length > 0) {
          return highlighter
            .loadLanguage(lang)
            .catch((err: unknown) => {
              console.error(err);
            })
            .then(() => {
              return highlighter.codeToHtml(str, lang);
            });
        } else {
          lang = "plaintext";
        }
      }
      return highlighter.codeToHtml(str, lang);
    } catch (err) {
      console.error("error while highlighting", str, lang, err);
      return `<pre><code>${markdown.utils.escapeHtml(str)}</code></pre>`;
    }
  },
});

const renderMarkdown = throttle(1000, (value) => {
  let workingValue = value;
  try {
    // Try to render markdown
    workingValue = !props.options?.disableMarkdown
      ? markdown.render(value)
      : value;
  } catch (e) {
    // If it fails, just display the raw markdown
    workingValue = value;
  }

  // Sanitize the markdown and set it to the ref
  sanitizedMarkdown.value = DOMPurify.sanitize(workingValue, {
    KEEP_CONTENT: true,
  });

  // Start MathJax typesetting asynchronously
  if (props.options?.disableMathJax) return;
  if (!mathjax) {
    // if mathjax is not loaded yet, try again in 1 sec (throttle)
    renderMarkdown(value);
    return;
  }
  setTimeout(() => {
    mathjax.typesetPromise([markdownElement.value]);
  }, 0);
});

watch(
  () => props.content,
  (value) => {
    renderMarkdown(value);
  }
);

onMounted(async () => {
  mathjax = await useMathJax();
  highlighter = await getShikiHighlighter();
  renderMarkdown(props.content);
});
</script>

<template>
  <div v-html="sanitizedMarkdown" ref="markdownElement" class="markdown"></div>
</template>

<style lang="scss">
.markdown {
  --code-line-height: 1.5rem;
  --code-font-size: 0.9rem;
  --color-divider: var(--color-background, var(--vp-c-divider));

  font-family: "Lato", "Roboto", "Arial", sans-serif;
  font-weight: 300;
  word-break: break-word;

  mjx-container {
    min-width: 0 !important;
    overflow-y: hidden;
    overflow-x: auto;
    height: 100%;

    &[display="true"] {
      overflow-x: auto;
      & > mjx-math {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 4px 0;
      }
    }
  }

  mjx-merror {
    background-color: var(
      --color-alert-error,
      var(--vp-custom-block-danger-bg)
    );
    color: var(--color-alert-error-text, var(--vp-custom-block-danger-text));
    text-align: center;
    display: flex;
    flex-direction: row;
    justify-content: center;

    padding: 0.2rem 0.4rem;
    border-radius: 0.3rem;
  }

  h1,
  h2,
  h3,
  h4 {
    font-family: "Poppins", "Open Sans", "Arial", sans-serif;
  }

  /**
 * Headings
 * -------------------------------------------------------------------------- */

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    position: relative;
    font-weight: 600;
    outline: none;
  }

  h1 {
    letter-spacing: -0.02em;
    line-height: 40px;
    font-size: 28px;
  }

  h2 {
    margin: 40px 0 16px;
    border-top: 1px solid var(--color-divider, var(--cp-c-divider-light));
    padding-top: 24px;
    letter-spacing: -0.02em;
    line-height: 32px;
    font-size: 24px;
  }

  h3 {
    margin: 32px 0 0;
    letter-spacing: -0.01em;
    line-height: 28px;
    font-size: 20px;
  }

  @media (min-width: 768px) {
    h1 {
      letter-spacing: -0.02em;
      line-height: 40px;
      font-size: 32px;
    }
  }

  /**
 * Paragraph and inline elements
 * -------------------------------------------------------------------------- */

  p,
  summary {
    margin: 16px 0;
  }

  p {
    line-height: 28px;
  }

  blockquote {
    margin: 16px 0;
    border-left: 2px solid var(--color-primary-active, var(--cp-c-divider));
    padding-left: 16px;
    transition: border-color 0.5s;
  }

  blockquote > p {
    margin: 0;
    font-size: 16px;
    color: var(--color-text-secondary, var(--cp-c-text-2));
    transition: color 0.5s;
  }

  a {
    font-weight: 500;
    color: var(--color-primary-active, var(--cp-c-brand));
    text-decoration-style: dotted;
    transition: color 0.25s;
  }

  a:hover {
    color: var(--color-primary, var(--cp-c-brand-dark));
  }

  strong {
    font-weight: 600;
  }

  /**
 * Lists
 * -------------------------------------------------------------------------- */

  ul,
  ol {
    padding-left: 1.25rem;
    margin: 16px 0;
  }

  ul {
    list-style: disc;
  }

  ol {
    list-style: decimal;
  }

  li + li {
    margin-top: 8px;
  }

  li > ol,
  li > ul {
    margin: 8px 0 0;
  }

  /**
 * Table
 * -------------------------------------------------------------------------- */

  table {
    display: block;
    border-collapse: collapse;
    margin: 20px 0;
    overflow-x: auto;
  }

  tr {
    border-top: 1px solid var(--color-divider, var(--cp-c-divider));
    transition: background-color 0.5s;
  }

  tr:nth-child(2n) {
    background-color: var(--c-bg-soft, var(--cp-c-bg-soft));
  }

  th,
  td {
    border: 1px solid var(--color-divider, var(--cp-c-divider));
    padding: 12px 16px;
  }

  th {
    font-size: 16px;
    font-weight: 600;
    background-color: var(--c-white-soft, var(--cp-c-white-soft), #f9f9f9);
  }

  .dark th {
    background-color: var(--c-black, var(--cp-c-black), #1a1a1a);
  }

  /**
 * Decorational elements
 * -------------------------------------------------------------------------- */

  hr {
    margin: 16px 0;
    border: none;
    border-top: 1px solid var(--color-divider, var(--cp-c-divider-light));
  }

  /**
 * Code
 * -------------------------------------------------------------------------- */

  /* inline code */
  :not(pre, h1, h2, h3, h4, h5, h6) > code {
    font-size: var(--code-font-size, --vp-code-font-size);
  }

  :not(pre) > code {
    border-radius: 4px;
    padding: 3px 6px;
    color: var(--color-code-text, var(--cp-c-text-code));
    background-color: var(--color-code-bg-muted, var(--vp-c-black-soft));
    transition: color 0.5s, background-color 0.5s;
  }

  h1 > code,
  h2 > code,
  h3 > code {
    font-size: 0.9em;
  }

  a > code {
    color: var(--color-primary, var(--cp-c-brand));
    transition: color 0.25s;
  }

  a:hover > code {
    color: var(--color-primary-active, var(--cp-c-brand-dark));
  }

  pre {
    position: relative;
    padding: 16px 0;
    overflow-x: auto;
    margin: 16px -12px;
    background-color: var(--color-code-bg, var(--cp-c-code-block-bg));
    border-radius: 4px;
    transition: background-color 0.5s;

    code {
      display: block;
      padding: 0 24px;
      width: fit-content;
      min-width: 100%;
      line-height: var(--code-line-height, --vp-code-line-height);
      font-size: var(--code-font-size, --vp-code-font-size);
      color: var(--color-code-text, var(--vp-code-block-color));
      transition: color 0.5s;
    }
  }
}

.markdown-editor-content {
  &.side-by-side .markdown {
    // changes if markdown is shown side by side to editor

    pre {
      margin: 16px 0;
    }
  }
}
</style>
