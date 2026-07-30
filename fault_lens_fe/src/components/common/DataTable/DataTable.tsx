"use client";

import {
    DataGrid,
    DataGridProps,
} from "@mui/x-data-grid";
import { DataTableEmptyOverlay } from "./DataTableEmptyOverlay";

export function DataTable(props: DataGridProps) {
    return (
        <DataGrid
            disableRowSelectionOnClick
            pageSizeOptions={[10, 25, 50, 100]}
            slots={{
                noRowsOverlay: DataTableEmptyOverlay,
            }}
            initialState={{
                pagination: {
                    paginationModel: {
                        pageSize: 10,
                    },
                },
            }}
            sx={{
                border: 0,

                "& .MuiDataGrid-columnHeaders": {
                    backgroundColor: "background.paper",
                },

                "& .MuiDataGrid-cell": {
                    borderBottomColor: "divider",
                },
            }}
            {...props}
        />
    );
}