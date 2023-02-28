export type MetaData = {
    [key: PropertyKey]: unknown;
    created_at: string;
    updated_at: string;
};

export interface ErrorBin {
    [key: string]: string[] | ErrorBin;
}
