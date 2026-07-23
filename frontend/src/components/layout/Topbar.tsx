import * as Avatar from "@radix-ui/react-avatar";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { Bell, LogOut, Moon, Settings, Sun } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";

function initials(name: string) {
  return name
    .split(" ")
    .map((part) => part[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function Topbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="glass sticky top-0 z-20 flex h-16 items-center justify-between px-6">
      <div>
        <p className="text-sm text-muted-foreground">{user?.organization_name}</p>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={toggleTheme}
          className="flex h-9 w-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>

        <button className="relative flex h-9 w-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-destructive" />
        </button>

        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button className="flex items-center gap-2 rounded-md px-2 py-1.5 transition-colors hover:bg-accent">
              <Avatar.Root className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground">
                <Avatar.Fallback>{user ? initials(user.full_name) : "?"}</Avatar.Fallback>
              </Avatar.Root>
              <div className="hidden text-left sm:block">
                <p className="text-sm font-medium leading-none">{user?.full_name}</p>
                <p className="text-xs capitalize text-muted-foreground">{user?.role.replace("_", " ")}</p>
              </div>
            </button>
          </DropdownMenu.Trigger>

          <DropdownMenu.Portal>
            <DropdownMenu.Content
              align="end"
              sideOffset={8}
              className="z-30 min-w-[180px] animate-fade-in rounded-md border border-border bg-card p-1 shadow-lg"
            >
              <DropdownMenu.Item className="flex cursor-pointer items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent">
                <Settings className="h-4 w-4" /> Settings
              </DropdownMenu.Item>
              <DropdownMenu.Separator className="my-1 h-px bg-border" />
              <DropdownMenu.Item
                onClick={handleLogout}
                className="flex cursor-pointer items-center gap-2 rounded-sm px-2 py-1.5 text-sm text-destructive outline-none hover:bg-destructive/10"
              >
                <LogOut className="h-4 w-4" /> Log out
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}
