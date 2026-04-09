import React from "react";
import { UsernameChecker } from "@/components/UsernameChecker";

export default function Home() {
  return (
    <div className="min-h-[100dvh] w-full flex flex-col items-center justify-center bg-background px-4 py-12 md:py-24">
      <div className="w-full max-w-lg mx-auto relative">
        {/* Subtle decorative background blur */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-primary/5 blur-3xl rounded-full pointer-events-none -z-10" />
        
        <UsernameChecker />
        
        <div className="mt-12 text-center">
          <p className="text-xs text-muted-foreground font-medium uppercase tracking-widest">
            A precise pocket tool
          </p>
        </div>
      </div>
    </div>
  );
}
