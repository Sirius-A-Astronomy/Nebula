<script setup lang="ts">
import { ref, watch, computed } from "vue";
import Markdown from "./Markdown.vue";

const props = defineProps<{
	content?: string;
	defaultTab?: string;
	modelValue?: string;
	customText?: {
		renderedLabel?: string;
		sourceLabel?: string;
		sideBySideLabel?: string;
	};
	placeholder?: string;
	title?: string;
	options?: {
		maxRows?: number;
		sourceFirst?: boolean;
		disableMarkdown?: boolean;
		disableMathJax?: boolean;
		tabToIndentToggle?: boolean;
	};
}>();

const contentEditable = ref(props.modelValue ?? props.content ?? "");

watch(
	[() => props.modelValue, () => props.content],
	([modelValue, content]) => {
		contentEditable.value = modelValue ?? content ?? "";
	}
);

const selectedTab = ref(props.defaultTab || "rendered");

const emit = defineEmits<{
	(e: "update:modelValue", value: string): void;
}>();

const tabs = computed(() => {
	const tabs = [
		{
			name: "rendered",
			label: props.customText?.renderedLabel ?? "Rendered",
		},
		{
			name: "source",
			label: props.customText?.sourceLabel ?? "Source",
		},
		{
			name: "side-by-side",
			label: props.customText?.sideBySideLabel ?? "Side-by-side",
		},
	];

	if (props.options?.sourceFirst) {
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
</script>

<template>
	<div class="markdown-editor">
		<div class="markdown-editor-header">
			<h4 class="title" v-if="title">{{ title }}</h4>
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
							type="radio" />
					</label>
				</template>
			</div>
		</div>
		<div
			class="editor-actions"
			v-if="selectedTab === 'source' || selectedTab === 'side-by-side'">
			<label
				v-if="props.options?.tabToIndentToggle"
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
			<textarea
				:rows="
					options?.maxRows
						? Math.min(
								options.maxRows,
								contentEditable.split('\n').length + 1
						  )
						: contentEditable.split('\n').length + 1
				"
				:placeholder="placeholder ?? 'Enter your markdown here...'"
				v-show="
					selectedTab === 'source' || selectedTab === 'side-by-side'
				"
				@keydown="keyDownHandler"
				ref="markdownEditElement"
				@input="emit('update:modelValue', contentEditable)"
				v-model="contentEditable" />
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
	border-radius: 12px;
}

.editor-actions {
	display: flex;
	align-items: center;
	padding: 0 12px;
	margin-top: 12px;
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
		font-weight: 600;
		line-height: 1.5;
		margin-bottom: 4px;
		color: var(--color-text-primary, var(--vp-code-block-color));
		padding: 0 12px;
	}

	.tabs {
		position: relative;
		display: flex;
		margin-right: -24px;
		margin-left: -24px;
		overflow-x: hidden;
		padding: 0 12px;
	}

	.side-by-side {
		margin-left: auto;
	}
}

.markdown-editor-content {
	margin-right: -24px;
	margin-left: -24px;
	padding: 8px 12px;
	color: var(--color-text-primary, var(--vp-code-block-color));
	overflow: auto;
	display: grid;
	grid-template-columns: 1fr;
	gap: 0.5rem;
	overflow-y: hidden;
	tab-size: 4;

	&.side-by-side {
		grid-template-columns: 1fr 1fr;
	}

	textarea {
		height: 100%;
		border-radius: 8px;
		border: none;
		padding: 12px;
		font-size: 14px;
		line-height: 1.5;
		background-color: var(--color-code-bg, var(--vp-code-tab-bg));
		color: var(--color-code-text);
		resize: vertical;
		overflow-y: auto;

		&::placeholder {
			color: var(--color-neutral-400, var(--vp-code-tab-placeholder));
		}

		&:focus {
			outline: var(--color-primary-active, var(--vp-code-tab-focus)) auto
				1px;
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
	.markdown-editor-header .tabs {
		margin-right: 0;
		margin-left: 0;
		border-radius: 8px 8px 0 0;
	}

	.markdown-editor-content {
		border-radius: 0 0 8px 8px;
		margin-right: 0;
		margin-left: 0;
	}
}

.markdown-editor-header .tabs input {
	position: absolute;
	opacity: 0;
	pointer-events: none;
}

.markdown-editor-header .tabs label {
	position: relative;
	display: inline-block;
	border-bottom: 1px solid transparent;
	padding: 0 12px;
	line-height: 48px;
	font-size: 14px;
	font-weight: 500;
	color: var(--color-text-secondary, var(--vp-code-tab-text-color));
	white-space: nowrap;
	cursor: pointer;
	transition: color 0.25s;
}

.markdown-editor-header .tabs label::after {
	position: absolute;
	right: 8px;
	bottom: -1px;
	left: 8px;
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

.markdown-editor-header label.checked {
	color: var(--color-text-primary, var(--vp-code-tab-active-text-color));
	background-color: var(
		--color-primary-active,
		var(--vp-code-tab-active-bar-color)
	);
	border-radius: 8px 8px 0 0;
}

.markdown-editor-header label.active::after {
	background-color: var(
		--color-primary-active,
		var(--vp-code-tab-active-bar-color)
	);
}
</style>
