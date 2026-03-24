import { Button } from "@/components/ui/button";

interface AllSetPageProps {
  onFinish: () => void;
}

export function AllSetPage({ onFinish }: AllSetPageProps) {
  return (
    <div className="flex flex-col items-center text-center py-8">
      <span className="text-5xl mb-4">🎉</span>
      <h2 className="text-2xl font-bold mb-2">All Set!</h2>
      <p className="text-sm text-muted-foreground mb-2">
        Your preferences have been saved.
      </p>
      <p className="text-sm text-muted-foreground mb-8">
        You can change them anytime in Settings.
      </p>
      <p className="text-base font-medium mb-6">
        Enjoy your wallpapers!
      </p>
      <Button onClick={onFinish} size="lg">
        Start Using App
      </Button>
    </div>
  );
}
