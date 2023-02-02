import { computed, ref } from "vue";

import type { Ref } from "vue";
import api from "@http/api";

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

type ApiResponse<T> = {
    status: number;
    data?: T;
    message?: string;
};

export const storeModuleFactory = <T extends { id: string }>(
    moduleName: string
) => {
    const storeContents: Ref<State<T>> = ref({});

    const lastLoad: Ref<number> = ref(0);
    const isValid: Ref<boolean> = ref(true);
    const loadedAll: Ref<boolean> = ref(false);
    const isLoadingAll: Ref<boolean> = ref(false);

    const state = {
        storeContents,
        shouldLoadAll: () => {
            const now = Date.now();
            const should =
                now - lastLoad.value > 1000 * 60 * 5 || !isValid.value;
            !loadedAll.value;

            return should && !isLoadingAll.value;
        },
    };

    const getters = {
        byId: (id: string) => computed(() => storeContents.value[id]),
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
            isLoadingAll.value = true;
            const response = (await api.get(`${moduleName}/`)) as ApiResponse<
                T[]
            >;

            if (response.status === 200) {
                setters.setAll(response.data as T[]);
                loadedAll.value = true;
                lastLoad.value = Date.now();
                isValid.value = true;
                isLoadingAll.value = false;
            }

            return response;
        },

        getById: async (id: string) => {
            const response = await api.get(`${moduleName}/${id}`);

            if (response.status === 200) {
                setters.setById(id, response.data as T);
            }

            return response;
        },

        create: async <K extends New<T>>(newItem: K) => {
            const response = await api.post(`${moduleName}/`, newItem);

            if (response.status === 201) {
                const data = response.data as T;
                setters.setById(data.id, data);
            }

            return response;
        },

        update: async (updatedItem: Updatable<T>) => {
            if (!updatedItem.id) {
                throw new Error("Cannot update item without id");
            }
            const response = await api.put(
                `${moduleName}/${updatedItem.id}`,
                updatedItem
            );

            if (response.status === 200) {
                const data = response.data as T;
                setters.setById(updatedItem.id, data);
            }

            return response;
        },

        delete: async (id: string) => {
            const response = await api.delete(`${moduleName}/${id}`);

            if (response.status === 200) {
                setters.deleteById(id);
            }

            return response;
        },

        invalidateAll: () => {
            isValid.value = false;
        },
    };

    return {
        state,
        getters,
        setters,
        actions,
    };
};
