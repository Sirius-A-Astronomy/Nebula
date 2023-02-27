import { computed, ref } from "vue";

import type { Ref } from "vue";
import api from "@http/api";

const createdStores: {
    actions: {
        invalidateAll: () => void;
    };
    setters: {
        setAll: (items: any[]) => void;
    };
}[] = [];

export type State<T extends { id: string }> = {
    [id: string]: T;
};

export type DeepPartial<T> = T extends object
    ? {
          [P in keyof T]?: DeepPartial<T[P]>;
      }
    : T;

export type New<T extends { id: string }> = Omit<T, "id" | "created_at">;

export type Updatable<T extends { id: string }> = DeepPartial<T>;

export const storeModuleFactory = <T extends { id: string }>(
    moduleName: string
) => {
    const storeContents: Ref<State<T>> = ref({});

    const state = {
        storeContents,
        isLoadingAll: ref(false),
        loadedAll: ref(false),
        isValid: ref(true),
        lastLoad: ref(0),
        shouldLoadAll: () => {
            const now = Date.now();
            const should =
                now - state.lastLoad.value > 1000 * 60 * 5 ||
                !state.isValid.value;
            !state.loadedAll.value;

            return should && !state.isLoadingAll.value;
        },
    };

    const getters = {
        byId: (id: string) => computed(() => storeContents.value[id] ?? null),
        all: computed(() => Object.values(storeContents.value)),
    };

    const setters = {
        setById: (id: string, item: T) => {
            storeContents.value[id] = item;
        },

        setAll: (items: T[]) => {
            storeContents.value = items.reduce((acc, item) => {
                acc[item.id] = item;
                return acc;
            }, {} as State<T>);
        },

        deleteById: (id: string) => {
            delete storeContents.value[id];
        },
    };

    const actions = {
        getAll: async () => {
            state.isLoadingAll.value = true;
            const response = await api.get<T[]>(`${moduleName}/`);

            if (response.ok) {
                setters.setAll(response.data as T[]);
                state.loadedAll.value = true;
                state.lastLoad.value = Date.now();
                state.isValid.value = true;
                state.isLoadingAll.value = false;
            }

            return response;
        },

        getById: async (id: string) => {
            const response = await api.get<T>(`${moduleName}/${id}`);

            if (response.ok) {
                setters.setById(id, response.data);
            }

            return response;
        },

        getByFilter: async (filter: Record<string, string>) => {
            const response = await api.get<T[]>(`${moduleName}/`, filter);

            if (response.ok) {
                for (const item of response.data) {
                    setters.setById(item.id, item);
                }
            }

            return response;
        },

        create: async <K>(newItem: K) => {
            const response = await api.post<T>(`${moduleName}/`, newItem);

            if (response.ok) {
                const data = response.data;
                setters.setById(data.id, data);
            }

            return response;
        },

        update: async <K extends { id?: string }>(updatedItem: K) => {
            if (!updatedItem.id) {
                throw new Error("Cannot update item without id");
            }
            const response = await api.put<T, K>(
                `${moduleName}/${updatedItem.id}`,
                updatedItem
            );

            if (response.ok) {
                const data = response.data;
                setters.setById(updatedItem.id, data);
            }

            return response;
        },

        delete: async (id: string) => {
            const response = await api.delete<T>(`${moduleName}/${id}`);

            if (response.ok) {
                setters.deleteById(id);
            }

            return response;
        },

        invalidateAll: () => {
            state.isValid.value = false;
        },
    };

    const createdStore = {
        state,
        getters,
        setters,
        actions,
    };

    createdStores.push(createdStore);

    return createdStore;
};

export const invalidateAllStores = () => {
    createdStores.forEach((store) => store.actions.invalidateAll());
};

export const clearAllStores = () => {
    createdStores.forEach((store) => {
        store.setters.setAll([]);
    });
};
