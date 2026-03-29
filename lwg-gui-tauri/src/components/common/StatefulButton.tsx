"use client";

import * as React from "react";
import { Button as ShadcnButton, ButtonProps } from "@/components/ui/button";
import { AnimatePresence, motion } from "framer-motion";
import { Loader2, Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatefulButtonProps extends Omit<ButtonProps, "onClick"> {
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => Promise<void> | void;
}

export function Button({
  children,
  onClick,
  className,
  variant = "ghost",
  size = "icon",
  ...props
}: StatefulButtonProps) {
  const [status, setStatus] = React.useState<"idle" | "loading" | "success">(
    "idle",
  );

  const handleClick = async (e: React.MouseEvent<HTMLButtonElement>) => {
    // 如果没有传入 onClick，直接返回
    if (!onClick) return;

    // 如果正在处理中，阻止重复点击
    if (status !== "idle") {
      e.preventDefault();
      return;
    }

    setStatus("loading");
    try {
      // ✨ 修复 3：调用 onClick 时把事件 e 传回去
      await onClick(e);
      setStatus("success");
      setTimeout(() => {
        setStatus("idle");
      }, 1500);
    } catch (error) {
      console.error(error);
      setStatus("idle");
    }
  };

  return (
    <ShadcnButton
      variant={variant}
      size={size}
      className={cn(
        "relative transition-all",
        status === "success" &&
          "text-green-500 hover:text-green-600 hover:bg-green-500/10",
        className,
      )}
      onClick={handleClick}
      disabled={status === "loading"}
      {...props}
    >
      <AnimatePresence mode="popLayout" initial={false}>
        {status === "idle" && (
          <motion.span
            key="idle"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.2 }}
            className="flex items-center justify-center w-full h-full"
          >
            {children}
          </motion.span>
        )}

        {status === "loading" && (
          <motion.span
            key="loading"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <Loader2 className="h-4 w-4 animate-spin" />
          </motion.span>
        )}

        {status === "success" && (
          <motion.span
            key="success"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <Check className="h-4 w-4" />
          </motion.span>
        )}
      </AnimatePresence>
    </ShadcnButton>
  );
}
