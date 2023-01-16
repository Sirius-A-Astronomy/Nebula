<script setup lang="ts">
import { getShikiHighlighter } from "../lib/highlighter";
import type { Highlighter } from "shiki";
import { ref, watch, computed, onMounted } from "vue";
import Markdown from "./Markdown.vue";
import DOMPurify from "dompurify";

const props = defineProps<{
	content?: string;
	modelValue?: string;
	customText?: {
		renderedLabel?: string;
		sourceLabel?: string;
		sideBySideLabel?: string;
	};
	placeholder?: string;
	title?: string;
	preset?: "docs";
	options?: {
		defaultTab?: string;
		maxRows?: number;
		renderedFirst?: boolean;
		disableMarkdown?: boolean;
		disableMathJax?: boolean;
		tabToIndentToggle?: boolean;
	};
}>();

const contentEditable = ref(props.modelValue ?? props.content ?? "");

const presets = {
	docs: {
		options: {
			defaultTab: "rendered",
			renderedFirst: true,
			disableMarkdown: false,
			disableMathJax: false,
			tabToIndentToggle: false,
		},
		customText: {
			renderedLabel: "Rendered",
			sourceLabel: "Source",
			sideBySideLabel: "Side-by-side",
		},
	},
};

const options = computed(() => {
	if (props.preset && presets[props.preset!]) {
		return Object.entries(presets[props.preset!].options).reduce(
			(acc, [key, value]) => {
				if (
					props.options?.[key as keyof typeof props.options] ===
					undefined
				) {
					acc[key] = value;
				}
				return acc;
			},
			props.options ?? ({} as Record<string, unknown>)
		);
	}
	return props.options;
});

const customText = computed(() => {
	if (props.preset) {
		return Object.entries(presets[props.preset!].customText).reduce(
			(acc, [key, value]) => {
				if (
					props.customText?.[key as keyof typeof props.options] ===
					undefined
				) {
					acc[key] = value;
				}
				return acc;
			},
			props.customText ?? ({} as Record<string, unknown>)
		);
	}
	return props.customText;
});

watch(
	[() => props.modelValue, () => props.content],
	([modelValue, content]) => {
		contentEditable.value = modelValue ?? content ?? "";
	}
);

let highlighter: Highlighter;
const highlightedContent = ref(contentEditable.value);

const highlightContent = () => {
	if (!highlighter)
		return (highlightedContent.value = contentEditable.value) + " ";
	highlightedContent.value =
		DOMPurify.sanitize(
			highlighter.codeToHtml(
				contentEditable.value,
				"markdown",
				"material-palenight"
			),
			{ KEEP_CONTENT: true }
		) + " ";
};

watch(contentEditable, highlightContent);

const selectedTab = ref(options.value?.defaultTab || "source");

const emit = defineEmits<{
	(e: "update:modelValue", value: string): void;
}>();

const tabs = computed(() => {
	const tabs = [
		{
			name: "rendered",
			label: customText.value?.renderedLabel ?? "Rendered",
		},
		{
			name: "source",
			label: customText.value?.sourceLabel ?? "Source",
		},
		{
			name: "side-by-side",
			label: customText.value?.sideBySideLabel ?? "Side-by-side",
		},
	];

	if (!options.value?.renderedFirst) {
		// swap the first two elements
		[tabs[0], tabs[1]] = [tabs[1], tabs[0]];
	}

	return tabs;
});

const useTabIndent = ref(false);

const markdownEditElement = ref<HTMLTextAreaElement | null>(null);

const keyDownHandler = (event: KeyboardEvent) => {
	if (
		event.key === "Enter" &&
		props.options?.maxRows &&
		contentEditable.value.split("\n").length >= props.options.maxRows
	) {
		event.preventDefault();
		return false;
	}
	if (
		event.key === "Tab" &&
		useTabIndent.value &&
		!(event.ctrlKey || event.metaKey || event.altKey || event.shiftKey)
	) {
		event.preventDefault();
		console.log("tabbing");
		if (!markdownEditElement.value) return;
		const start = markdownEditElement.value.selectionStart;
		const end = markdownEditElement.value.selectionEnd;
		const value = markdownEditElement.value.value;
		markdownEditElement.value.value =
			value.slice(0, start) + "\t" + value.slice(end);
		markdownEditElement.value.setSelectionRange(start, end);
		markdownEditElement.value.setRangeText("\t", start, end, "end");
		markdownEditElement.value.setSelectionRange(start + 1, end + 1);
	}
};

onMounted(async () => {
	highlighter = await getShikiHighlighter();
	highlightContent();
});

const markdownEditorId = ref(
	`markdown-editor-${Math.random().toString(36).slice(8)}`
);
</script>

<template>
	<div class="markdown-editor" :class="`preset-${preset}`">
		<div class="markdown-editor-header">
			<label :for="markdownEditorId" class="title" v-if="title">{{
				title
			}}</label>
			<div class="tabs">
				<template v-for="tab in tabs" :key="tab.name">
					<label
						:class="{
							'side-by-side': tab.name === 'side-by-side',
							active: tab.name === selectedTab,
						}"
						>{{ tab.label }}
						<input
							:checked="tab.name === selectedTab"
							@change="selectedTab = tab.name"
							:name="markdownEditorId"
							@keydown="
								(e) => {
									if (e.key === 'Enter') {
										selectedTab = tab.name;
										e.preventDefault();
									}
								}
							"
							type="radio" />
					</label>
				</template>
			</div>
		</div>
		<div
			class="editor-actions"
			v-if="
				(selectedTab === 'source' || selectedTab === 'side-by-side') &&
				options?.tabToIndentToggle
			">
			<label
				v-if="options.tabToIndentToggle"
				class="tab-indent-toggle"
				:class="{
					checked: useTabIndent,
				}">
				Use Tab to indent
				<input
					type="checkbox"
					name="tabIndent"
					id="tabIndent"
					v-model="useTabIndent" />
			</label>
		</div>
		<div
			class="markdown-editor-content"
			:class="{
				'side-by-side': selectedTab === 'side-by-side',
			}">
			<div
				class="textarea-wrapper"
				v-if="
					selectedTab === 'source' || selectedTab === 'side-by-side'
				">
				<textarea
					:placeholder="placeholder ?? 'Enter your markdown here...'"
					@keydown="keyDownHandler"
					ref="markdownEditElement"
					:id="markdownEditorId"
					@input="emit('update:modelValue', contentEditable)"
					v-model="contentEditable" />
				<div
					class="syntax-highlighted"
					v-html="highlightedContent"></div>
			</div>
			<Markdown
				class="vp-markdown-preview"
				v-show="
					selectedTab === 'rendered' || selectedTab === 'side-by-side'
				"
				:options="{
					disableMarkdown: options?.disableMarkdown,
					disableMathJax: options?.disableMathJax,
				}"
				:content="contentEditable" />
		</div>
	</div>
</template>

<style lang="scss" scoped>
.markdown-editor {
	margin-top: 16px;
	margin-bottom: 12px;
	padding-top: 12px;
	background-color: var(--color-background, var(--vp-c-black-mute));

	&.preset-docs {
		padding-inline: 24px;
		margin-left: -24px;
		margin-right: -24px;
	}
}

.editor-actions {
	display: flex;
	align-items: center;
	padding: 0 12px;
	margin-top: 8px;
	.tab-indent-toggle {
		display: flex;
		align-items: center;
		margin-left: auto;
		color: var(--color-text-primary, var(--vp-code-tab-text-color));
		font-size: 12px;
		font-weight: 300;
		line-height: 1.5;
		cursor: pointer;

		&.checked {
			color: var(
				--color-text-primary,
				var(--vp-code-tab-active-text-color)
			);
		}

		input {
			margin-left: 8px;
		}
	}
}

.markdown-editor-header {
	.title {
		font-size: 16px;
		font-weight: 400;
		line-height: 1.5;
		margin-bottom: 4px;
		color: var(--color-text-primary, var(--vp-code-block-color));
		padding: 0 12px;
	}

	.tabs {
		position: relative;
		display: flex;
		overflow-x: hidden;
		padding: 0 12px;
	}
}

.markdown-editor-content {
	margin-right: -24px;
	margin-left: -24px;
	padding: 8px 24px;
	color: var(--color-text-primary, var(--vp-code-block-color));
	overflow: auto;
	display: grid;
	grid-template-columns: minmax(0, 1fr);
	gap: 0.5rem;
	overflow-y: hidden;
	tab-size: 4;

	&.side-by-side {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	// text-area wrapper provides auto resizing to the text-area
	.textarea-wrapper {
		display: grid;
		background-color: var(--color-code-bg, var(--vp-code-tab-bg));

		.syntax-highlighted {
			// wrapper::after needs to have exactly the same styles as the text-area
			// and the same content

			// this causes it to be exactly the same size as the text-area should be
			// causing the parent to resize to fit the text-area
			white-space: pre-wrap;
			padding: 12px;
			pointer-events: none;

			:deep(pre) {
				background-color: transparent !important;
				margin: 0;
				font-family: monospace;
				white-space: pre-wrap;
			}
		}

		textarea {
			caret-color: var(--color-code-text, var(--vp-code-tab-text-color));
			color: #0000;
			background-color: #0000;
			z-index: 1;

			&::placeholder {
				color: var(--color-neutral-400, var(--vp-code-tab-placeholder));
			}

			&:focus {
				outline: none;
				box-shadow: none;
			}
		}

		textarea,
		.syntax-highlighted {
			grid-area: 1/ 1 / 2 / 2;
			height: 100%;
			border-radius: 8px;
			font-family: monospace;
			border: none;
			padding: 12px;
			font-size: 14px;
			line-height: 1.5;
			resize: none;
			overflow-y: hidden;
			tab-size: 4;
			word-wrap: break-word;
		}
	}
}

.markdown-editor-header .tabs::after {
	position: absolute;
	right: 0;
	bottom: 0;
	left: 0;
	height: 1px;
	background-color: var(
		--color-background-secondary,
		var(--vp-code-tab-divider)
	);
	content: "";
}

@media (min-width: 640px) {
	.markdown-editor {
		border-radius: 12px;
		&.preset-docs {
			margin-left: 0;
			margin-right: 0;
		}
	}

	.markdown-editor-header .tabs {
		margin-right: 0;
		margin-left: 0;
		border-radius: 8px 8px 0 0;
	}

	.markdown-editor-content {
		border-radius: 0 0 8px 8px;
		margin-right: 0;
		margin-left: 0;
		padding: 8px 0px;

		.textarea-wrapper {
			border-radius: 8px;
		}
	}
}

.markdown-editor-header .tabs input {
	position: absolute;
	opacity: 0;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	pointer-events: none;
}

.markdown-editor-header .tabs label {
	position: relative;
	display: inline-block;
	border-bottom: 1px solid transparent;
	line-height: 48px;
	font-size: 14px;
	font-weight: 500;
	color: var(--color-text-secondary, var(--vp-code-tab-text-color));
	white-space: nowrap;
	box-shadow: none;
	cursor: pointer;
	transition: color 0.25s, box-shadow 0.25s;

	& + label {
		margin-left: 24px;
	}

	&.side-by-side {
		margin-left: auto;
	}

	&:has(input:focus) {
		color: var(--color-text-primary, var(--vp-code-tab-active-text-color));
		box-shadow: inset 0 -4px 0 var(--color-primary-active, var(--vp-code-tab-active-bar-color));
	}
}

.markdown-editor-header .tabs label::after {
	position: absolute;
	right: 0px;
	bottom: -1px;
	left: 0px;
	z-index: 1;
	height: 1px;
	content: "";
	background-color: transparent;
	transition: background-color 0.25s;
}

.markdown-editor-header label:hover {
	color: var(--color-text-primary, var(--vp-code-tab-hover-text-color));
}

.markdown-editor-header label.active {
	color: var(--color-text-primary, var(--vp-code-tab-active-text-color));
}

.markdown-editor-header label.active::after {
	background-color: var(
		--color-primary-active,
		var(--vp-code-tab-active-bar-color)
	);
}
</style>
