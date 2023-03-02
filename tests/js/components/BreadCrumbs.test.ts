import { mount, config } from "@vue/test-utils";
import BreadCrumbs from "@components/BreadCrumbs.vue";
import type { BreadCrumb } from "@components/BreadCrumbs.vue";
import { describe, it, expect, beforeAll, afterAll } from "vitest";

beforeAll(() => {
    config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
    config.global.renderStubDefaultSlot = false;
});

describe("BreadCrumbs.vue", () => {
    it("renders breadcrumbs when passed props", () => {
        // arrange
        expect(BreadCrumbs).toBeDefined();
        const breadcrumbs: BreadCrumb[] = [
            { name: "Home", to: "/" },
            { name: "Dashboard", to: "/dashboard" },
        ];

        // act
        const wrapper = mount(BreadCrumbs, {
            props: { breadcrumbs },
            global: {
                stubs: ["RouterLink"],
            },
        });

        // assert
        expect(wrapper.text()).toContain("Home");
        expect(wrapper.text()).toContain("Dashboard");
        expect(wrapper.find(".path-container").element.children.length).toBe(
            breadcrumbs.length
        );
    });
});
