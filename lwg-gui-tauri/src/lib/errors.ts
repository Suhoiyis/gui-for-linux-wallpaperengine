import { toast } from "sonner";

/**
 * 统一处理 API 错误
 * @param error - 错误对象
 * @param context - 错误上下文描述
 */
export const handleApiError = (error: unknown, context: string): void => {
  console.error(`[${context}]`, error);
  toast.error(context, {
    description: error instanceof Error ? error.message : String(error),
  });
};

/**
 * 统一处理 API 警告
 * @param message - 警告消息
 * @param context - 警告上下文描述
 */
export const handleApiWarning = (message: string, context: string): void => {
  console.warn(`[${context}]`, message);
  toast.warning(context, {
    description: message,
  });
};