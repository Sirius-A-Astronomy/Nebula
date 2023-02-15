import { describe, it, expect, vi, expectTypeOf } from "vitest";

import { storeModuleFactory } from "@stores/factory/storeFactory";
import type { ComputedRef } from "vue";
import type { ApiResponse } from "@http/api";

describe("storeModuleFactory", () => {
    type TestType = {
        name: string;
        id: string;
        age: number;
    };

    it("should return a store module", () => {
        const storeModule = storeModuleFactory<TestType>("tests");

        expect(storeModule).toBeTruthy();
        expect(storeModule.state).toBeTruthy();
        expect(storeModule.actions).toBeTruthy();

        expect(storeModule.state.storeContents).toBeTruthy();
        expect(storeModule.state.shouldLoadAll).toBeTruthy();

        /* ASSERT GETTERS */
        expect(storeModule.getters).toBeTruthy();

        expect(storeModule.getters.byId).toBeTruthy();
        expectTypeOf(storeModule.getters.byId).toMatchTypeOf<
            (id: string) => ComputedRef<TestType>
        >();

        expect(storeModule.getters.all).toBeTruthy();
        expectTypeOf(storeModule.getters.all).toMatchTypeOf<
            ComputedRef<TestType[]>
        >();

        /* ASSERT SETTERS */

        expect(storeModule.setters).toBeTruthy();

        expect(storeModule.setters.setById).toBeTruthy();
        expectTypeOf(storeModule.setters.setById).toMatchTypeOf<
            (id: string, item: TestType) => void
        >();

        expect(storeModule.setters.setAll).toBeTruthy();
        expectTypeOf(storeModule.setters.setAll).toMatchTypeOf<
            (items: TestType[]) => void
        >();

        expect(storeModule.setters.deleteById).toBeTruthy();
        expectTypeOf(storeModule.setters.deleteById).toMatchTypeOf<
            (id: string) => void
        >();

        /* ASSERT ACTIONS */

        expect(storeModule.actions).toBeTruthy();

        expect(storeModule.actions.getAll).toBeTruthy();
        expectTypeOf(storeModule.actions.getAll).toMatchTypeOf<
            () => Promise<ApiResponse<TestType[]>>
        >();

        expect(storeModule.actions.getById).toBeTruthy();
        expectTypeOf(storeModule.actions.getById).toMatchTypeOf<
            (id: string) => Promise<ApiResponse<TestType>>
        >();
    });

    it("can set and get items", async () => {
        const storeModule = storeModuleFactory<TestType>("tests");

        const testItem = {
            name: "test",
            id: "1",
            age: 1,
        };

        storeModule.setters.setById(testItem.id, testItem);

        expect(storeModule.getters.byId(testItem.id).value).toEqual(testItem);

        const testItem2 = {
            name: "test2",
            id: "2",
            age: 2,
        };

        storeModule.setters.setById(testItem2.id, testItem2);

        expect(storeModule.getters.byId(testItem2.id).value).toEqual(testItem2);

        expect(storeModule.getters.all.value).toEqual([testItem, testItem2]);
    });
});
