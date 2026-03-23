// 在你的 Wallpapers 页面组件里
import { useAppStore } from "@/store/appStore";

// ... Inside Component
const setWallpapers = useAppStore((state) => state.setWallpapers);
const setSelectedId = useAppStore((state) => state.setSelectedId);
const selectedId = useAppStore((state) => state.selectedId);

// ... 获取数据后
useEffect(() => {
  scanWallpapers().then((data) => {
    setWallpapers(data); // 存入 store
  });
}, []);

// ... 在渲染 Card 的地方
<div
  onClick={() => setSelectedId(item.id)} // 👈 关键：点击选中
  className={`cursor-pointer border-2 ${selectedId === item.id ? "border-brand" : "border-transparent"}`}
>
  {/* ... Card Content ... */}
</div>;
