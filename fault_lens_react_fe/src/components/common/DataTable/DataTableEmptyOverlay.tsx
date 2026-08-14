import { GridOverlay } from "@mui/x-data-grid";

import { EmptyState } from "../EmptyState";

export function DataTableEmptyOverlay() {
    return (
        <GridOverlay>
            <EmptyState
                title="No Data"
                description="Nothing to display."
            />
        </GridOverlay>
    );
}