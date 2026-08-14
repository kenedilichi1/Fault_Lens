import { Link as RouterLink, useLocation } from "react-router-dom";
import CloseOutlinedIcon from "@mui/icons-material/CloseOutlined";
import MenuIcon from "@mui/icons-material/Menu";

import {
    Drawer,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography,
    Box,
    IconButton,
    useTheme,
    useMediaQuery,
} from "@mui/material";
import { navigation } from "@/constants/navigation";
import { SIDEBAR_WIDTH } from "@/constants/layout";

type SidebarProps = {
    mobileOpen: boolean;
    desktopOpen: boolean;
    onClose: () => void;
    onDesktopToggle: () => void;
};

export function Sidebar({ mobileOpen, desktopOpen, onClose, onDesktopToggle }: SidebarProps) {
    const location = useLocation();
    const pathname = location.pathname;
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

    const drawerContent = (
        <>
            <Toolbar sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", px: [1] }}>
                {(!isMobile && desktopOpen) || isMobile ? (
                    <Typography variant="h6" sx={{ fontWeight: 700, ml: 2, whiteSpace: "nowrap" }}>
                        FaultLens
                    </Typography>
                ) : null}

                <IconButton onClick={isMobile ? onClose : onDesktopToggle} sx={{ mx: desktopOpen || isMobile ? 0 : "auto" }}>
                    {isMobile ? <CloseOutlinedIcon /> : <MenuIcon />}
                </IconButton>
            </Toolbar>

            <Box sx={{ overflow: "hidden" }}>
                <List>
                    {navigation.map((item) => {
                        const Icon = item.icon;

                        return (
                            <ListItemButton
                                key={item.href}
                                component={RouterLink}
                                to={item.href}
                                selected={pathname === item.href}
                                sx={{
                                    minHeight: 48,
                                    justifyContent: desktopOpen || isMobile ? 'initial' : 'center',
                                    px: 2.5,
                                }}
                                onClick={isMobile ? onClose : undefined}
                            >
                                <ListItemIcon
                                    sx={{
                                        minWidth: 0,
                                        mr: desktopOpen || isMobile ? 3 : 'auto',
                                        justifyContent: 'center',
                                    }}
                                >
                                    <Icon />
                                </ListItemIcon>

                                <ListItemText 
                                    primary={item.label} 
                                    sx={{ opacity: desktopOpen || isMobile ? 1 : 0 }} 
                                />
                            </ListItemButton>
                        );
                    })}
                </List>
            </Box>
        </>
    );

    return (
        <Box
            component="nav"
            sx={{ width: { sm: desktopOpen ? SIDEBAR_WIDTH : 65 }, flexShrink: { sm: 0 } }}
        >
            {/* Mobile Drawer */}
            <Drawer
                variant="temporary"
                open={mobileOpen}
                onClose={onClose}
                ModalProps={{
                    keepMounted: true, // Better open performance on mobile.
                }}
                sx={{
                    display: { xs: "block", sm: "none" },
                    "& .MuiDrawer-paper": {
                        boxSizing: "border-box",
                        width: SIDEBAR_WIDTH,
                    },
                }}
            >
                {drawerContent}
            </Drawer>
            
            {/* Desktop Drawer */}
            <Drawer
                variant="permanent"
                sx={{
                    display: { xs: "none", sm: "block" },
                    "& .MuiDrawer-paper": {
                        boxSizing: "border-box",
                        width: desktopOpen ? SIDEBAR_WIDTH : 65,
                        overflowX: 'hidden',
                        transition: theme.transitions.create('width', {
                            easing: theme.transitions.easing.sharp,
                            duration: desktopOpen 
                                ? theme.transitions.duration.enteringScreen 
                                : theme.transitions.duration.leavingScreen,
                        }),
                    },
                }}
                open
            >
                {drawerContent}
            </Drawer>
        </Box>
    );
}