import LoadingButton, {
    LoadingButtonProps,
} from "@mui/lab/LoadingButton";

type AppButtonProps = LoadingButtonProps;

export function AppButton({
    children,
    variant = "contained",
    size = "large",
    ...props
}: AppButtonProps) {
    return (
        <LoadingButton
            variant={variant}
            size={size}
            {...props}
        >
            {children}
        </LoadingButton>
    );
}