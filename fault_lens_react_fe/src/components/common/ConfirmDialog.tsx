import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from "@mui/material";
import { AppButton } from "./AppButton";

type ConfirmDialogProps = {
    open: boolean;
    title: string;
    description: string;
    confirmText?: string;
    cancelText?: string;
    loading?: boolean;
    destructive?: boolean;
    onConfirm: () => void;
    onClose: () => void;
};

export function ConfirmDialog({
    open,
    title,
    description,
    confirmText = "Confirm",
    cancelText = "Cancel",
    loading = false,
    destructive = false,
    onConfirm,
    onClose,
}: ConfirmDialogProps) {
    return (
        <Dialog
            open={open}
            onClose={loading ? undefined : onClose}
            maxWidth="xs"
            fullWidth
        >
            <DialogTitle>{title}</DialogTitle>

            <DialogContent>
                <DialogContentText>
                    {description}
                </DialogContentText>
            </DialogContent>

            <DialogActions sx={{ px: 3, pb: 3 }}>
                <AppButton
                    onClick={onClose}
                    disabled={loading}
                    color="secondary"
                >
                    {cancelText}
                </AppButton>

                <AppButton
                    onClick={onConfirm}
                    loading={loading}
                    color={destructive ? "error" : "primary"}
                >
                    {confirmText}
                </AppButton>
            </DialogActions>
        </Dialog>
    );
}