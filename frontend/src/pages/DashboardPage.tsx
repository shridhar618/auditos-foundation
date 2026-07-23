import { motion } from "framer-motion";
import { ArrowUpRight, ShieldAlert, ShieldCheck, TrendingUp, Users } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";

const PLACEHOLDER_KPIS = [
  { label: "Compliance Score", value: "—", icon: ShieldCheck, tone: "text-success" },
  { label: "Risk Score", value: "—", icon: ShieldAlert, tone: "text-warning" },
  { label: "Open Investigations", value: "—", icon: TrendingUp, tone: "text-primary" },
  { label: "Active Users", value: "1", icon: Users, tone: "text-accent" },
];

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold tracking-tight">Welcome back, {user?.full_name.split(" ")[0]}</h1>
        <p className="text-muted-foreground">
          This is the AuditOS foundation build — authentication, roles, and the app shell are wired up.
          The full compliance dashboard, investigations, and AI agents land in the next build phases.
        </p>
      </motion.div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {PLACEHOLDER_KPIS.map((kpi, i) => (
          <motion.div
            key={kpi.label}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Card className="animate-slide-up">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{kpi.label}</CardTitle>
                <kpi.icon className={`h-4 w-4 ${kpi.tone}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{kpi.value}</div>
                <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                  Coming in the Dashboard module
                </p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your session</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div className="flex justify-between border-b border-border pb-2">
            <span className="text-muted-foreground">Organization</span>
            <span className="font-medium">{user?.organization_name}</span>
          </div>
          <div className="flex justify-between border-b border-border pb-2">
            <span className="text-muted-foreground">Role</span>
            <span className="font-medium capitalize">{user?.role.replace("_", " ")}</span>
          </div>
          <div className="flex justify-between pb-2">
            <span className="text-muted-foreground">Permissions granted</span>
            <span className="font-medium">{user?.permissions.length}</span>
          </div>
          <a href="#" className="inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline">
            View full permission list <ArrowUpRight className="h-3 w-3" />
          </a>
        </CardContent>
      </Card>
    </div>
  );
}
