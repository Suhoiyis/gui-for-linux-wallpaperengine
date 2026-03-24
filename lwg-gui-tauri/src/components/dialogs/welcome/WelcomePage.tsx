import { Button } from "@/components/ui/button";

interface WelcomePageProps {
  onNext: () => void;
}

export function WelcomePage({ onNext }: WelcomePageProps) {
  return (
    <div className="flex flex-col items-center text-center py-6">
      {/* Logo */}
      <div className="h-24 w-24 rounded-[22%] overflow-hidden shadow-xl border border-border/40 mb-6 bg-background flex items-center justify-center">
        <img
          src="/GUI_rounded.png"
          alt="LWG Logo"
          className="w-full h-full object-cover"
          onError={(e) => {
             e.currentTarget.style.display = 'none';
          }}
        />
      </div>
      
      {/* Title */}
      <h1 className="text-2xl font-bold mb-2">Linux Wallpaper Engine GUI</h1>
      <p className="text-xl text-muted-foreground mb-4">Welcome!</p>
      
      {/* Description */}
      <p className="text-sm text-muted-foreground mb-8 max-w-sm">
        A modern GUI for applying Steam Workshop live wallpapers on Linux.
      </p>
      
      {/* Button */}
      <Button onClick={onNext} size="lg">
        Get Started
      </Button>
    </div>
  );
}
