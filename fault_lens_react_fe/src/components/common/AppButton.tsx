import Button, { ButtonProps } from "@mui/material/Button";

type AppButtonProps = ButtonProps;

export function AppButton({
    children,
    variant = "contained",
    size = "large",
    ...props
}: AppButtonProps) {
    return (
        <Button
            variant={variant}
            size={size}
            {...props}
        >
            {children}
        </Button>
    );
}