import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import WarningAmberRoundedIcon from "@mui/icons-material/WarningAmberRounded";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import PsychologyOutlinedIcon from "@mui/icons-material/PsychologyOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import BusinessIcon from "@mui/icons-material/Business";
import GridViewIcon from "@mui/icons-material/GridView";
import VpnKeyTwoToneIcon from "@mui/icons-material/VpnKeyTwoTone";
import PeopleOutlinedIcon from "@mui/icons-material/PeopleOutlined";
import DesktopWindowsOutlinedIcon from "@mui/icons-material/DesktopWindowsOutlined";
import QueryStatsOutlinedIcon from "@mui/icons-material/QueryStatsOutlined";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import type { SvgIconComponent } from "@mui/icons-material";
import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';

export interface NavigationItem {
  label: string;
  href: string;
  icon: SvgIconComponent;
}
export const navigation = {
  basic: [
    {
      label: "Overview",
      href: "/overview",
      icon: GridViewIcon,
    },
    {
      label: "Incidents",
      href: "/incidents",
      icon: WarningAmberRoundedIcon,
    },
    {
      label: "Alerts",
      href: "/alerts",
      icon: NotificationsOutlinedIcon,
    },
    {
      label: "Services",
      href: "/service",
      icon: DesktopWindowsOutlinedIcon,
    },
    {
      label: "Logs",
      href: "/logs",
      icon: DescriptionOutlinedIcon,
    },
    {
      label: "Metrics",
      href: "/metrics",
      icon: QueryStatsOutlinedIcon,
    },
    {
      label: "Traces",
      href: "/traces",
      icon: LightModeOutlinedIcon,
    },
    {
      label: "Dashboards",
      href: "/dashboards",
      icon: DashboardOutlinedIcon,
    },
  ],
  management: [
    {
      label: "Organizations",
      href: "/organizations",
      icon: BusinessIcon,
    },
    {
      label: "Teams",
      href: "/teams",
      icon: PeopleOutlinedIcon,
    },
    {
      label: "API Keys",
      href: "/api-keys",
      icon: VpnKeyTwoToneIcon,
    },
    {
      label: "Settings",
      href: "/settings",
      icon: SettingsOutlinedIcon,
    },
  ],
}satisfies{
  basic:NavigationItem[],
  management:NavigationItem[]
};
