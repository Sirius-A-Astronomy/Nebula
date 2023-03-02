import MarkdownEditor from "@components/MarkdownEditor.vue";

import { mount } from "@vue/test-utils";
import { describe, it, expect } from "vitest";

describe("MarkdownEditor base functionality", () => {
    it("should render", () => {
        const wrapper = mount(MarkdownEditor);
        expect(wrapper.find("textarea").exists()).toBe(true);
    });

    it("should have a settable content", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        expect(wrapper.find("textarea").element.value).toBe("# Hello World");
    });

    it("should have a settable v-model", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                modelValue: "# Hello World",
            },
        });

        expect(wrapper.find("textarea").element.value).toBe("# Hello World");
    });

    it("should emit an input event when the content changes", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        await wrapper.find("textarea").setValue("# Hello World 2");

        expect(wrapper.emitted("update:modelValue")).toBeTruthy();
        expect(wrapper.emitted("update:modelValue")?.[0]).toEqual([
            "# Hello World 2",
        ]);
    });

    it("can switch to preview mode", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        await wrapper
            .find("input[type=radio][data-tab=rendered]")
            .setValue("rendered");

        await wrapper.vm.$nextTick();

        expect(wrapper.find(".markdown-preview").isVisible()).toBe(true);
        expect(wrapper.find("textarea").exists()).toBe(false);
    });

    it("can switch to edit mode", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        await wrapper
            .find("input[type=radio][data-tab=rendered]")
            .setValue("rendered");

        await wrapper.vm.$nextTick();

        await wrapper
            .find("input[type=radio][data-tab=source]")
            .setValue("source");

        await wrapper.vm.$nextTick();

        expect(wrapper.find(".markdown-preview").isVisible()).toBe(false);
        expect(wrapper.find("textarea").exists()).toBe(true);
    });

    it("show edit and preview side-by-side", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        await wrapper
            .find("input[type=radio][data-tab=side-by-side]")
            .setValue("side-by-side");
        await wrapper.vm.$nextTick();

        expect(wrapper.find(".markdown-preview").isVisible()).toBe(true);
        expect(wrapper.find("textarea").exists()).toBe(true);
    });

    it("Should pass content to MarkdownDisplay", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
            },
        });

        const markdownDisplay = wrapper.findComponent({
            name: "MarkdownDisplay",
        });

        expect(markdownDisplay.exists()).toBe(true);
        expect(markdownDisplay.props("content")).toBe("# Hello World");

        await wrapper
            .find("input[type=radio][data-tab=rendered]")
            .setValue("rendered");
        await wrapper.vm.$nextTick();

        expect(markdownDisplay.isVisible()).toBe(true);

        await wrapper.setProps({ content: "## Updated text" });
        await wrapper.vm.$nextTick();

        expect(markdownDisplay.props("content")).toBe("## Updated text");
    });
});

describe("MarkdownEditor options", () => {
    it("should have customisable text", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                customText: {
                    renderedLabel: "Custom Rendered",
                    sourceLabel: "Custom Source",
                    sideBySideLabel: "Custom Side by side",
                },
            },
        });

        expect(
            wrapper
                .find("input[type=radio][data-tab=rendered]")
                .element.parentElement?.textContent?.trim()
        ).toBe("Custom Rendered");

        expect(
            wrapper
                .find("input[type=radio][data-tab=source]")
                .element.parentElement?.textContent?.trim()
        ).toBe("Custom Source");

        expect(
            wrapper
                .find("input[type=radio][data-tab=side-by-side]")
                .element.parentElement?.textContent?.trim()
        ).toBe("Custom Side by side");
    });

    it("Can have a title", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                title: "Custom Title",
            },
        });

        expect(wrapper.find("label.title").text()).toBe("Custom Title");
    });

    it("Can have a placeholder", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                placeholder: "Custom Placeholder",
            },
        });

        expect(wrapper.find("textarea").attributes("placeholder")).toBe(
            "Custom Placeholder"
        );
    });

    it("Can have a preset set to docs", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                preset: "docs",
            },
        });

        // expect rendered tab to be selected
        expect(
            (
                wrapper.find("input[type=radio][data-tab=rendered]")
                    .element as HTMLInputElement
            ).value
        ).toBe("on");

        expect(wrapper.find("textarea").exists()).toBe(false);
        expect(wrapper.find(".markdown-preview").isVisible()).toBe(true);

        // expect rendered tab to be first in the list
        expect(
            wrapper.findAll("input[type=radio]").at(0)?.attributes("data-tab")
        ).toBe("rendered");

        // expect source tab to be second in the list
        expect(
            wrapper.findAll("input[type=radio]").at(1)?.attributes("data-tab")
        ).toBe("source");
    });

    it("Can have a tab to indent toggle", async () => {
        const wrapper = mount(MarkdownEditor, {
            props: {
                content: "# Hello World",
                options: {
                    tabToIndentToggle: true,
                },
            },
        });

        // now a toggle should be present
        expect(wrapper.find("input[type=checkbox]#tabIndent").exists()).toBe(
            true
        );

        // checking the toggle should change the tab to indent option
        await wrapper.find("input[type=checkbox]#tabIndent").setValue(true);

        // inputting a tab should now indent
        await wrapper.find("textarea").trigger("focus");
        await wrapper.find("textarea").trigger("keydown", {
            key: "Tab",
        });
        await wrapper.vm.$nextTick();

        expect(wrapper.find("textarea").element.value).toBe("# Hello World\t");
    });
});
