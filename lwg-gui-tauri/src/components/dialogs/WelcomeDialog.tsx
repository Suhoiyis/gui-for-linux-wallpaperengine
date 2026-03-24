import { useMemo, useState } from "react";
import { Dialog, DialogContent } from "@/components/ui/dialog";

import { WelcomePage } from "./welcome/WelcomePage";
import { RequirementsPage } from "./welcome/RequirementsPage";
import { DirectoriesPage } from "./welcome/DirectoriesPage";
import { QuickSettingsPage } from "./welcome/QuickSettingsPage";
import { AllSetPage } from "./welcome/AllSetPage";
import { useAppStore } from "@/store/appStore";
import { cn } from "@/lib/utils";

interface WelcomeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  isRequired?: boolean;
}

export function WelcomeDialog({ open, onOpenChange, isRequired }: WelcomeDialogProps) {
  const [step, setStep] = useState(0);
  const completeOnboarding = useAppStore((s) => s.completeOnboarding);

  const dots = useMemo(() => {
    const total = 5;
    return Array.from({ length: total }, (_, idx) => idx);
  }, []);

  const goNext = () => setStep((s) => Math.min(4, s + 1));
  const goPrev = () => setStep((s) => Math.max(0, s - 1));

  const handleFinish = async () => {
    await completeOnboarding();
    // If save failed in Tauri mode, store will revert and keep dialog open.
    // If save succeeded (or mock mode), close request is safe.
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        onEscapeKeyDown={(e) => isRequired && e.preventDefault()}
        onPointerDownOutside={(e) => isRequired && e.preventDefault()}
        className={cn(
          "sm:max-w-[560px]",
          isRequired ? "[&>button]:hidden" : "",
        )}
      >
        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2 pt-1">
          {dots.map((idx) => (
            <span
              key={idx}
              className={cn(
                "h-2 w-2 rounded-full transition-colors",
                idx === step ? "bg-foreground" : "bg-muted-foreground/30",
              )}
              aria-label={`Step ${idx + 1} of 5`}
            />
          ))}
        </div>

        {/* Pages */}
        <div className="animate-in fade-in slide-in-from-top-2 duration-300">
          {step === 0 && <WelcomePage onNext={goNext} />}
          {step === 1 && <RequirementsPage onNext={goNext} />}
          {step === 2 && <DirectoriesPage onNext={goNext} onSkip={goNext} />}
          {step === 3 && <QuickSettingsPage onNext={goNext} onSkip={goNext} />}
          {step === 4 && <AllSetPage onFinish={handleFinish} />}
        </div>

        {/* Back button (hidden on first/last pages) */}
        {step > 0 && step < 4 && (
          <div className="flex justify-start">
            <button
              type="button"
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
              onClick={goPrev}
            >
              Back
            </button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
