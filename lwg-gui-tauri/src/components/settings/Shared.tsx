// src/components/settings/Shared.tsx
import { Check, ChevronsUpDown } from "lucide-react";
import { isTauriEnv } from "@/lib/utils";
import { cn } from "@/lib/utils";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { open } from "@tauri-apps/plugin-dialog";
import { useEffect, useState } from "react";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { FolderOpen } from "lucide-react";

// ============================================================================
// Types
// ============================================================================

interface SwitchRowProps {
  label: string;
  description?: string;
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
  icon?: React.ReactNode;
  disabled?: boolean;
}

interface SliderRowProps {
  label: string;
  value: number;
  onValueChange: (value: number) => void;
  max: number;
  min?: number;
  step?: number;
  suffix?: string;
}

// ============================================================================
// Constants
// ============================================================================

export const SCALING_OPTIONS = [
  { value: "default", label: "Default" },
  { value: "stretch", label: "Stretch" },
  { value: "fit", label: "Fit" },
  { value: "fill", label: "Fill" },
] as const;

export const CLAMPING_OPTIONS = [
  { value: "clamp", label: "Clamp" },
  { value: "border", label: "Border" },
  { value: "repeat", label: "Repeat" },
] as const;

export const CYCLE_ORDER_OPTIONS = [
  { value: "random", label: "Random" },
  { value: "id", label: "By ID (sequential)" },
] as const;

export const RESOLUTION_OPTIONS = [
  { value: "3840x2160", label: "4K (3840x2160)" },
  { value: "2560x1440", label: "2K (2560x1440)" },
  { value: "1920x1080", label: "FHD (1920x1080)" },
  { value: "1366x768", label: "HD+ (1366x768)" },
  { value: "1280x720", label: "HD (1280x720)" },
] as const;

export const THEME_OPTIONS = [
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
  { value: "system", label: "System" },
] as const;

export const LOG_FILTER_OPTIONS = [
  { value: "All", label: "All Sources" },
  { value: "GUI", label: "GUI Only" },
  { value: "Core", label: "Core Only" },
  { value: "Engine", label: "Engine Only" },
  { value: "Controller", label: "Controller Only" },
] as const;

export const LOG_LEVEL_COLORS: Record<string, string> = {
  info: "text-blue-500",
  warn: "text-amber-500",
  error: "text-red-500",
};

// ============================================================================
// Utility Functions
// ============================================================================

export const getLevelColor = (level: string): string => {
  return LOG_LEVEL_COLORS[level] || "text-muted-foreground";
};

export const formatLogEntry = (log: {
  timestamp: string;
  level: string;
  source: string;
  message: string;
}): string => {
  return `[${log.timestamp}] [${log.level.toUpperCase()}] [${log.source}] ${log.message}`;
};

// ============================================================================
// Reusable Components
// ============================================================================

export function Header({ title, desc }: { title: string; desc: string }) {
  return (
    <div>
      <h3 className="text-lg font-medium">{title}</h3>
      <p className="text-sm text-muted-foreground">{desc}</p>
      <Separator className="my-2" />
    </div>
  );
}

export function SwitchRow({
  label,
  description,
  checked,
  onCheckedChange,
  icon,
  disabled,
}: SwitchRowProps) {
  return (
    <div
      className={
        "flex items-center justify-between " + (disabled ? "opacity-50" : "")
      }
    >
      <div className="flex items-center gap-2">
        {icon}
        <div className="space-y-0.5">
          <Label>{label}</Label>
          {description && (
            <p className="text-xs text-muted-foreground">{description}</p>
          )}
        </div>
      </div>
      <Switch
        checked={checked}
        onCheckedChange={onCheckedChange}
        disabled={disabled}
      />
    </div>
  );
}

// ✨ 修复后的 SliderRow：包含输入功能，并解决 FPS 重叠
export function SliderRow({
  label,
  value,
  onValueChange,
  max,
  min = 0,
  step = 1,
  suffix = "",
}: SliderRowProps) {
  // 本地字符串状态，处理暂时不合规的输入（如空字符串）
  const [inputValue, setInputValue] = useState(value.toString());

  // 外部 value 改变时，同步更新输入框
  useEffect(() => {
    setInputValue(value.toString());
  }, [value]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  // 统一的数值确认逻辑（Blur 或 Enter 触发）
  const handleCommit = () => {
    let newValue = parseFloat(inputValue);

    // 如果输入非数字，重置原值
    if (isNaN(newValue)) {
      setInputValue(value.toString());
      return;
    }

    // 限制在 [min, max] 范围内
    if (newValue > max) newValue = max;
    if (newValue < min) newValue = min;

    // 更新本地状态（可能会调整用户输入的边界值）
    setInputValue(newValue.toString());
    // 通知父组件
    onValueChange(newValue);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleCommit();
      e.currentTarget.blur();
    } else if (e.key === "Escape") {
      setInputValue(value.toString());
      e.currentTarget.blur();
    }
  };

  // ✨ 视觉修复核心：根据后缀长度，动态计算 Input 的右内边距
  // 每个字符大约占 6px (针对 xs font-mono)，再加上 8px 的基础间距
  const paddingRight = suffix ? `${suffix.length * 6 + 10}px` : "10px";

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <Label>{label}</Label>

        {/* ✨ 优化：带后缀的高级输入框容器 */}
        <div className="relative flex items-center">
          <Input
            value={inputValue}
            onChange={handleInputChange}
            onBlur={handleCommit}
            onKeyDown={handleKeyDown}
            style={{ paddingRight: paddingRight }} // ✨ 应用动态边距，杜绝重叠
            className="h-7 w-24 text-right font-mono text-xs bg-muted border-transparent hover:border-border focus:border-primary focus:ring-1 focus:ring-primary transition-all rounded"
          />
          {/* 绝对定位的后缀单位 */}
          <span className="absolute right-2 text-xs font-mono text-muted-foreground/70 pointer-events-none">
            {suffix}
          </span>
        </div>
      </div>

      <Slider
        value={[value]}
        onValueChange={(v) => {
          // 拖动时同步更新输入框
          setInputValue(v[0].toString());
          onValueChange(v[0]);
        }}
        max={max}
        min={min}
        step={step}
        className="py-2"
      />
    </div>
  );
}

export function SelectField({
  label,
  value,
  onValueChange,
  options,
}: {
  label: string;
  value: string;
  onValueChange: (value: string) => void;
  options: readonly { value: string; label: string }[];
}) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Select value={value} onValueChange={onValueChange}>
        <SelectTrigger>
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {options.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}

export function InputField({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
  min,
}: {
  label: string;
  value: string | number;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
  min?: number;
}) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Input
        type={type}
        min={min}
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export function PathInputField({
  label,
  value,
  onChange,
  placeholder,
  className,
}: {
  label: string | React.ReactNode;
  value: string;
  onChange: (value: string | null) => void;
  placeholder?: string;
  className?: string;
}) {
  const handleBrowse = async () => {
    const isTauri = isTauriEnv();
    if (!isTauri) {
      console.warn("[Browser Mode] File dialog not available");
      return;
    }

    try {
      const selected = await open({
        directory: true,
        multiple: false,
        defaultPath: value || undefined,
      });

      if (selected && typeof selected === "string") {
        onChange(selected);
      }
    } catch (error) {
      console.error("Failed to open directory dialog:", error);
    }
  };

  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <div className="flex space-x-2">
        <Input
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value || null)}
          className={className}
        />
        <Button variant="secondary" onClick={handleBrowse}>
          <FolderOpen className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}

export function SwitchCard({
  label,
  description,
  checked,
  onCheckedChange,
}: {
  label: string;
  description: string;
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
}) {
  return (
    <div className="space-y-3 p-3 bg-muted/30 rounded-lg">
      <div className="flex items-center justify-between">
        <Label className="text-sm">{label}</Label>
        <Switch checked={checked} onCheckedChange={onCheckedChange} />
      </div>
      <p className="text-[10px] text-muted-foreground">{description}</p>
    </div>
  );
}

export function TextareaField({
  label,
  value,
  onChange,
  placeholder,
  description,
  disabled,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  description?: string;
  disabled?: boolean;
}) {
  return (
    <div
      className={"space-y-2 flex flex-col " + (disabled ? "opacity-50" : "")}
    >
      <div className="space-y-0.5">
        <Label>{label}</Label>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </div>
      <Textarea
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="resize-none min-h-[80px]"
        disabled={disabled}
      />
    </div>
  );
}

// ✨ 新增：支持下拉选择 + 自由输入的终极 Combobox 组件
export function EditableComboboxField({
  label,
  value,
  onChange,
  options,
  placeholder = "Select or type...",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: readonly { value: string; label: string }[];
  placeholder?: string;
}) {
  const [open, setOpen] = useState(false);
  // 记录用户正在输入的搜索词
  const [inputValue, setInputValue] = useState("");

  // 如果当前选中的值在预设里，显示标签（如 "FHD (1920x1080)"），否则直接显示用户的自定义值
  const selectedLabel =
    options.find((opt) => opt.value === value)?.label || value;

  return (
    <div className="space-y-2 flex flex-col">
      <Label>{label}</Label>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between font-normal bg-background"
          >
            {value ? selectedLabel : placeholder}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] p-0" align="start">
          <Command>
            <CommandInput
              placeholder="Search or type custom resolution..."
              value={inputValue}
              onValueChange={setInputValue}
            />
            <CommandList>
              <CommandEmpty>
                {/* 如果搜不到标准选项，就把它变成一个【确认使用自定义值】的按钮 */}
                {inputValue ? (
                  <button
                    className="w-full text-left px-2 py-1.5 text-sm hover:bg-accent hover:text-accent-foreground rounded-sm cursor-pointer"
                    onClick={() => {
                      onChange(inputValue);
                      setOpen(false);
                      setInputValue("");
                    }}
                  >
                    Use custom:{" "}
                    <span className="font-bold">"{inputValue}"</span>
                  </button>
                ) : (
                  "No options found."
                )}
              </CommandEmpty>
              <CommandGroup>
                {/* 1. 渲染标准选项 */}
                {options.map((option) => (
                  <CommandItem
                    key={option.value}
                    value={option.value}
                    onSelect={() => {
                      onChange(option.value);
                      setOpen(false);
                      setInputValue("");
                    }}
                  >
                    <Check
                      className={cn(
                        "mr-2 h-4 w-4",
                        value === option.value ? "opacity-100" : "opacity-0",
                      )}
                    />
                    {option.label}
                  </CommandItem>
                ))}

                {/* 2. 如果用户输入的字符不在标准选项里，在列表底部动态追加一个自定义选项 */}
                {inputValue && !options.find((o) => o.value === inputValue) && (
                  <CommandItem
                    key={inputValue}
                    value={inputValue}
                    onSelect={() => {
                      onChange(inputValue);
                      setOpen(false);
                      setInputValue("");
                    }}
                  >
                    <Check
                      className={cn(
                        "mr-2 h-4 w-4",
                        value === inputValue ? "opacity-100" : "opacity-0",
                      )}
                    />
                    Use custom:{" "}
                    <span className="font-bold ml-1">"{inputValue}"</span>
                  </CommandItem>
                )}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
