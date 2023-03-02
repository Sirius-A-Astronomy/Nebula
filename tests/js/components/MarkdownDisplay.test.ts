import { mount, config } from "@vue/test-utils";
import MarkdownDisplay from "@components/MarkdownDisplay.vue";
import { describe, it, expect, beforeAll, afterAll, vi } from "vitest";
import { JSDOM } from "jsdom";
import { useMathJax } from "@/lib/mathjax";

/*
    Test the MarkdownDisplay component

    Does not test mathjax.
    Does test markdown, DOMPurify, and vue rendering.
*/

// mock mathjax since it's import is a mess, and testing it might be impossible
vi.mock("@/lib/mathjax", () => {
    const mathjax = {
        typesetPromise: vi.fn(),
    };
    return {
        useMathJax: vi.fn(() => mathjax),
    };
});

// mock window and document since they are not available in node and DOMPurify needs them
const dom = new JSDOM();

const window = dom.window;
const document = window.document;

// @ts-ignore
global.window = window;
// @ts-ignore
global.document = document;

let mathjax: any;
beforeAll(async () => {
    config.global.renderStubDefaultSlot = true;
    mathjax = await useMathJax();
});

afterAll(() => {
    config.global.renderStubDefaultSlot = false;
});

const markdownHasUpdated = async (wrapper: any, oldValue: string = "") => {
    while (
        (
            wrapper.find("div.markdown").element as HTMLDivElement
        ).innerHTML.trim() === oldValue.trim()
    ) {
        await new Promise((resolve) => setTimeout(resolve, 50));
    }
    return;
};

describe("MarkdownDisplay.vue", () => {
    it("Renders markdown when passed content", async () => {
        // arrange
        expect(MarkdownDisplay).toBeDefined();
        const markdown = "# Hello World";

        // act
        const wrapper = mount(MarkdownDisplay, {
            props: { content: markdown },
        });

        await markdownHasUpdated(wrapper);
        // assert
        expect(wrapper.find("h1").text()).toBe("Hello World");
        expect(useMathJax).toBeCalledTimes(2);

        // arrange
        const oldHtml =
            (wrapper.find("div.markdown").element as HTMLDivElement)
                .innerHTML || "";

        // act
        await wrapper.setProps({ content: "## Updated text" });

        await markdownHasUpdated(wrapper, oldHtml);
        // assert
        expect(wrapper.find("h2").text()).toBe("Updated text");
    });

    it("Safely encodes dangerous html", async () => {
        // arrange
        expect(MarkdownDisplay).toBeDefined();
        const markdown = `<script\x20type="text/javascript">throw new Error("you got xssd");</script>`;

        // act
        const wrapper = mount(MarkdownDisplay, {
            props: { content: markdown },
        });

        await markdownHasUpdated(wrapper);
        // assert
        expect(wrapper.find("script").exists()).toBe(false);
        expect(wrapper.find("div.markdown").text()).toContain("you got xssd");
    });
});
