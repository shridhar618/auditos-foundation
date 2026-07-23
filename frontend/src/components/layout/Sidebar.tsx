import {
  BarChart3,
  Bot,
  FileText,
  LayoutDashboard,
  Search,
  Settings,
  ShieldCheck,
  ShieldQuestion,
  Users,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/investigations", label: "Investigations", icon: ShieldQuestion },
  { to: "/documents", label: "Documents", icon: FileText },
  { to: "/policies", label: "Policies", icon: ShieldCheck },
  { to: "/ai-agents", label: "AI Agents", icon: Bot },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/users", label: "Users & Roles", icon: Users },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-border bg-card/50 lg:flex lg:flex-col">
      <div className="flex h-16 items-center gap-2 border-b border-border px-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <ShieldCheck className="h-4 w-4" />
        </div>
        <span className="text-lg font-bold tracking-tight">AuditOS</span>
      </div>

      <div className="px-4 pt-4">
        <button className="flex w-full items-center gap-2 rounded-md border border-border bg-background px-3 py-2 text-sm text-muted-foreground shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground">
          <Search className="h-4 w-4" />
          Search
          <kbd className="ml-auto rounded border border-border bg-muted px-1.5 py-0.5 text-[10px] font-medium">⌘K</kbd>
        </button>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-4 scrollbar-thin">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )
            }
          >
            <Icon className="h-4 w-4 shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-border p-4 text-xs text-muted-foreground">
        AuditOS v0.1.0 · Foundation build
      </div>
    </aside>
  );
}
