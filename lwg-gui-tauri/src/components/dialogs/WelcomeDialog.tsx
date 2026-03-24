import { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

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

const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 200 : -200,
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 200 : -200,
    opacity: 0,
  }),
};

export function WelcomeDialog({ open, onOpenChange, isRequired }: WelcomeDialogProps) {
  const [step, setStep] = useState(0);
  const [direction, setDirection] = useState(1);
  const completeOnboarding = useAppStore((s) => s.completeOnboarding);

  const dots = useMemo(() => {
    const total = 5;
    return Array.from({ length: total }, (_, idx) => idx);
  }, []);

  const goNext = () => {
    setDirection(1);
    setStep((s) => Math.min(4, s + 1));
  };
  
  const goPrev = () => {
    setDirection(-1);
    setStep((s) => Math.max(0, s - 1));
  };

  const handleFinish = async () => {
    await completeOnboarding();
    onOpenChange(false);
  };

  const renderPage = () => {
    switch (step) {
      case 0:
        return <WelcomePage />;
      case 1:
        return <RequirementsPage />;
      case 2:
        return <DirectoriesPage />;
      case 3:
        return <QuickSettingsPage />;
      case 4:
        return <AllSetPage />;
      default:
        return null;
    }
  };

  const getPageTitle = () => {
    switch (step) {
      case 0:
        return "Welcome";
      case 1:
        return "Requirements Check";
      case 2:
        return "Directories";
      case 3:
        return "Quick Settings";
      case 4:
        return "All Set!";
      default:
        return "";
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        onEscapeKeyDown={(e) => isRequired && e.preventDefault()}
        onPointerDownOutside={(e) => isRequired && e.preventDefault()}
        className={cn(
          "w-[600px] h-[480px] max-w-none max-h-none",
          "flex flex-col",
          "p-0",
          isRequired ? "[&>button]:hidden" : "",
        )}
      >
        <div className="flex flex-col items-center gap-2 pt-5 pb-3 px-6 shrink-0 border-b border-border/50">
          <div className="flex items-center gap-2">
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
          <h2 className="text-sm font-medium text-muted-foreground">{getPageTitle()}</h2>
        </div>

        <div className="flex-1 overflow-hidden min-h-0 px-6 relative">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.div
              key={step}
              custom={direction}
              variants={variants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.18, ease: "easeOut" }}
              className="h-full overflow-hidden"
            >
              {renderPage()}
            </motion.div>
          </AnimatePresence>
        </div>

        <div className="flex items-center justify-between px-6 py-4 shrink-0 border-t border-border/50 bg-muted/20">
          <div className="w-24">
            {step > 0 && (
              <Button variant="ghost" size="sm" onClick={goPrev}>
                Back
              </Button>
            )}
          </div>

          <div className="flex justify-end gap-2">
            {step < 4 ? (
              <Button size="sm" onClick={goNext}>
                {step === 0 ? "Get Started" : "Continue"}
              </Button>
            ) : (
              <Button size="sm" onClick={handleFinish}>
                Start Using App
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}