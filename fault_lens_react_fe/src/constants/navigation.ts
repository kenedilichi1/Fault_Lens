import DashboardOutlinedIcon from "@mui/icons-material/DashboardOutlined";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import WarningAmberOutlinedIcon from "@mui/icons-material/WarningAmberOutlined";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import PsychologyOutlinedIcon from "@mui/icons-material/PsychologyOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";

export const navigation = [
    {
        label: "Dashboard",
        href: "/dashboard",
        icon: DashboardOutlinedIcon,
    },
    {
        label: "Projects",
        href: "/projects",
        icon: FolderOutlinedIcon,
    },
    {
        label: "Logs",
        href: "/logs",
        icon: DescriptionOutlinedIcon,
    },
    {
        label: "Incidents",
        href: "/incidents",
        icon: WarningAmberOutlinedIcon,
    },
    {
        label: "Alerts",
        href: "/alerts",
        icon: NotificationsOutlinedIcon,
    },
    {
        label: "AI Insights",
        href: "/ai",
        icon: PsychologyOutlinedIcon,
    },
    {
        label: "Settings",
        href: "/settings",
        icon: SettingsOutlinedIcon,
    },
];