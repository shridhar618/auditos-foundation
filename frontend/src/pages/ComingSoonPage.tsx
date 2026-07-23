import { Construction } from "lucide-react";

export default function ComingSoonPage({ title }: { title: string }) {
  return (
    <div className="flex h-[60vh] flex-col items-center justify-center text-center">
      <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-muted">
        <Construction className="h-6 w-6 text-muted-foreground" />
      </div>
      <h2 className="text-xl font-semibold">{title}</h2>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">
        This module is scheduled for the next build phase, following the feature-by-feature roadmap.
      </p>
    </div>
  );
}
