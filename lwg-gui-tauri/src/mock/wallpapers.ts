// src/mock/wallpapers.ts
export const MOCK_WALLPAPERS = Array.from({ length: 20 }).map((_, i) => {
  const images = [
    "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=800&q=80", // 雾中山脉
    "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=800&q=80", // 深色森林
    "https://images.unsplash.com/photo-1506259091721-347f79819525?w=800&q=80", // 极简海面
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80", // 科技感星空
    "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=800&q=80", // 傍晚湖泊
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80", // 森林阳光
  ];

  return {
    id: `wp-${i}`,
    title:
      [
        "Misty Peaks",
        "Deep Forest",
        "Silent Ocean",
        "Neural Starfield",
        "Sunset Lake",
        "Hidden Grove",
      ][i % 6] + ` #${i}`,
    preview: images[i % images.length],
    type: (i % 3 === 0 ? "Video" : i % 3 === 1 ? "Scene" : "Web") as any,
    path: `/home/user/wallpapers/wp${i}.mp4`,
  };
});
