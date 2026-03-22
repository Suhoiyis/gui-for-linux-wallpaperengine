import * as React from "react";
import { cn } from "../lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "ghost" | "outline" | "destructive";
  size?: "default" | "sm" | "lg" | "icon";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    // 基础样式：圆角、居中、过渡动画
    const baseStyles =
      "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-95";

    // 变体样式 (Variants)
    const variants = {
      default:
        "bg-primary text-black hover:bg-blue-400 shadow-lg shadow-blue-900/20",
      secondary: "bg-white/10 text-white hover:bg-white/20",
      ghost: "text-gray-400 hover:text-white hover:bg-white/5", // 用于导航栏按钮
      outline:
        "border border-white/10 bg-transparent hover:bg-white/5 text-white",
      destructive: "bg-red-500 text-white hover:bg-red-600",
    };

    // 尺寸样式 (Sizes)
    const sizes = {
      default: "h-10 px-4 py-2",
      sm: "h-9 rounded-md px-3",
      lg: "h-12 rounded-md px-8",
      icon: "h-10 w-10", // 用于纯图标按钮
    };

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

export { Button };
