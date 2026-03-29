import { useEffect, useRef, useCallback, useState } from "react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
  type CarouselApi,
} from "@/components/ui/carousel";
import { Wallpaper } from "@/types";
import { Thumbnail } from "@/components/common/Thumbnail";

interface CompactCarouselProps {
  /** 壁纸列表 */
  wallpapers: Wallpaper[];
  /** 当前选中的壁纸 ID */
  selectedId: string | null;
  /** 选择壁纸回调 */
  onSelect: (id: string) => void;
  /** 滑动/悬停时的实时预览回调 */
  onHoverPreview?: (id: string | null) => void;
}



/**
 * Compact 模式底部缩略图轮播组件
 * 包含：缩略图轮播、选中状态同步、鼠标拖拽滚动
 */
export function CompactCarousel({
  wallpapers,
  selectedId,
  onSelect,
  onHoverPreview,
}: CompactCarouselProps) {
  const [api, setApi] = useState<CarouselApi | undefined>(undefined);
  const [localHoverId, setLocalHoverId] = useState<string | null>(null);
  
  // 用于区分“用户手动拖拽”和“外部触发的 api.scrollTo()”
  // 外部触发的滚动不应该发射 onHoverPreview 事件，避免上方大图闪烁
  const isAutoScrollingRef = useRef(false);

  // 使用 ref 保持回调最新，避免 useEffect 因 onSelect 变化重新注册
  const onSelectRef = useRef(onSelect);
  onSelectRef.current = onSelect;

  const selectedIdRef = useRef(selectedId);
  selectedIdRef.current = selectedId;

  const wallpapersRef = useRef(wallpapers);
  wallpapersRef.current = wallpapers;

  const onHoverPreviewRef = useRef(onHoverPreview);
  onHoverPreviewRef.current = onHoverPreview;

  const handleSetApi = useCallback((newApi: CarouselApi) => {
    setApi(newApi);
  }, []);

  // 监听 Embla 的事件，同步选中和实时预览状态
  useEffect(() => {
    if (!api) return;

    // 当滚动完全停止并锁定到一个 snap point 时
    const handleSelect = () => {
      const snapIndex = api.selectedScrollSnap();
      const targetWp = wallpapersRef.current[snapIndex];
      if (targetWp && targetWp.id !== selectedIdRef.current) {
        onSelectRef.current(targetWp.id);
      }
      // 触发真实选中后，清除悬停预览
      onHoverPreviewRef.current?.(null);
      setLocalHoverId(null);
      isAutoScrollingRef.current = false;
    };

    // 当用户正在滚动时实时触发
    const handleScroll = () => {
      // 如果是外部调用 scrollTo 引起的滚动动画，则忽略，避免画面闪烁
      if (isAutoScrollingRef.current) return;

      // selectedScrollSnap() 会略过中间项，直接报告终点
      // slidesInView() 会实时返回当前视野内的卡片索引数组（通常是奇数个）
      const inView = api.slidesInView();
      if (inView.length > 0) {
        // 取视野正中间的索引
        const centerIndex = inView[Math.floor(inView.length / 2)];
        const targetWp = wallpapersRef.current[centerIndex];
        if (targetWp) {
          onHoverPreviewRef.current?.(targetWp.id);
          setLocalHoverId(targetWp.id);
        }
      }
    };

    // 当手指松开，轮播图惯性停止时，清除预览状态让视图恢复到 selectedId
    // 用户停下来如果不改变选择，这里会触发；如果改变了，会触发 select
    const handleSettle = () => {
      onHoverPreviewRef.current?.(null);
      setLocalHoverId(null);
      isAutoScrollingRef.current = false;
    };

    api.on("select", handleSelect);
    api.on("scroll", handleScroll);
    api.on("settle", handleSettle);
    
    return () => {
      api.off("select", handleSelect);
      api.off("scroll", handleScroll);
      api.off("settle", handleSettle);
    };
  }, [api]); // re-register when api becomes available

  // 当外部 selectedId 变化时，同步轮播位置
  useEffect(() => {
    if (!api) return;

    const index = wallpapers.findIndex((w) => w.id === selectedId);
    if (index !== -1 && api.selectedScrollSnap() !== index) {
      isAutoScrollingRef.current = true;
      api.scrollTo(index);
    }
  }, [selectedId, wallpapers]);

  // 点击缩略图：直接选中 + 滚动
  const handleItemClick = useCallback(
    (wp: Wallpaper, index: number) => {
      // 直接触发选中，不依赖 Embla 的 "select" 事件
      onSelect(wp.id);
      // 同时滚动到该位置
      isAutoScrollingRef.current = true;
      api?.scrollTo(index);
    },
    [onSelect, api],
  );

  return (
    <div className="p-2 border-t bg-muted/10 relative group">
      <Carousel
        setApi={handleSetApi}
        opts={{
          align: "center",
          loop: true,
          dragFree: true, // 允许自由拖拽（惯性滚动）
        }}
        className="w-full max-w-full"
      >
        <CarouselContent className="-ml-1">
          {wallpapers.map((wp, index) => (
            <CarouselItem key={wp.id} className="pl-1 basis-1/5 select-none">
              <div
                className={`
                  aspect-square rounded-md overflow-hidden cursor-pointer transition-all border-2
                  ${(localHoverId || selectedId) === wp.id ? "border-primary shadow-md scale-95" : "border-transparent opacity-60 hover:opacity-100"}
                `}
                onClick={() => handleItemClick(wp, index)}
              >
                <Thumbnail 
                  wallpaperId={wp.id} 
                  className="w-full h-full rounded-none border-none"
                />
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious className="left-1 h-6 w-6 opacity-0 group-hover:opacity-70 transition-opacity hover:!opacity-100 disabled:hidden" />
        <CarouselNext className="right-1 h-6 w-6 opacity-0 group-hover:opacity-70 transition-opacity hover:!opacity-100 disabled:hidden" />
      </Carousel>
    </div>
  );
}
