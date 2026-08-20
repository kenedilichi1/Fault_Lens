import {
    Alert,
    AlertColor,
    Snackbar,
} from "@mui/material";
import {
    createContext,
    ReactNode,
    useCallback,
    useState,
} from "react";

type ToastOptions = {
    title: string;
    description?: string;
    variant?: AlertColor;
};

type ToastContextType = {
    toast: (options: ToastOptions) => void;
};

export const ToastContext = createContext<ToastContextType | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toastState, setToastState] = useState<ToastOptions | null>(null);

    const toast = useCallback((options: ToastOptions) => {
        setToastState(options);
    }, []);

    const handleClose = () => {
        setToastState(null);
    };

    return (
        <ToastContext.Provider value={{ toast }}>
            {children}

            <Snackbar
                open={Boolean(toastState)}
                autoHideDuration={4000}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: "top",
                    horizontal: "right",
                }}
            >
                {toastState ? (
                    <Alert
                        onClose={handleClose}
                        severity={toastState.variant ?? "info"}
                        variant="filled"
                        sx={{ width: "100%" }}
                    >
                        {toastState.title}
                        {toastState.description && (
                            <div>{toastState.description}</div>
                        )}
                    </Alert>
                ) : undefined}
            </Snackbar>
        </ToastContext.Provider>
    );
}